
---

```markdown
# 🧠 Obsidian → Google Drive Sync (with WhatsApp Notifications)

This Python automation script synchronizes your **local Obsidian vault** to **Google Drive**, preserving folder structure and updating only changed files.  
After each run, it sends a **WhatsApp notification** via **Twilio API** with sync results (added, updated, unchanged files).

---

## 🚀 Features

- ✅ Syncs your entire Obsidian vault (including subfolders) to Google Drive  
- ✅ Creates missing folders automatically  
- ✅ Uploads new files and updates changed ones (using MD5 checksum comparison)  
- ✅ Skips unchanged files to minimize API calls  
- ✅ Sends WhatsApp notifications (Twilio API) when sync starts and finishes  
- ✅ Supports file types: `.md`, `.pdf`, `.png`, `.jpg`  
- ✅ Secure Google OAuth2 authentication with token caching  

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
├── token.json                  # Auto-generated after first run
├── .env                        # Stores Twilio secrets
└── README.md                   # Documentation (this file)

````

---

## ⚙️ Prerequisites

### 1. Python & Dependencies

Install dependencies:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client twilio python-dotenv
````

---

### 2. Google Drive API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or use an existing one).
3. Enable **Google Drive API**.
4. Go to **APIs & Services → Credentials → Create Credentials → OAuth Client ID**.
5. Choose **Desktop App**, and download the `credentials.json` file.
6. Place `credentials.json` in the same folder as the script.

> 🧠 On the first run, a browser window will open to authenticate your Google account.
> This will generate and save a `token.json` for future use.

---

### 3. Twilio API Setup (for WhatsApp)

1. Log in to your [Twilio Console](https://www.twilio.com/console).
2. Activate the **WhatsApp Sandbox**.
3. Note your **Account SID**, **Auth Token**, and **Twilio Sandbox Number** (usually `whatsapp:+14155238886`).
4. Verify your personal WhatsApp number in the Sandbox.
5. Create a `.env` file in your project root:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=whatsapp:+3816XXXXXXX  # Your verified WhatsApp number
```

---

## 🧠 How It Works

### 🔐 Authentication

* Uses Google OAuth2 to connect to your Drive account.
* Saves `token.json` for subsequent runs (so you only log in once).

### 🔄 Sync Logic

1. Walks through your local Obsidian vault recursively.
2. For each file:

   * Checks if it already exists in Drive.
   * Compares MD5 checksum to detect changes.
   * Uploads new or modified files.
3. Skips hidden and unsupported files.

### 💬 Notifications

* Sends a WhatsApp message before the sync starts and after it completes.
* Example notification:

```
✅ Obsidian sync finished!
🆕 Added: 3
🔁 Updated: 5
👌 Unchanged: 24
```

---

## ⚙️ Configuration

In `obsidian_drive_sync.py`, configure the following constants:

```python
# Local Obsidian vault folder path
VAULT_PATH = r"C:\Users\path-to-your-obsidian-vault"

# Target Google Drive folder ID
DRIVE_FOLDER_ID = "google-drive-folder-id"
```

To find your Drive Folder ID:

1. Open your desired folder in Google Drive.
2. The URL will look like:
   `https://drive.google.com/drive/folders/1k2Fzvi0SnKk8G4k-M8nOj_csXFi6wCJo`
3. The part after `/folders/` is your **Drive Folder ID**.

---

## 🧪 Running the Script

From the terminal:

```bash
python obsidian_drive_sync.py
```

Expected output:

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

| Issue                                       | Possible Cause                             | Solution                                           |
| ------------------------------------------- | ------------------------------------------ | -------------------------------------------------- |
| `google.auth.exceptions.RefreshError`       | Expired or invalid token                   | Delete `token.json` and re-run the script          |
| `TwilioRestException: Authentication Error` | Invalid SID or Auth Token                  | Check `.env` credentials                           |
| Files not uploading                         | Invalid or missing `DRIVE_FOLDER_ID`       | Verify the Drive folder ID and permissions         |
| Hidden/system files being uploaded          | `.obsidian` or `.git` folders not excluded | Script already skips hidden folders — verify paths |

---

## 🧱 Future Enhancements

* [ ] Bi-directional sync (Drive → Local)
* [ ] Automated scheduling (Windows Task Scheduler or CRON)
* [ ] Enhanced logging with timestamps
* [ ] Optional email or Discord notifications
* [ ] Configurable file extensions and ignore patterns

---

## 👤 Author

**Luka Janković**
*FullStack .NET & Angular Software Engineer*
🔗 [LinkedIn Profile](https://www.linkedin.com/in/jankovicluka/)
🏗 Focused on automation, cloud integration, and productivity tooling.

---

## 🪪 License

MIT License © 2025 Luka Janković
Use freely. Modify responsibly.