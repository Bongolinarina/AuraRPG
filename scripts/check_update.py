import os
import sys
import requests
import zipfile
import io
import shutil
import subprocess
import time

# ---------------- Config ----------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data import config
import importlib
importlib.reload(config)

CURRENT_VERSION = config.version

OWNER = "Bongolinarina"
REPO = "AuraRPG"

# Files to update (relative paths in repo)
FILES_TO_UPDATE = [
    "scripts/main.py",
    "data/config.py",
    "game/__init__.py",
    "game/commands.py",
    # Add more files if needed
]

# ---------------- Download ----------------
def download_latest_zip():
    url = f"https://github.com/{OWNER}/{REPO}/archive/refs/heads/main.zip"
    try:
        print("[DEBUG] Downloading latest version...")
        r = requests.get(url, stream=True)
        r.raise_for_status()
        return zipfile.ZipFile(io.BytesIO(r.content))
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        return None

def apply_update():
    z = download_latest_zip()
    if not z:
        return False

    temp_dir = os.path.join(os.path.dirname(__file__), "temp_update")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    z.extractall(temp_dir)
    extracted_folder = os.path.join(temp_dir, os.listdir(temp_dir)[0])

    # Backup player data
    player_file = os.path.join(os.path.dirname(__file__), "..", "data", "player_data.txt")
    backup_data = None
    if os.path.exists(player_file):
        with open(player_file, "r") as f:
            backup_data = f.read()

    # Copy files
    for root, dirs, files in os.walk(extracted_folder):
        rel_path = os.path.relpath(root, extracted_folder)
        target_dir = os.path.join(os.path.dirname(__file__), "..", rel_path)
        os.makedirs(target_dir, exist_ok=True)
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_dir, file)
            if dst_file != player_file:  # do not overwrite player data
                shutil.copy2(src_file, dst_file)

    # Restore player data
    if backup_data:
        with open(player_file, "w") as f:
            f.write(backup_data)

    shutil.rmtree(temp_dir)
    print("[DEBUG] Update applied successfully!")
    return True

# ---------------- Restart Game ----------------
def restart_game_in_new_window():
    """Launch main.py in a new CMD window and exit this one."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    main_path = os.path.join(project_root, "scripts", "main.py")

    if not os.path.exists(main_path):
        print("[ERROR] main.py not found!")
        sys.exit()

    main_path_quoted = f'"{main_path}"'
    print("[DEBUG] Launching updated game in a new CMD window...")
    subprocess.Popen(f'start "" python {main_path_quoted}', shell=True)
    time.sleep(0.5)
    print("[DEBUG] Closing this window...")
    sys.exit()

# ---------------- Check for Update ----------------
def get_latest_version():
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
    latest = get_latest_version()
    if not latest:
        print("[DEBUG] No tags found on GitHub.")
        return

    print(f"[DEBUG] Latest GitHub version: {latest}")
    print(f"[DEBUG] Your current version: {CURRENT_VERSION}")

    if latest != CURRENT_VERSION:
        choice = input(f"A new version is available ({latest}). Update? [y/N]: ").lower()
        if choice == "y":
            success = apply_update()
            if success:
                restart_game_in_new_window()
            else:
                print("[ERROR] Update failed. Continuing with current version.")
        else:
            print("Skipping update.")
    else:
        print("You are running the latest version.")

# ---------------- Run if called directly ----------------
if __name__ == "__main__":
    check_for_update()
