#  if message.content.startswith('$hello'):

import discord
from discord.ext import commands
import language_tool_python

import os
import sqlite3
from sqlite3 import Error
import sys
import time


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'user_scores.sqlite')
LOCALE = 'en-US'

tool = language_tool_python.LanguageTool(LOCALE)

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
        if db_command_user_exists(db, ctx.author.id):
            await ctx.send(f'Author UserID: {ctx.author.id}')
            await ctx.send(f'Score: {db_command_get_score(db, ctx.author.id)}')
        else:
            await ctx.send(f'Score: 0')
            # if user doesn't exist, they haven't been found making a spelling error
    else:
        # check specified user
        await ctx.send(f'Checking score of: {args[0]}')
        # need to parse username from args[0] into userid
        #if db_command_user_exists(db, ctx.author.id):
        #    await ctx.send(f'Sender UserID: {ctx.author.id}')
        #    await ctx.send(f'User Score: {
        #else:
        #    await ctx.send('User does not exist.')
        #await ctx.send(f'Sender UserID: {ctx.author.id}')
        #await ctx.send(f'User Score: {db_command_get_score(db, ctx.author.id)}')
        # parse username -> args[0]
        # need to figure out user id from username (is that possible?)
        # if not matching any, send error
        # if matching, send their score


@bot.listen('on_message')  # avoid conflicting with commands
async def check_message(message):
    # prevents bot from responding to its own messages
    if message.author == bot.user:
        return  # else this responds to our messages
    await message.channel.send('recieved') # debug
    # this currently checks bot commands (from the user), it should not. (add allow list)
    matches = tool.check(message.content)
    if matches:
        await message.channel.send(f"You can't spell! ${len(matches)}") # temp debug
        if db_command_user_exists(db, message.author.id):
            db_command_update_score(db, message.author.id, len(matches))
        else:
            db_command_add_user(db, message.author.id, len(matches))
        # add len(matches) to message.author's entry in the database
        # store the author's userid in the database, NOT their username and tag, otherwise their score will be lost if their nickname changes
        # if > 0 mistakes, add mistakes to user entry
        # if user entry doesn't exist, create it
    else: # eliminate once debug done, should do nothing if spelling is correct
        await message.channel.send("You can spell!") # temp debug


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


def db_connect(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print('Connected to database.')
    except Error as e:
        print(f'Couldn\'t connect to database: Error: {e}')
        print('Aborting bot startup.')
        exit()
    return connection


def db_execute_single_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result is not None else result
    except Error as e:
        print(f'Database error: "{e}" occured!')


def db_execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f'Database error: "{e}" occured!')


def db_execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f'Database error: "{e}" occured!')


def db_command_add_user(connection, discord_id, start_score):
    add_user = f"""
    INSERT INTO
        users (discord_id, user_score)
    VALUES
        ({discord_id}, {start_score});
    """
    db_execute_query(connection, add_user)


def db_command_create_users_table(connection):
    print("running create users table")
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        discord_id INTEGER PRIMARY KEY,
        user_score INTEGER
    );
    """
    db_execute_query(connection, create_users_table)


def db_command_get_score(connection, discord_id):
    print("running get score")
    select_score = f"""
    SELECT
        user_score
    FROM
        users
    WHERE
        discord_id = {discord_id};\
    """
    return db_execute_single_read_query(connection, select_score) # [0][0]
    # db_execute_read_query returns a tuple of tuples, so [0][0] is used to
    # retrieve the actual score


def db_command_update_score(connection, discord_id, score_increase):
    print("running update score")
    original_score = db_command_get_score(connection, discord_id)
    update_score = f"""
    UPDATE
        users
    SET
        user_score = {original_score + score_increase}
    WHERE
        discord_id = {discord_id}
    """
    db_execute_query(connection, update_score)


def db_command_user_exists(connection, discord_id):
    print("running user_exists")
    check_exists = f"""
    SELECT
        user_score
    FROM
        users
    WHERE
        discord_id = {discord_id}
    """
    return db_execute_single_read_query(connection, check_exists) is not None


if __name__ == '__main__':
    print('entered main')
    db = db_connect(DB_PATH)
    db_command_create_users_table(db)
    if len(sys.argv) < 2: # 1 argument for program name +1 for bot token
        print('Bot token not provided. Bot shutting down.')
        exit()
    bot.run(sys.argv[1]) # bot token


# make sqlite into class once working

# Todo:
# Implement allow list for check_message() (e.g typing in bot command or 'gn'/'Gn')
# Implement check() (done for single user, not done for checking other users)
# Comments for functions
