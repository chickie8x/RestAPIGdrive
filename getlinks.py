from __future__ import print_function

import os.path
import pickle
import re

from django.core.validators import URLValidator
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.pickle.

SCOPES = ['https://www.googleapis.com/auth/drive']
DES_PATH = os.getcwd() + "/"
folderId ='1Aj4-D82_EqtJFz92Z3ynZcHkXG2wBm9h'

def get_Gdrive_folder_id(drive, driveService, name, parent="root"):  # return ID of folder, create it if missing
    body = {'title': name,
            'mimeType': "application/vnd.google-apps.folder"
            }
    query = "title='Temp folder for script' and mimeType='application/vnd.google-apps.folder'" \
            " and '" + parent + "' in parents and trashed=false"
    if parent != "root":
        query += "and driveId='" + parent + "' and includeItemsFromAllDrives=true and supportsAllDrives = true"
    listFolders = drive.ListFile({'q': query})
    for subList in listFolders:
        if subList == []:  # if folder doesn't exist, create it
            folder = driveService.files().insert(body=body).execute()
            break
        else:
            folder = subList[0]  # if one folder with the correct name exist, pick it

    return folder['id']


def extract_file_ids_from_folder(drive, folderID):
    files = drive.ListFile({'q': "'" + folderID + "' in parents"}).GetList()
    fileIDs = []
    for file in files:
        fileIDs.append(file['id'])
    return fileIDs


def extract_files_id(link):
    if not 'view' in link:
        id = link[33:]
    else:
        id = re.search("file/d/(.*)/views?",link).group(1)
    return id
    # copy of google drive file from google drive link :
    # links = re.findall(r"\b(?:https?:\/\/)?(?:drive\.google\.com[-_&?=a-zA-Z\/\d]+)",
    #                    links)  # extract google drive links
    # try:
    #     fileIDs = [re.search(r"(?<=/d/|id=|rs/).+?(?=/|$)", link)[0] for link in links]  # extract the fileIDs
    #     for fileID in fileIDs:
    #         if drive.files().get(fileId=fileID).execute()[
    #             'mimeType'] == "application/vnd.google-apps.folder":
    #             fileIDs.extend(extract_file_ids_from_folder(drive, fileID))
    #             fileIDs.remove(fileID)
    #     return fileIDs
    # except Exception as error:
    #     print("error : " + str(error))
    #     print("Link is probably invalid")
    #     print(links)


# def copy_file(drive, fileId, copy_title):
#     copied_file = {'title': copy_title}
#     try:
#         return drive.files().copy(fileId=fileId, body=copied_file).execute()
#     except :
#         print('An error occurred')
#     return None


def fileClone(drive, fileId):
    file = drive.files().copy(fileId=fileId, fields='*', supportsAllDrives=True).execute()
    drive.files().update(
        fileId=file['id'],
        addParents=folderId,
        removeParents=file['parents'][0],
        fields='id,parents',
    ).execute()
    return file


def delete_file(drive, id):
    drive.auth.service.files().delete(fileId=id).execute()


def getCreds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def getFile(link,drive):
    if not 'view' in link:
        id = link[33:]
        file = drive.files().copy(fileId=id ,fields ='*').execute()
        drive.files().update(
            fileId=file['id'],
            addParents=folderId,
            removeParents=file['parents'][0],
            fields='id,parents'
        ).execute()
        return file
    else:
        id = re.search("file/d/(.*)/views?",link).group(1)
        file = drive.files().copy(fileId=id, fields='*').execute()
        drive.files().update(
            fileId=file['id'],
            addParents=folderId,
            removeParents=file['parents'][0],
            fields='id,parents'
        ).execute()
        return file


def fileInfo(drive,fileId):
    file = drive.files().get(fileId=fileId, fields='*', supportsAllDrives=True).execute()
    return file


def sizeof_file(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def checkurl(url):
    validator = URLValidator()
    try:
        validator(url)
        return True
    except:
        return False


def main():
    creds = getCreds()


if __name__ == '__main__':
    main()
