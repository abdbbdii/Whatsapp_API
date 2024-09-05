import json

import io
import requests

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from api.appSettings import appSettings


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
    r = requests.get(
        appSettings.utils_server + "service/google_auth/",
        json={"password": appSettings.utils_server_password, "scopes": ["https://www.googleapis.com/auth/drive.readonly"]},
    )
    if r.status_code != 200:
        return None
    appSettings.update('google_creds', json.loads(r.json().get("google_creds")))
    service = build("drive", "v3", credentials=appSettings.google_creds)
    file_id = get_file_id_from_link(gdrive_link)
    file_data = get_file_data(service, file_id)
    return file_data


if __name__ == "__main__":
    link = "https://drive.google.com/file/d/1fWxPcicK0VtgWcBhLp6zerhGPPOSQ-9S/view?usp=drive_web"
    data = download_gdrive_file(link)
    with open("downloaded_file.md", "wb") as f:
        f.write(data)
