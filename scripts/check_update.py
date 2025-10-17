# check_update.py
import os
import sys
import requests
import zipfile
import io
import shutil
import subprocess

# ---------------- Config ----------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data import config

CURRENT_VERSION = config.version

# ---------------- GitHub Repo ----------------
OWNER = "Bongolinarina"
REPO = "AuraRPG"

# ---------------- Files to update ----------------
FILES_TO_UPDATE = [
    "main.py",
    "data/config.py",
    "game/__init__.py",
    "game/commands.py",
    # Add more files here as needed
]

# ---------------- Helper Functions ----------------
def download_latest_zip():
    """Download latest main branch as zip from GitHub."""
    url = f"https://github.com/{OWNER}/{REPO}/archive/refs/heads/main.zip"
    try:
        print("Downloading latest version from GitHub...")
        r = requests.get(url, stream=True)
        r.raise_for_status()
        return zipfile.ZipFile(io.BytesIO(r.content))
    except Exception as e:
        print(f"Download failed: {e}")
        return None


def restart_game():
    """Restart the game in a new CMD window and close the current one."""
    print("Restarting game to apply updates...")

    # Absolute path to run_game.bat
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    bat_path = os.path.join(project_root, "run_game.bat")

    if os.path.exists(bat_path):
        print(f"[DEBUG] Launching: {bat_path}")

        # Launch the batch in a new CMD window and close the current one
        # /C runs the command then closes this window automatically
        subprocess.Popen(f'start "" cmd /C "{bat_path}"', shell=True)
    else:
        print(f"[ERROR] run_game.bat not found at {bat_path}")

    sys.exit()  # Exit the current Python process

# ---------------- Update ----------------
def update_game():
    """Download all files from GitHub and apply updates."""
    z = download_latest_zip()
    if not z:
        return

    print("Extracting files...")
    temp_dir = "temp_update"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    z.extractall(temp_dir)
    extracted_folder = os.path.join(temp_dir, os.listdir(temp_dir)[0])

    # Backup player data
    player_data = "data/player_data.txt"
    backup_data = None
    if os.path.exists(player_data):
        with open(player_data, "r") as f:
            backup_data = f.read()

    # Copy files over
    for root, dirs, files in os.walk(extracted_folder):
        rel_path = os.path.relpath(root, extracted_folder)
        target_dir = os.path.join(".", rel_path)
        os.makedirs(target_dir, exist_ok=True)
        for file in files:
            dst_file = os.path.join(target_dir, file)
            src_file = os.path.join(root, file)
            if dst_file != player_data:
                shutil.copy2(src_file, dst_file)

    # Restore player data
    if backup_data:
        with open(player_data, "w") as f:
            f.write(backup_data)

    shutil.rmtree(temp_dir)
    print("Update complete!")
    restart_game()

# ---------------- Check for updates ----------------
def get_latest_version():
    """Get latest tag from GitHub."""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/tags"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        tags = r.json()
        if not tags:
            return None
        return tags[0]["name"]
    except Exception as e:
        print(f"[Update check failed] {e}")
        return None

def check_for_update():
    """Check if a new version is available and prompt user."""
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
