from twilio.rest import Client
from dotenv import load_dotenv
import os
import hashlib
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Local files for auth caching
CREDENTIALS_FILE = 'credentials.json'  # downloaded from Google Cloud Console
TOKEN_FILE = 'token.json'              # saved after first login

def authenticate():
    """
    Handles Google OAuth flow:
    - Reads credentials.json (client secrets)
    - Opens browser on first run for login
    - Stores token.json for future runs
    """
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)


def md5sum(file_path):
    """Calculate MD5 hash of a file to detect changes."""
    h = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def upload_file(service, local_path, drive_folder_id):
    """
    Uploads or updates a single file to Google Drive.
    - If file exists and is unchanged, skip
    - Otherwise upload or replace
    """
    filename = os.path.basename(local_path)
    local_md5 = md5sum(local_path)

    # Find if the file already exists
    query = f"name = '{filename}' and '{drive_folder_id}' in parents and trashed=false"
    result = service.files().list(q=query, fields="files(id, name, md5Checksum)").execute()
    files = result.get('files', [])

    media = MediaFileUpload(local_path, resumable=True)

    if files:
        drive_file = files[0]
        if drive_file.get('md5Checksum') == local_md5:
            print(f"✅ Skipped (unchanged): {filename}")
            return 'unchanged'
        print(f"🔁 Updating file: {filename}")
        service.files().update(fileId=drive_file['id'], media_body=media).execute()
        return 'updated'
    else:
        print(f"⬆️ Uploading new file: {filename}")
        service.files().create(
            body={'name': filename, 'parents': [drive_folder_id]},
            media_body=media,
            fields='id'
        ).execute()
        return 'added'


def get_or_create_drive_folder(service, parent_id, folder_name):
    """Get the Drive folder ID for folder_name under parent_id, or create it if it doesn't exist."""
    query = f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_name}' and '{parent_id}' in parents and trashed=false"
    result = service.files().list(q=query, fields="files(id, name)").execute()
    folders = result.get('files', [])
    if folders:
        return folders[0]['id']
    # Create folder
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    print(f"📁 Created folder: {folder_name}")
    return folder['id']


def sync_vault(service, vault_path, drive_folder_id):
    """
    Walks through your Obsidian vault and syncs all non-hidden files.
    """
    allowed_exts = {'.md', '.pdf', '.png', '.jpg'}
    folder_cache = {vault_path: drive_folder_id}
    stats = {'added': 0, 'updated': 0, 'unchanged': 0}
    for root, dirs, files in os.walk(vault_path):
        # Skip folders that start with '.'
        rel_path = os.path.relpath(root, vault_path)
        if any(part.startswith('.') for part in rel_path.split(os.sep) if part != '.'):
            continue
        # Skip root folder
        if rel_path == '.':
            current_drive_folder_id = drive_folder_id
        else:
            # Traverse and create folders as needed
            parts = rel_path.split(os.sep)
            parent_id = drive_folder_id
            for part in parts:
                folder_key = os.path.join(vault_path, *parts[:parts.index(part)+1])
                if folder_key in folder_cache:
                    parent_id = folder_cache[folder_key]
                else:
                    parent_id = get_or_create_drive_folder(service, parent_id, part)
                    folder_cache[folder_key] = parent_id
            current_drive_folder_id = parent_id
        for file in files:
            if file.startswith('.'):
                continue  # skip hidden or system files
            ext = os.path.splitext(file)[1].lower()
            if ext not in allowed_exts:
                continue  # skip files not in allowed extensions
            local_file = os.path.join(root, file)
            result = upload_file(service, local_file, current_drive_folder_id)
            if result in stats:
                stats[result] += 1
    return stats

def send_whatsapp_message(body):
    """
    Send a WhatsApp message using Twilio API.
    Fill in your Twilio credentials and WhatsApp numbers below.
    """
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    from_whatsapp_number = 'whatsapp:+14155238886'  # Twilio sandbox number
    to_whatsapp_number = os.getenv('TWILIO_PHONE_NUMBER')
    message = client.messages.create(
        body=body,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )
    print(f"WhatsApp message sent: {body}")


if __name__ == "__main__":
    # 1. Authenticate with Google
    service = authenticate()

    # 2. Set your local Obsidian vault folder path (change this!)
    VAULT_PATH = r"C:\Users\luka.jankovic\Opsidian Notes\Opsidian"

    # 3. Set your Google Drive folder ID (copy from Drive URL)
    DRIVE_FOLDER_ID = "1k2Fzvi0SnKk8G4k-M8nOj_csXFi6wCJo"

    # 4. Sync all files
    send_whatsapp_message("Obsidian sync started.")
    print("🔄 Starting sync...")
    stats = sync_vault(service, VAULT_PATH, DRIVE_FOLDER_ID)
    print("✅ Sync complete.")
    summary = (
        f"✅ Obsidian sync finished!\n"
        f"🆕 Added: {stats['added']}\n"
        f"🔁 Updated: {stats['updated']}\n"
        f"👌 Unchanged: {stats['unchanged']}"
    )
    send_whatsapp_message(summary)