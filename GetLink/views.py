import time

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.dispatch import receiver
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from googleapiclient.discovery import build
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import getlinks
from .forms import SignUpForm, LoginForm
from .models import FileObject, SubscribeList
from .serializers import GetLinkSerializers

creds = getlinks.getCreds()
drive = build('drive', 'v3', credentials=creds)




# Create your views here.
@login_required
@api_view(['GET', 'POST'])
def listFile(request):
    if request.method == 'GET':
        fileList = FileObject.objects.all()
        serializer = GetLinkSerializers(fileList, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serilizer = GetLinkSerializers(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data, status=status.HTTP_201_CREATED)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['GET', 'POST'])
def viewFile(request, fileId):
    if request.method == 'GET':
        file = FileObject.objects.filter(fileId=fileId).order_by('fileId')
        serializer = GetLinkSerializers(file, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response("Object not found", status=status.HTTP_400_BAD_REQUEST)


def explorer(request):
    files = FileObject.objects.all()
    userid = request.user.id
    return render(request, 'GetLink/explorer.html', {'files': files, 'userid': userid})


def index(request):
    if request.method == 'POST':
        data = request.POST.get('get_input')
        if getlinks.checkurl(data):
            originalFileID = getlinks.extract_files_id(data)
            if FileObject.objects.filter(originalID=originalFileID).exists():
                print('exists')
                return redirect('/file/' + originalFileID)
            else:
                print('create')
                FileObject.objects.create(url=data)
                return redirect('/file/' + originalFileID)
        else:
            results = FileObject.objects.filter(fileName__contains=data)
            return render(request, 'GetLink/search.html', {'results': results})
    else:
        return render(request, 'GetLink/index.html')


def getById(request, fileId):
    file = FileObject.objects.filter(originalID=fileId)[0]
    context = {
        'fileID': file.id,
        'fileName': file.fileName,
        'fileSize': file.fileSize,
        'genId': file.storedFileId,
        'originalID': file.originalID,
        'views': file.counter
    }
    return render(request, 'GetLink/getbyid.html', context=context)


def genLink(request):
    if request.method == 'POST':
        parameter = request.POST.get('parameter')
        link = getlinks.fileClone(drive, parameter)['webContentLink']
        return JsonResponse({'link': link}, status=200)


def register(request):
    if request.method == 'POST':
        register_form = SignUpForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            return redirect('/')
    else:
        register_form = SignUpForm()
    return render(request, 'GetLink/register.html', {'form': register_form})


def loginView(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                if 'next' in request.GET:
                    messages.success(request, 'You have been login as ' + str(request.user))
                    nexturl = request.GET.get('next')
                    return HttpResponseRedirect(nexturl)
                else:
                    messages.success(request, 'You have been login as ' + str(request.user))
                    return redirect('/')
            else:
                messages.warning(request, 'Invalid login infomation')
                login_form = LoginForm()
                return render(request, 'GetLink/login.html', {'form': login_form})
        else:
            messages.warning(request, 'Invalid login infomation')
            return redirect('/accounts/login/')
    else:
        login_form = LoginForm()
        return render(request, 'GetLink/login.html', {'form': login_form})


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    if not user:
        mes = ''
    else:
        mes = 'You have been logged out'
    messages.add_message(request, messages.WARNING, mes)


def logout_view(request):
    logout(request)


@login_required
def ajax_post(request):
    userid = request.user.id
    fileid = request.POST.get('fileid')
    file = FileObject.objects.get(pk=fileid)
    user = User.objects.get(pk=userid)
    title = file.fileName
    time.sleep(1)
    if not SubscribeList.objects.filter(fileID=fileid, userID=userid).exists():
        obj = SubscribeList.objects.create(userID=user, fileID=file, title=title)
        result = obj.title + ' is added to list'
        messages.add_message(request, messages.SUCCESS, result)
    else:
        obj = SubscribeList.objects.get(fileID=fileid, userID=userid)
        result = obj.title + ' is already exist'
        messages.add_message(request, messages.WARNING, result)

    return JsonResponse({'mes': result}, status=200)


@login_required
def subList(request):
    userid = request.user.id
    obj = FileObject.objects.filter(subscribelist__userID=userid)
    return render(request, 'GetLink/sublist.html', {'sublist': obj})


@login_required
def deleteFile(request):
    userid = request.user.id
    fileid = request.POST.get('fileid')
    try:
        file = SubscribeList.objects.filter(fileID=fileid, userID=userid)
        file.delete()
        mes = ' successfully delete file'
        messages.add_message(request, messages.SUCCESS, mes)
    except:
        mes = 'failed to delete file :('
        messages.add_message(request, messages.WARNING, mes)
    return JsonResponse({'mes': mes}, status=200)


@login_required
def pwchange(request):
    if request.method == 'POST':
        userid = request.user.id
        user = User.objects.get(pk=userid)
        oldPassword = request.user.password
        oldPasswordEntered = request.POST.get('old-password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        matchcheck = check_password(oldPasswordEntered, oldPassword)
        if matchcheck:
            if getlinks.validatePassword(password1, password2):
                user.set_password(password1)
                user.save()
                messages.success(request, 'Password is updated successfully')
                return redirect('/accounts/login/')
            else:
                messages.warning(request, 'Change password failed')
                return redirect('/changepw/')
        else:
            messages.warning(request, 'Wrong current password')
            return redirect('/changepw/')
    else:
        return render(request, 'GetLink/pwchange.html')


def passwordReset(request):
    if request.method == 'POST':
        email = request.POST.get('get_email')
        if email != "":
            users = User.objects.filter(email=email)
            if users:
                subject = 'Password reset requested'
                email_template = 'GetLink/password_reset_email.txt'
                c = {
                    'email': users[0].email,
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(users[0].pk)),
                    "user": users,
                    'token': default_token_generator.make_token(users[0]),
                    'protocol': 'http',
                }
                mail = render_to_string(email_template, c)
                print(mail)
                try:
                    send_mail(subject, mail, 'admin@123.com', ['chickie8x.qn@gmail.com'], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header')
                messages.success(request,
                                 'An email with password reset link has been sent to your inbox , please check ')
                return redirect('/user/password_reset/done/')
            else:
                messages.warning(request,
                                 'Email not found , please check again ')
                return redirect('/user/password_reset/done/')
    else:
        return render(request, 'GetLink/forgotpw.html')


def passwordResetDone(request):
    return render(request, 'GetLink/password_reset_done.html')


def getUrl(request):
    obj = FileObject.objects.all()
    return render(request, 'GetLink/getUrl.html', {'urls': obj})
