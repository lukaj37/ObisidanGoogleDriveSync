# 1. Create a new virtual environment (named .venv)
python -m venv .venv

# 2. Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# 3. Upgrade pip and install Google + watchdog libraries
pip install --upgrade pip
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib watchdog
