import re


def extract_files_id(links, drive):
    # copy of google drive file from google drive link :
    links = re.findall(r"\b(?:https?:\/\/)?(?:drive\.google\.com[-_&?=a-zA-Z\/\d]+)",
                       links)  # extract google drive links
    try:
        fileIDs = [re.search(r"(?<=/d/|id=|rs/).+?(?=/|$)", link)[0] for link in links]  # extract the fileIDs
        for fileID in fileIDs:
            if drive.auth.service.files().get(fileId=fileID).execute()[
                'mimeType'] == "application/vnd.google-apps.folder":
                fileIDs.extend(extract_file_ids_from_folder(drive, fileID))
                fileIDs.remove(fileID)
        return fileIDs
    except Exception as error:
        print("error : " + str(error))
        print("Link is probably invalid")
        print(links)