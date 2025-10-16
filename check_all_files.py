from check.templates import commands_template, init_template, main_template
from check.check_files import ensure_file, check_player_data
import os

def run_all_checks():
    os.makedirs("game", exist_ok=True)
    ensure_file("game/commands.py", commands_template)
    ensure_file("game/__init__.py", init_template)
    ensure_file("main.py", main_template)
    check_player_data()
    print("All files and folders checked!")

if __name__ == "__main__":
    run_all_checks()
