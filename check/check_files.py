import os
from data.config import *
def ensure_file(path, expected_content):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(expected_content)
        print(f"{path} created.")
        return

    with open(path, "r") as f:
        current_content = f.read()

    if current_content != expected_content:
        with open(path, "w") as f:
            f.write(expected_content)
        print(f"{path} corrected.")
    else:
        print(f"{path} already correct.")

def check_player_data():
    os.makedirs("data", exist_ok=True)
    player_file = "data/player_data.txt"

    required_vars = {
        "plrName": NAME,
        "plrLvl": LVL,
        "plrXP": XP,
        "plrCoins": COINS,
        "plrHP": HP,
        "plrMaxHP": MAXHP,
        "plrRebirth": REBIRTH,
        "inventory": INV
    }

    # Create the file if it doesn't exist
    if not os.path.exists(player_file):
        with open(player_file, "w") as f:
            for key, val in required_vars.items():
                f.write(f"{key}={val}\n")
        print("✅ Created new player_data.txt with default values.")
        return

    # Check for missing keys and fix them
    with open(player_file, "r") as f:
        lines = f.readlines()

    data = {}
    for line in lines:
        if "=" in line:
            key, val = line.strip().split("=", 1)
            data[key] = val

    missing = False
    for key, val in required_vars.items():
        if key not in data:
            data[key] = val
            missing = True

    if missing:
        with open(player_file, "w") as f:
            for key, val in data.items():
                f.write(f"{key}={val}\n")
        print("⚙️ Fixed missing values in player_data.txt")
    else:
        print("✅ player_data.txt is up to date.")

    existing_lines = []
    if os.path.exists(player_file):
        with open(player_file, "r") as f:
            existing_lines = [line.strip() for line in f if line.strip()]

    existing_vars = {}
    for line in existing_lines:
        if '=' in line:
            key, val = line.split('=', 1)
            existing_vars[key.strip()] = val.strip()

    new_lines = existing_lines.copy()
    for var, default in required_vars.items():
        if var not in existing_vars:
            if isinstance(default, str) and not default.startswith('{'):
                new_lines.append(var + ' = "' + default.strip('"') + '"')
            else:
                new_lines.append(f"{var} = {default}")

    with open(player_file, "w") as f:
        f.write("\n".join(new_lines) + "\n")
    print("player_data.txt checked and updated if needed.")