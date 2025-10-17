# scripts/check_update.py
import os
import sys
import requests
import base64
import importlib
import subprocess

# ---------------- Project Root ----------------
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# ---------------- Config ----------------
from data import config
importlib.reload(config)  # reload to get latest version
CURRENT_VERSION = config.version
GITHUB_TOKEN = getattr(config, "GITHUB_TOKEN", "")

OWNER = "Bongolinarina"
REPO = "AuraRPG"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

# ---------------- Files to Update ----------------
FILES_TO_UPDATE = [
    "scripts/main.py",
    "scripts/check_update.py",
    "data/config.py",
    "game/__init__.py",
    "game/commands.py",
    # Add more files as needed
]

# ---------------- Download ----------------
def download_file(filepath):
    """Download a single file from GitHub and overwrite local copy."""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{filepath}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to download {filepath}: {response.status_code}")
        return False

    content = response.json().get("content")
    if content is None:
        print(f"No content found for {filepath}")
        return False

    decoded = base64.b64decode(content)

    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(filepath, "wb") as f:
        f.write(decoded)
    print(f"Updated {filepath}")
    return True

# ---------------- Restart Game ----------------
def restart_game():
    """Restart the game in a new window and exit the current process."""
    print("Restarting game to apply updates...")
    python_exe = sys.executable
    script_path = os.path.abspath(sys.argv[0])

    if os.name == "nt":  # Windows
        subprocess.Popen(f'start "" "{python_exe}" "{script_path}"', shell=True)
    else:
        subprocess.Popen([python_exe, script_path])

    sys.exit()  # Exit current process

# ---------------- Update ----------------
def update_game():
    """Download all tracked files from GitHub and restart the game."""
    print("Updating game files from GitHub...")
    success = True

    for file in FILES_TO_UPDATE:
        if not download_file(file):
            success = False

    if success:
        print("All files updated successfully!")
        restart_game()
    else:
        print("Some files failed to update. Check your token/repo permissions.")

# ---------------- Check for Update ----------------
def get_latest_version():
    """Return the latest tag from GitHub repo."""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/tags"
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
        tags = response.json()
        if not tags:
            return None
        return tags[0]["name"]  # latest tag
    except Exception as e:
        print(f"[Update check failed] {e}")
        return None

def check_for_update():
    """Check GitHub for a newer version and optionally update."""
    latest = get_latest_version()
    if latest is None:
        print("No tags found on GitHub.")
        return

    print(f"Latest GitHub version: {latest}")
    print(f"Your current version: {CURRENT_VERSION}")

    if latest != CURRENT_VERSION:
        choice = input(f"A new version is available ({latest}). Update? [y/N]: ").lower()
        if choice == "y":
            update_game()
        else:
            print("Skipping update.")
    else:
        print("You are running the latest version.")

# ---------------- Main ----------------
if __name__ == "__main__":
    check_for_update()
