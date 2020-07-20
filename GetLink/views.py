from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from googleapiclient.discovery import build
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import api_view, renderer_classes

import getlinks
from .models import FileObject
from .serializers import GetLinkSerializers
from .forms import InputForm, SignUpForm

creds = getlinks.getCreds()
drive = build('drive', 'v3', credentials=creds)


# Create your views here.
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


# @login_required
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
    return render(request, 'GetLink/explorer.html', {'files': files})


def index(request):
    if request.method == 'POST':
        my_form = InputForm(request.POST)
        if my_form.is_valid():
            data = my_form.cleaned_data.get('user_input')
            originalFileID = getlinks.extract_files_id(data)
            if FileObject.objects.filter(originalID=originalFileID).exists():
                return redirect('/' + originalFileID)
            else:
                FileObject.objects.create(url=data)
                return redirect('/' + originalFileID)

    else:
        my_form = InputForm()
    return render(request, 'GetLink/index.html', {'form': my_form})


def getById(request, fileId):
    files = FileObject.objects.filter(originalID=fileId)
    return render(request, 'GetLink/getbyid.html', {'files': files})


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
