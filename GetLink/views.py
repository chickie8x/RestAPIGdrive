from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from googleapiclient.discovery import build
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import getlinks
from .forms import InputForm, SignUpForm, LoginForm
from .models import FileObject, SubscribeList
from .serializers import GetLinkSerializers

creds = getlinks.getCreds()
drive = build('drive', 'v3', credentials=creds)
# driveManager = GoogleAuthManager.create_drive_manager()


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
        my_form = InputForm(request.POST)
        if my_form.is_valid():
            data = my_form.cleaned_data.get('user_input')
            if getlinks.checkurl(data):
                originalFileID = getlinks.extract_files_id(data)
                if FileObject.objects.filter(originalID=originalFileID).exists():
                    return redirect('/' + originalFileID)
                else:
                    FileObject.objects.create(url=data)
                    return redirect('/' + originalFileID)
            else:
                results = FileObject.objects.filter(fileName__contains=data)
                return render(request, 'GetLink/search.html', {'results': results})

    else:
        my_form = InputForm()
    return render(request, 'GetLink/index.html', {'form': my_form})


def getById(request, fileId):
    download = getlinks.fileClone(drive, fileId)['webContentLink']
    file = FileObject.objects.filter(originalID=fileId)[0]
    file.counter += 1
    file.save()

    context = {
        'fileName': file.fileName,
        'fileSize': file.fileSize,
        'download': download,
        'originalID': file.originalID,
        'views': file.counter
    }
    return render(request, 'GetLink/getbyid.html', context=context)


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
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    mes = 'Username or password is incorrect'
                    return render(request, 'GetLink/login.html', {'form': login_form, 'mes': mes})
        else:
            login_form = LoginForm()
            return render(request, 'GetLink/login.html', {'form': login_form})


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def ajax_post(request):
    userid = request.user.id
    fileid = request.POST.get('fileid')
    file = FileObject.objects.get(pk=fileid)
    user = User.objects.get(pk=userid)
    title = file.fileName
    if not SubscribeList.objects.filter(fileID=fileid, userID=userid).exists():
        obj = SubscribeList.objects.create(userID=user, fileID=file, title=title)
        result = obj.title + ' created'
    else:
        obj = SubscribeList.objects.get(fileID=fileid, userID=userid)
        result = obj.title + ' get'
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
    except:
        mes = 'failed to delete file :('
    return JsonResponse({'mes': mes}, status=200)


@login_required
def pwchange(request):
    newpw = request.POST.get('newpw')
    userid = request.user.id
    user = User.objects.get(pk=userid)
    try:
        user.set_password(newpw)
        user.save()
        mes = 'change password sucessfully'
    except:
        mes = 'change password failed'
    return JsonResponse({'mes': mes}, status=200)
