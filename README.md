# Aunty Mai Bot
A story bot that guides new users through the Discord server and **The Midnight Shift**, given user commands.

## Background
As **The Midnight Shift** is a very dense story, the *Aunty Mai Bot* serves to provide information on the story itself, as well as the _Aunty Mai's_ Discord itself. 
By putting commands into the designated **#bot** channel, a user can use the bot to their advantage.

## Commands
All commands to the bot take the form of:

`!aunty <command> <args>`

The following commands are part of the MVP:
* **Help**: 
  * _Format_: `!aunty -h [channel name]` or `!aunty -help [channel name]`
  * _Description_: Will provide server-specific help to the user. If a channel name isn't provided, by default the Aunty Bot will display a summary of all the commands it can execute. If a channel name is provided, the bot will give a description of the channel.
* **Info**: 
  * _Format_: `!aunty -i [character]` or `!aunty -info [character]`
  * _Description_: Will provide character information to the user. If a character isn't provided, **The Midnight Shift** will be described by default.

## TODO: 
* **List**:
  * _Format_: `!aunty -l <characters>/<channels>` or `!aunty -list <characters>/<channels>`
  * _Description_: Those characters/channels can be tough to keep track of! No worries - the list command is here to help! Specify either `characters` or `channels` after the flag.

## Progress
* **Help**: Needs to properly show if a channel exists and if so, its description.
