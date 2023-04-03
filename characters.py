import json
import os
import pandas as pd

"""
**Groupings**
- Main
- Aunty Mai's
- HQ
- SPD
- Paractivists
- Hikosen
- Wipers
- Soma Mafia
- Others
"""

if os.path.isfile('characters.json'):
    with open('characters.json', 'r') as f:
        characters = json.load(f)
else:
    characters = {}

groupings = {"Main", "Syurga's Most Wanted", "Aunty Mai's", "HQ", "SPD", "Hikosen", "Paractivists", "Wipers", "Soma Mafia", "Others"}

y_n = {"yes", "no"}


def add_character():
    global characters
    global groupings
    global y_n
    name = input("Enter character name (make sure that it is at least 1 word): ")
    while not name.strip():
        name = input("Please enter a valid name for the character: ")
    age = input("Enter character age (make sure that it's a number): ")
    while not age.isdigit():
        age = input("Please enter a valid age for the character: ")
    tagline = input("Enter character tagline (make sure that it's a phrase): ")
    while not tagline.strip():
        tagline = input("Please enter a valid tagline for the character: ")
    type_char = input("Enter type of character (make sure that it's within the groupings): ")
    while type_char not in groupings:
        type_char = input("Please enter a valid character type: ")
    title = input("Enter character title (The <Adjective> <Noun> Format): ")
    while not title.strip() or len(title.split()) != 3 or not title.startswith("The"):
        title = input("Please enter a valid title for the character (The <Adjective> <Noun> Format): ")
    birthday = input("Enter character birthday (MM/DD format): ")
    while not (len(birthday) == 5 and birthday[2] == '/' and birthday[:2].isdigit() and birthday[3:].isdigit()):
        birthday = input("Please enter a valid birthday for the character (MM/DD format): ")
    height = input("Enter character height (ft\"inches format): ")
    while not height or not any(char.isdigit() for char in height):
        height = input("Please enter a valid height for the character (ft\"inches format): ")
    hair = input("Enter character hair color (Color, and dye if applicable): ")
    while not hair.strip():
        hair = input("Please enter a valid hair color for the character: ")
    eyes = input("Enter character eye color (Color, multiple allowed): ")
    while not eyes.strip():
        eyes = input("Please enter a valid eye color for the character: ")
    tattoos = input("Does the character have tattoos? (Yes/No): ")
    while tattoos.lower() not in y_n:
        tattoos = input("Please enter a valid response (Yes/No): ")
    ethnicity = input("Enter character ethnicity (optional, leave blank if not applicable): ")
    traits = []
    while len(traits) < 4:
        trait = input(f"Enter defining trait {len(traits) + 1} (leave blank to stop): ")
        if not trait:
            break
        traits.append(trait)
    based_in = input("Enter character based in (optional, leave blank if not applicable): ")
    blurb = input("Enter character blurb (at least 2 sentences): ")
    while len(blurb.split('.')) < 2:
        blurb = input("Please enter a valid blurb for the character (at least 2 sentences): ")
    hidden = input("Do you want to hide this character? (Yes/No): ")
    while hidden.lower() not in y_n:
        hidden = input("Please enter a valid response (Yes/No): ")

    character = {
        'name': name,
        'age': age,
        'tagline': tagline,
        'type_char': type_char,
        'title': title,
        'birthday': birthday,
        'height': height,
        'hair': hair,
        'eyes': eyes,
        'tattoos': tattoos,
        'blurb': blurb,
        'hidden': hidden
    }

    if ethnicity:
        character['ethnicity'] = ethnicity

    if traits:
        character['defining_traits'] = traits

    if based_in:
        character['based_in'] = based_in

    first_name = name.split(' ')[0].lower()
    full_name = first_name
    if first_name in characters:
        while True:
            # prompt the user for the full name of the character
            print(
                f"A character with the first name {first_name} already exists. Please enter the full name of the "
                f"character you want to add:")
            full_name = input().lower().replace(' ', '_')
            if full_name in characters:
                # return
                break

    characters[full_name] = character

    with open('characters.json', 'w') as f:
        json.dump(characters, f, indent=4)

    print(f"{name} added to characters dictionary.")

    group_chars()


def delete_character():
    global characters
    # get available characters
    print("Characters:")
    char_set = set()
    print(characters.keys())
    for c in characters.keys():
        c_name = characters[c]['name']
        print("- ", c_name)
        char_set.add(c_name)
    char = input("Which character would you like to delete? Enter C to cancel.")
    # if character is in characters, delete it. If not, say that the character is invalid. Else, ask if they want to
    # cancel.
    if char.lower() == "c":
        print("Character deletion cancelled.")
    elif char not in char_set:
        print("Character not in list of available characters. Try again!")
    else:
        keys_to_delete = []
        for k, v in characters.items():
            if v['name'] == char:
                keys_to_delete.append(k)
        for k in keys_to_delete:
            del characters[k]
            print(char + " deleted from characters")
        with open('characters.json', 'w') as f:
            json.dump(characters, f, indent=4)


def group_chars():
    df = pd.read_json("characters.json").transpose()
    grouped_indices = df.groupby('type_char').groups
    new_df = pd.DataFrame()
    type_order = ["Main", "Syurga\'s Most Wanted", "Aunty Mai\'s", "HQ", "SPD", "Hikosen", "Paractivists", "Wipers", "Soma Mafia", "Others"]
    for char_type in type_order:
        if char_type in grouped_indices:
            for char in grouped_indices[char_type]:
                new_df = pd.concat([new_df, df.loc[char]], axis=1)
    new_df.to_json("characters.json", indent=4)


def modify():
    for character in characters.values():
        print(character['name'])
        alt_names = []
        while True:
            nickname = input(
                f"Enter a nickname for {character['name']} (or press Enter to move on to the next character): ")
            if not nickname:
                break
            alt_names.append(nickname)
        if "alt_names" in character:
            character["alt_names"].extend(alt_names)
        else:
            character["alt_names"] = alt_names
    with open('characters.json', 'w') as f:
        json.dump(characters, f, indent=4)


def main():
    while True:
        choice = input("Add, Modify, Group, or Delete Character?\nA: Add\nM: Modify\nG: Group\nD: Delete\nE: Exit\n:")
        if choice.lower() == "a":
            add_character()
        elif choice.lower() == "m":
            modify()
            pass
        elif choice.lower() == "g":
            group_chars()
        elif choice.lower() == "d":
            delete_character()
        elif choice.lower() == "e":
            ask_exit = input("Exit? Y/N")
            if ask_exit.lower().startswith("y"):
                break


if __name__ == "__main__":
    main()
