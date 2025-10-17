import requests
from data.config import version as current_version
from auto_update import update_game

# === Replace this with your repo info ===
GITHUB_USER = "Bongolinarina"
GITHUB_REPO = "AuraRPG"

def get_latest_version():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/tags"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        tags = response.json()
        if not tags:
            return None
        return tags[0]["name"]  # latest tag
    except Exception as e:
        print(f"[Update check failed] {e}")
        return None

def check_for_update():
    latest = get_latest_version()
    if latest and latest != current_version:
        print(f"\nA new version is available: {latest}")
        choice = input("Do you want to update now? (y/n): ").lower()
        if choice == "y":
            update_game()
        else:
            print("Continuing with current version...")
    else:
        print("You are running the latest version.")

# Run this when called directly
if __name__ == "__main__":
    check_for_update()