import requests, zipfile, io, os, shutil, sys
from data.config import version as current_version

GITHUB_USER = "Bongolinarina"
GITHUB_REPO = "AuraRPG"
PLAYER_DATA_FILE = "data/player_data.txt"
RUN_BAT = "run_game.bat"  # Path to your batch launcher

def download_latest_version():
    url = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/archive/refs/heads/main.zip"
    try:
        print("Downloading latest version...")
        r = requests.get(url, stream=True)
        r.raise_for_status()
        z = zipfile.ZipFile(io.BytesIO(r.content))
        return z
    except Exception as e:
        print(f"Download failed: {e}")
        return None

def update_game():
    z = download_latest_version()
    if not z:
        return

    print("Extracting and updating files...")
    temp_dir = "temp_update"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    z.extractall(temp_dir)

    # The zip usually extracts into a folder like AuraRPG-main
    extracted_folder = os.path.join(temp_dir, os.listdir(temp_dir)[0])

    # Backup player data
    backup_data = None
    if os.path.exists(PLAYER_DATA_FILE):
        with open(PLAYER_DATA_FILE, "r") as f:
            backup_data = f.read()

    # Copy all files to the project folder
    for root, dirs, files in os.walk(extracted_folder):
        rel_path = os.path.relpath(root, extracted_folder)
        target_dir = os.path.join(".", rel_path)
        os.makedirs(target_dir, exist_ok=True)
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_dir, file)
            if dst_file != PLAYER_DATA_FILE:  # Don't overwrite player data
                shutil.copy2(src_file, dst_file)

    # Restore player data
    if backup_data:
        with open(PLAYER_DATA_FILE, "w") as f:
            f.write(backup_data)

    shutil.rmtree(temp_dir)
    print("Update complete!")

    # Launch game via run_game.bat in a new CMD window
    bat_path = os.path.abspath(RUN_BAT)
    if os.path.exists(bat_path):
        print("Restarting game in a new CMD window...")
        os.system(f'start "" "{bat_path}"')
    else:
        print(f"Batch launcher {RUN_BAT} not found. Please run main.py manually.")

    # Exit current Python process
    sys.exit()

# Run if script called directly
if __name__ == "__main__":
    update_game()
