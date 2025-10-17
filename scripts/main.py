import os
import sys

# ----------------- Ensure CMD -----------------
def ensure_cmd():
    shell = os.environ.get("COMSPEC", "")
    if "cmd.exe" not in shell.lower():
        bat_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "run_game.bat"))
        print("[DEBUG] Launching game in a real CMD window...")
        if os.path.exists(bat_path):
            os.system(f'start "" "{bat_path}"')
        else:
            print(f"[DEBUG] ERROR: run_game.bat not found at {bat_path}")
        sys.exit()

ensure_cmd()  # first thing

# ----------------- Update Check -----------------
from check_update import check_for_update
check_for_update()

# ----------------- Game Logic -----------------
from game import *
check_files()

level = get_value("plrLvl")
name = get_value("plrName")

if not name:
    name = input("Enter your character's name: ")
    save("plrName", name)

print(f"Name: {name}\nLevel: {level}")
