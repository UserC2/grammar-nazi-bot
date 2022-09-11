#  if message.content.startswith('$hello'):

import discord
from discord.ext import commands
import language_tool_python # doesn't work on replit
import time
import os
import sys

kLocale = 'en-US'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(case_insensitive=True,
                   command_prefix=commands.when_mentioned,
                   intents=intents,
                   strip_after_prefix=True)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def check(ctx, *args):
    if len(args) == 0:
        # check current user
        await ctx.send(f'Checking score of: {ctx.author}')
    else:
        await ctx.send(f'Checking score of: {args[0]}')
        # parse username -> args[0]
        # if not matching any, send error
        # if matching, send their score

@bot.listen('on_message')  # avoid conflicting with commands
async def check_message(message):
    # prevents bot from responding to its own messages
    if message.author == bot.user:
        return  # else this responds to our messages
    await message.channel.send('recieved') # debug
    # this currently checks bot commands (from the user), it should not. (add allow list)
    matches = language_tool_python.LanguageTool(kLocale).check(message.content)
    if len(matches) == 0:
        await message.channel.send("You can spell!")
        return
    else:
        await message.channel.send("You can't spell!")
        return  # temp
        # if > 0 mistakes, add mistakes to user entry
        # if user entry doesn't exist, create it

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, discord.errors.RateLimited):
        print("Error: Being Rate Limited")
        time.sleep(1)
        return

    if isinstance(error, discord.errors.Forbidden):
        await ctx.send(
            "Error: 403 Permission Violation (Check bot permissions!)")
        return

    if isinstance(error, discord.errors.PrivilegedIntentsRequired):
        await ctx.send(
            "Error: PriviledgedIntentsRequired. Contact Developer. Bot shutting down."
        )
        print("Error: PriviledgedIntentsRequired. Bot shutting down.")
        exit()

    if isinstance(error, discord.errors.LoginFailure):
        print("Error: Login Token Invalid. Bot shutting down.")
        exit()

# should this be enclosed in a main function?

if len(sys.argv) < 2: # 1 for program name +1 for bot token
    print("Bot token not provided. Bot shutting down.")
    exit()

bot.run(sys.argv[1]) # bot token

# Todo:
# Store 'score' for each individual user
# Implement check_message()
# Implement allow list for check_message() (e.g typing in bot command or 'gn'/'Gn')
# Implement check()
