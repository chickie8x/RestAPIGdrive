from django.db import models
import getlinks
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Create your models here.
creds =getlinks.getCreds()
drive =build('drive','v3',credentials=creds)
class LinkExtract(models.Model):
    fileName=models.CharField(max_length=500,null=True,blank=True)
    fileId = models.CharField(max_length=200,blank=True,null=True)
    url = models.CharField(max_length=500)
    directUrl =models.CharField(max_length=500,blank=True,null=True)
    fileSize =models.CharField(max_length=100,blank=True,null=True)
    fileExtension = models.CharField(max_length=100,blank=True,null=True)
    publishDate =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fileName

    def save(self, *args,**kwargs):
        obj = getlinks.getFile(self.url,drive)
        self.fileId = obj['id']
        self.fileName=obj['name']
        self.directUrl='https://drive.google.com/uc?id=' + obj["id"] + '&export=download'
        self.fileSize=obj['size']
        self.fileExtension = obj['fileExtension']
        return super(LinkExtract, self).save(*args, **kwargs)

