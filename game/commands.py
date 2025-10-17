# commands.py - auto-created starter file
import os
import sys
import psutil
import subprocess

def get_value(data):
    try:
        with open("data/player_data.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith(data):
                    value = line.split("=")[1].strip()
                    if value.startswith('"') and value.endswith('"'):
                        return value[1:-1]
                    try:
                        return int(value)
                    except ValueError:
                        return value
    except FileNotFoundError:
        return None

def save(var, data):
    filepath = "data/player_data.txt"
    lines = []
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        pass
    found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{var} ="):
            if isinstance(data, str):
                lines[i] = f'{var} = "{data}"\n'
            else:
                lines[i] = f"{var} = {data}\n"
            found = True
            break
    if not found:
        if isinstance(data, str):
            lines.append(f'{var} = "{data}"\n')
        else:
            lines.append(f"{var} = {data}\n")
    with open(filepath, "w") as file:
        file.writelines(lines)

def check_files():
    os.makedirs("data", exist_ok=True)
    player_file = "data/player_data.txt"
    if not os.path.exists(player_file):
        with open(player_file, "w") as f:
            f.write('plrName = ""\n')
            f.write('plrLvl = 1\n')
            f.write('plrXP = 0\n')
            f.write('plrCoins = 0\n')
            f.write('plrHP = 100\n')
            f.write('plrMaxHP = 100\n')
            f.write('plrRebirth = 0\n')
            f.write('inventory = {"Wood":0, "Stone":0}\n')
        print("player_data.txt created with default values.")
