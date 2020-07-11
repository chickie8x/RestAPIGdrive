from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import api_view, renderer_classes

from .models import LinkExtract
from .serializers import GetLinkSerializers
from .forms import InputForm

# Create your views here.
@api_view(['GET','POST'])
def listFile(request):
    if request.method=='GET':
        fileList=LinkExtract.objects.all()
        serializer =GetLinkSerializers(fileList,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serilizer = GetLinkSerializers(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

# @login_required
@api_view(['GET','POST'])
def viewFile(request,fileId):
    if request.method=='GET':
        file = LinkExtract.objects.filter(fileId=fileId).order_by('fileId')
        serializer = GetLinkSerializers(file,many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response("Object not found",status=status.HTTP_400_BAD_REQUEST)



def explorer(request):
    files = LinkExtract.objects.all()
    return render(request,'GetLink/explorer.html',{'files':files})

def index(request):
    if request.method == 'POST':
        my_form = InputForm(request.POST)
        if my_form.is_valid():
            data = my_form.cleaned_data.get('user_input')
            obj=LinkExtract.objects.create(url=data)
            return render(request,'GetLink/fromRedirect.html',{'result':obj})
    else:
        my_form = InputForm()
    return render(request,'GetLink/index.html',{'form':my_form})