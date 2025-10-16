from game import *

check_files()

level = get_value("plrLvl")
name = get_value("plrName")

if name is None or name == "":
    name = input("Enter your characters name: ")
    save("plrName", name)

print(f"Name: {name}\nLevel: {level}")
