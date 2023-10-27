import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.http import MediaIoBaseDownload


# Define the Google Drive API scopes and service account file path
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "app/gdrive_key.json"

# Create credentials using the service account file
file_location = "app/Optimum_Malignant_cases_with_prescreen.xlsx"
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def upload_file(file_location, credentials):
    # create drive api client
    service = build('drive', 'v3', credentials=credentials)
        
    file_metadata = {'name': 'Excel Report','mimeType': 'application/vnd.google-apps.spreadsheet'}
    media = MediaFileUpload(file_location, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',resumable=True)
    file = service.files().create(body=file_metadata, media_body=media,fields='id').execute()
    print(file.get('id'))
    return None

def check_files(credentials):
    service = build('drive', 'v3', credentials=credentials)
    # Call the Drive v3 API
    results = service.files().list().execute()
    # get the results
    items = results.get('files', [])
    print(items)
    return None
    
def del_file(file_id, credentials):
    service = build('drive', 'v3', credentials=credentials)
    service.files().delete(fileId=file_id).execute()
    return None

def download_file(real_file_id, file_out, credentials):

    # create drive api client
    service = build('drive', 'v3', credentials=credentials)
    file_id = real_file_id

    # pylint: disable=maybe-no-member
    request = service.files().export_media(fileId=file_id,
                                               mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(F'Download {int(status.progress() * 100)}.')
    file_retrieved: str = file.getvalue()
    with open(file_out, 'wb') as f:
        f.write(file_retrieved)
    return None

 
#upload_file(file_location, credentials)
#check_files(credentials)
#del_file("1S5r5nLXtDJLNPnAIRFtS_U2QIjECyZgGJhvUPowqQ3Y", credentials)

download_file("1ICIZSnY3O_zSU6aMHfcti2D7Yu5d2Rf52lm93CKD36g", "app/output.xlsx", credentials)


