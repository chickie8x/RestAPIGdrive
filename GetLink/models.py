from django.db import models
from django.contrib.auth.models import User

import GoogleAuthManager
import getlinks
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Create your models here.
creds = getlinks.getCreds()
# drive = build('drive', 'v3', credentials=creds)
drive = GoogleAuthManager.create_drive_manager()


class FileObject(models.Model):
    fileName = models.CharField(max_length=500)
    originalID = models.CharField(max_length=100)
    fileId = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=500)
    directUrl = models.CharField(max_length=500, blank=True, null=True)
    fileSize = models.CharField(max_length=100, blank=True, null=True)
    fileExtension = models.CharField(max_length=100, blank=True, null=True)
    createdDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fileName

    def save(self, *args, **kwargs):
        self.originalID = getlinks.extract_files_id(self.url)
        obj = getlinks.fileInfo(drive,self.originalID)
        self.fileId = obj['id']
        self.fileName = obj['title']
        self.directUrl = 'https://drive.google.com/uc?id=' + obj["id"] + '&export=download'
        self.fileSize = getlinks.sizeof_file(int(obj['fileSize']), suffix='B')
        self.fileExtension = obj['fileExtension']
        return super(FileObject, self).save(*args, **kwargs)


class SubscribeList(models.Model):
    userID = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    fileID = models.ForeignKey(FileObject, on_delete=models.DO_NOTHING)
