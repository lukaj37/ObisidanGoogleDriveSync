```markdown
# 🧠 Obsidian → Google Drive Sync (with WhatsApp Notifications)

This Python automation script synchronizes your **local Obsidian vault** to **Google Drive**, preserving folder structure and updating only changed files.  
After each run, it sends a **WhatsApp notification** via **Twilio API** with sync results (added, updated, unchanged files).

---

## 🚀 Features

✅ Syncs your entire Obsidian vault folder (and subfolders) to Google Drive  
✅ Creates missing folders automatically  
✅ Uploads new files and updates changed ones (using MD5 checksum comparison)  
✅ Skips unchanged files to minimize API calls  
✅ Sends WhatsApp message notifications (Twilio API) when the sync starts and finishes  
✅ Supports multiple file types: `.md`, `.pdf`, `.png`, `.jpg`  
✅ Safe Google OAuth2 authentication with token caching  

---

## 🧩 Tech Stack

| Component | Purpose |
|------------|----------|
| **Python 3.10+** | Core scripting runtime |
| **Google Drive API** | File upload, update, and folder management |
| **Twilio REST API** | Sending WhatsApp notifications |
| **dotenv (.env)** | Secure environment variable management |
| **hashlib (MD5)** | File change detection |
| **os / pathlib** | File system traversal and management |

---

## 📁 Project Structure

```

obsidian_drive_sync/
│
├── obsidian_drive_sync.py      # Main script
├── credentials.json            # Google API credentials (from Google Cloud)
├── token.json                  # Auto-generated on first run
├── .env                        # Stores Twilio secrets
└── README.md                   # You are here

````

---

## ⚙️ Prerequisites

### 1. Python & Dependencies
Install dependencies:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client twilio python-dotenv
````

### 2. Google Drive API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or use an existing one).
3. Enable **Google Drive API**.
4. Go to **APIs & Services → Credentials** → click **Create Credentials → OAuth Client ID**.
5. Choose **Desktop App**, and download the `credentials.json`.
6. Place `credentials.json` in the same folder as the script.

When you run the script for the first time, a browser window will open to authenticate your Google account.
This will generate `token.json` automatically.

---

### 3. Twilio API Setup (for WhatsApp)

1. Sign up or log in at [Twilio Console](https://www.twilio.com/console).
2. Activate **WhatsApp Sandbox**.
3. Note your **Account SID**, **Auth Token**, and **Twilio Sandbox number** (usually `whatsapp:+14155238886`).
4. Verify your own WhatsApp number in the Twilio Sandbox.
5. Create a `.env` file in your project root:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=whatsapp:+3816XXXXXXX  # Your verified WhatsApp number
```

---

## 🧠 How It Works

### Authentication

* Uses Google OAuth2 to connect to your Drive account.
* Saves a token for subsequent runs (so you only log in once).

### Sync Logic

1. Walks through your local Obsidian vault recursively.
2. For each file:

   * Checks if it exists in Drive.
   * Compares MD5 checksum.
   * Uploads new or modified files.
3. Skips hidden or unsupported files.

### Notifications

* Sends a WhatsApp message before sync starts and after it completes.
* Example output:

  ```
  ✅ Obsidian sync finished!
  🆕 Added: 3
  🔁 Updated: 5
  👌 Unchanged: 24
  ```

---

## 🧩 Configuration

In `obsidian_drive_sync.py`, configure these constants:

```python
# Your local Obsidian vault folder path
VAULT_PATH = r"C:\Users\path-to-your-obsidian-vault"

# Your target Google Drive folder ID
DRIVE_FOLDER_ID = "google-drive-folder-id"
```

To find your Drive folder ID:

* Open the folder in Google Drive.
* The URL will look like:
  `https://drive.google.com/drive/folders/1k2Fzvi0SnKk8G4k-M8nOj_csXFi6wCJo`
* The part after `/folders/` is the **Drive Folder ID**.

---

## 🧪 Running the Script

From the terminal:

```bash
python obsidian_drive_sync.py
```

Expected console output:

```
🔄 Starting sync...
⬆️ Uploading new file: daily-notes.md
🔁 Updating file: todo.md
✅ Skipped (unchanged): index.md
✅ Sync complete.
WhatsApp message sent: ✅ Obsidian sync finished!
```

---

## 🧰 Troubleshooting

| Issue                                       | Possible Cause                       | Solution                                                    |
| ------------------------------------------- | ------------------------------------ | ----------------------------------------------------------- |
| `google.auth.exceptions.RefreshError`       | Expired or invalid token             | Delete `token.json` and re-run script to reauthenticate     |
| `TwilioRestException: Authentication Error` | Invalid SID or Auth Token            | Check `.env` and re-run                                     |
| Files not uploading                         | Wrong `DRIVE_FOLDER_ID`              | Verify the folder ID and permissions                        |
| Hidden/system files being uploaded          | Check `.obsidian` and `.git` folders | The script already skips hidden folders — verify your paths |


## 🧱 Future Enhancements

* [ ] Bi-directional sync (Drive → Local)
* [ ] Sync scheduling via Windows Task Scheduler or CRON
* [ ] Enhanced logging with timestamps
* [ ] Optional email or Discord notifications

---

## 🧑‍💻 Author

**Luka Janković**
*FullStack .NET & Angular Software Engineer*
📧 (https://www.linkedin.com/in/jankovicluka/)
🏗 Focused on automation, cloud integration, and productivity tooling.

---
