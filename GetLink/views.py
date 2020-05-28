from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import api_view, renderer_classes

from .models import LinkExtract
from .serializers import GetLinkSerializers

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

@login_required
@api_view(['GET','POST'])
def viewFile(request,fileId):
    if request.method=='GET':
        file = LinkExtract.objects.filter(fileId=fileId).order_by('fileId')
        serializer = GetLinkSerializers(file,many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response("Object not found",status=status.HTTP_400_BAD_REQUEST)