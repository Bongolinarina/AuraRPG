import requests, zipfile, io, os, shutil
from data.config import version as current_version

GITHUB_USER = "Bongolinarina"
GITHUB_REPO = "AuraRPG"

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

    # The zip usually extracts into a folder named like AuraRPG-main
    extracted_folder = os.path.join(temp_dir, os.listdir(temp_dir)[0])

    # Backup player data
    player_data = "data/player_data.txt"
    backup_data = None
    if os.path.exists(player_data):
        with open(player_data, "r") as f:
            backup_data = f.read()

    # Copy all files to the game folder
    for root, dirs, files in os.walk(extracted_folder):
        rel_path = os.path.relpath(root, extracted_folder)
        target_dir = os.path.join(".", rel_path)
        os.makedirs(target_dir, exist_ok=True)
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_dir, file)
            if dst_file != player_data:  # don't overwrite player data
                shutil.copy2(src_file, dst_file)

    # Restore player data
    if backup_data:
        with open(player_data, "w") as f:
            f.write(backup_data)

    shutil.rmtree(temp_dir)
    print("Update complete! Please restart the game.")

# Run if script called directly
if __name__ == "__main__":
    update_game()