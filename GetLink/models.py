from django.contrib.auth.models import User
from django.db import models
from googleapiclient.discovery import build

import getlinks

# Create your models here.
creds = getlinks.getCreds()
drive = build('drive', 'v3', credentials=creds)


# drive = GoogleAuthManager.create_drive_manager()


class FileObject(models.Model):
    fileName = models.CharField(max_length=500)
    originalID = models.CharField(max_length=100)
    storedFileId = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=500)
    fileSize = models.CharField(max_length=100, blank=True, null=True)
    fileExtension = models.CharField(max_length=100, blank=True, null=True)
    createdDate = models.CharField(max_length=100)
    counter = models.IntegerField(default=0)

    def __str__(self):
        return self.fileName

    def save(self, *args, **kwargs):
        self.originalID = getlinks.extract_files_id(self.url)
        obj = getlinks.fileInfo(drive, self.originalID)
        storedFileId = drive.files().copy(fileId=self.originalID, fields='*', supportsAllDrives=True).execute()
        self.storedFileId = storedFileId['id']
        self.fileName = obj['name'] + ' link google drive'
        self.fileSize = getlinks.sizeof_file(int(obj['size']), suffix='B')
        self.fileExtension = obj['fileExtension']
        self.createdDate = obj['createdTime'].split('T')[0]
        return super(FileObject, self).save(*args, **kwargs)


class SubscribeList(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True)
    userID = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    fileID = models.ForeignKey(FileObject, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title
