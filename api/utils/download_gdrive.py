import pickle
import io
import base64
import json
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from api.appSettings import appSettings

# load_dotenv(find_dotenv()) if not os.getenv('VERCEL_ENV') else None

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def authenticate():
    """
    Authenticates the user using OAuth2 credentials and returns the credentials object.
    """
    creds = None

    if token := appSettings.token_pickle_base64:
        creds = pickle.loads(base64.b64decode(token))

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(json.loads(appSettings.google_credentials), SCOPES)
            creds = flow.run_local_server(port=0)

        appSettings.update("token_pickle_base64", base64.b64encode(pickle.dumps(creds)).decode("utf-8"))

    print("Authenticated successfully!")
    return creds

def get_file_data(service, file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")
    fh.seek(0)
    return fh.read()

def get_file_id_from_link(link):
    """
    Extract the file ID from a Google Drive link.
    The link format is typically like: https://drive.google.com/file/d/FILE_ID/view?usp=sharing
    """
    return link.split("/d/")[1].split("/")[0]

def download_gdrive_file(gdrive_link):
    """Gets the file data in bytes from Google Drive given its link."""
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

    file_id = get_file_id_from_link(gdrive_link)
    file_data = get_file_data(service, file_id)
    return file_data

# Example usage within another program
if __name__ == "__main__":
    link = "https://drive.google.com/file/d/1fWxPcicK0VtgWcBhLp6zerhGPPOSQ-9S/view?usp=drive_web"
    data = download_gdrive_file(link)
    with open("downloaded_file.md", "wb") as f:
        f.write(data)
