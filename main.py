import os
import sys

# ----------------- Ensure CMD -----------------
def ensure_cmd():
    # If not running in a real terminal (like VS Code)
    if not sys.stdin.isatty():
        bat_path = os.path.abspath("run_game.bat")
        print("Launching game in a real CMD window...")
        os.system(f'start "" "{bat_path}"')
        sys.exit()  # Stop the current Python instance

ensure_cmd()  # Call this first

# ----------------- Update Check -----------------
from check_update import check_for_update
check_for_update()

# ----------------- Game Logic -----------------
from game import *
check_files()

level = get_value("plrLvl")
name = get_value("plrName")

if name is None or name == "":
    name = input("Enter your character's name: ")
    save("plrName", name)

print(f"Name: {name}\nLevel: {level}")