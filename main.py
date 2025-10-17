from check_update import check_for_update

# Run update check first
check_for_update()

# Rest of your game
from game import *
check_files()

level = get_value("plrLvl")
name = get_value("plrName")

if name is None or name == "":
    name = input("Enter your character's name: ")
    save("plrName", name)

print(f"Name: {name}\nLevel: {level}")