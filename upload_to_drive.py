import os
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Full Drive access
SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_drive_service():
    creds = None
    credentials_file = Path("~/.config/google/client_secret_34595354078-haa1uabkevdrc8s8di26cc2sagbf9np7.apps.googleusercontent.com.json").expanduser()
    token_file = Path(
        "~/.config/google/token.json").expanduser()
    # Load existing token
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(
            token_file,
            SCOPES
        )

    # If no valid credentials, log in
    if not creds or not creds.valid:

        # Refresh expired token
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # First login
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file,
                SCOPES
            )

            creds = flow.run_local_server(port=51903, open_browser=False)

        # Save token
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return build("drive", "v3", credentials=creds)


def upload_large_file(file_path, folder_id=None):
    service = get_drive_service()

    metadata = {
        "name": os.path.basename(file_path)
    }

    if folder_id:
        metadata["parents"] = [folder_id]

    media = MediaFileUpload(
        file_path,
        resumable=True,
        chunksize=5 * 1024 * 1024
    )

    request = service.files().create(
        body=metadata,
        media_body=media,
        fields="id"
    )

    response = None

    print("Uploading...")

    while response is None:
        status, response = request.next_chunk()

        if status:
            print(f"{status.progress() * 100:.1f}%")

    print("Upload complete.")
    print("File ID:", response["id"])

    return response["id"]


def find_file(service, file_name, folder_id=None):
    # Escape single quotes for the Drive query language
    escaped_name = file_name.replace("'", "\\'")

    query = f"name = '{escaped_name}' and trashed = false"

    if folder_id:
        query += f" and '{folder_id}' in parents"

    results = (
        service.files()
        .list(
            q=query,
            fields="files(id, name)",
            pageSize=1,
        )
        .execute()
    )

    files = results.get("files", [])
    return files[0] if files else None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    upload_large_file(
        args.filename,
        folder_id="1tUBSUWxCqBy8Hnaq-T7_2WtE9C_s1mah"
    )