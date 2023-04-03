import json
import re

import discord

client = discord.Client(intents=discord.Intents.all())

help_flag = "-help"
info_flag = "-info"

with open('characters.json') as f:
    characters = json.load(f)


@client.event
async def on_message(message):
    if message.content.startswith("!aunty"):
        cmd_args = message.content.split(" ")
        # invalid commands
        if len(cmd_args) <= 1:
            await message.channel.send(
                "You call me? Use `!aunty -h` or `!aunty -help` for a list of available commands.")
        else:
            command, arg_list = cmd_args[1], cmd_args[2:]
            await process_commands(message, command, arg_list)


async def process_commands(message, command, arg_list):
    # help
    if command == help_flag or command == help_flag[:2]:
        await process_help(message, arg_list)
    elif command == info_flag or command == info_flag[:2]:
        await process_info(message, arg_list)
    else:
        await message.channel.send("Don't recognize this command. Use `!aunty -h` or `!aunty -help` for a list of "
                                   "available commands.")


async def process_help(message, arg_list):
    if not arg_list:
        await message.channel.send(
            "Hello! You must be new, or an old face appearing after a long time. I'm Aunty Mai, and I'm here to "
            "help you navigate this discord or the story that my creator made, The Midnight Shift. "
            "In order to use me, use the #bot channel and type the following:\n"
            "`!aunty <command>`\n"
            "I can do the following commands:\n"
            ":coffee: **-h OR -help [channel name]** : Provide info on a specific channel. If [channel name] isn't "
            "provided, this message is the default that'll be seen.\n"
            ":coffee: **-i OR -info [character]** : Provides info on a character if provided. If [character] isn't "
            "provided, the series' description is printed by default.\n**Type \"characters\" (no quotes) instead of "
            "[character] for a list of public characters - others, you'll have to discover by reading this story** "
            ":wink: \n"
            ":coffee: ...more commands coming soon!")
    else:
        # check the channel
        if message.channel_mentions:
            channel = message.channel_mentions[0]
            channel_mention = channel.mention
            description = channel.topic
            await message.channel.send(f"{channel_mention}: {description}")
        else:
            await message.channel.send("Hm, make sure the channel is valid. Try again _eh_!")


def output_character(character_name):
    character = characters[character_name]
    name = character['name']
    age = character['age']
    tagline = character['tagline']
    type_char = character['type_char']
    title = character['title']
    birthday = character['birthday']
    height = character['height']
    hair = character['hair']
    eyes = character['eyes']
    tattoos = character['tattoos']
    ethnicity = character.get('ethnicity', None)
    defining_traits = character.get('defining_traits', [])
    based_in = character.get('based_in', None)
    blurb = character['blurb']
    response = (
        f"__**{name}**__ [{age}]\n"
        f"**{title}**\n"
        f"__{tagline}__\n"
        f"**Type of Character**: {type_char}\n"
        f"**Birthday**: {birthday}\n"
        f"**Height**: {height}\n"
        f"**Hair**: {hair}\n"
        f"**Eyes**: {eyes}\n"
        f"**Tattoos**: {tattoos}\n"
    )
    if ethnicity:
        response += f"**Ethnicity**: {ethnicity}\n"
    if defining_traits:
        response += f"**Defining Traits**: {', '.join(defining_traits)}\n"
    if based_in:
        response += f"**Based In**: {based_in}\n"
    response += f"\n{blurb}"
    return response


async def process_info(message, arg_list):
    alt_name = ""
    if not arg_list:
        await message.channel.send("__Summary__\nThe Midnight Shift is a thrilling action-drama set in Southeast "
                                   "Asia; specifically,"
                                   "a former pirate city named Syurga which is at the brink of change. The protagonist,"
                                   "a former mobster known as the Watchdog, starts a new life as a charismatic and "
                                   "sarcastic restaurant manager named Saka, but is forced to revisit his past when he "
                                   "saves a detective from a gang crossfire. The detective, unable to arrest him, "
                                   "instead asks for his help in taking down the gangs vying for power. \n"
                                   "But what starts as a simple case soon spirals out of control as the Watchdog's "
                                   "old habits begin to resurface. Until then, welcome to the city of organized "
                                   "crime, corrupt industries, hungry media, underworld secrets, historical ruin, "
                                   "and the gilded paradise. Welcome to Syurga, where nothing is ever as it seems... \n"
                                   "To find out more about its residents and visitors, type `!aunty -i [character]` "
                                   "to begin. Don't know where to start? Type `!aunty -i characters` for a list of "
                                   "characters! Some are publicly available; **others, you'll have to discover by "
                                   "reading this story :wink:**")
    elif len(arg_list) == 1 and arg_list[0] == "characters":
        names = []
        type_chars = set()
        for v in characters.values():
            if v['type_char'] not in type_chars:
                names.append("__**" + v['type_char'] + "**__")
                type_chars.add(v['type_char'])
            if v['hidden'] == "Yes":
                names.append("- ???")
            else:
                names.append("- " + v['name'].split()[0])
        response = "\n".join(names)
        await message.channel.send(response)
    else:
        character_name = " ".join([arg.lower() for arg in arg_list])
        # Check if there is more than one character with the same first name
        matching_characters = []
        for c, v in characters.items():
            first_name = v['name'].split()[0]
            alt_names = v['alt_names'] if v['alt_names'] else []
            if first_name.lower() == character_name or character_name in alt_names:
                matching_characters.append(v)
                if character_name in alt_names:
                    alt_name = first_name.lower()
        if len(matching_characters) > 1:
            # Ask the user to specify the last name of the character they want information on
            msg = "There are multiple characters named " + character_name + "! Did you mean:\n"
            for i, character in enumerate(matching_characters):
                msg += str(i + 1) + ") " + character['name'] + "\n"
            await message.channel.send(msg)
            selection = await client.wait_for('message', check=lambda m: m.author == message.author)
            while True:
                if selection.content == "!exit":
                    await message.channel.send("Exiting character selection.")
                    break
                if selection.content.isdigit() and 1 <= int(selection.content) <= len(matching_characters):
                    full_name = matching_characters[int(selection.content) - 1]['name']
                    for c, v in characters.items():
                        if v['name'].lower() == full_name.lower():
                            response = output_character(c)
                            await message.channel.send(response)
                            break
                    break
                elif re.match(r'^[a-zA-Z\s]+$', selection.content):
                    for c, v in characters.items():
                        if v['name'].lower() == selection.content.lower():
                            response = output_character(c)
                            await message.channel.send(response)
                            break
                    break
                else:
                    await message.channel.send(
                        f"Invalid selection. Please enter a number between 1 and {len(matching_characters)} inclusive, "
                        f"or a valid character name, or type !exit to quit.")
                selection = await client.wait_for('message', check=lambda m: m.author == message.author)
        elif character_name in characters or alt_name != "":
            if character_name == "aunty":
                await message.channel.send("Ho ho, looking for me?")
            if alt_name != "":
                response = output_character(alt_name)
            if alt_name == "":
                response = output_character(character_name)
            await message.channel.send(response)
        else:
            await message.channel.send(
                f"{character_name} not found in characters dictionary. Try typing the first name!")


client.run('token')
