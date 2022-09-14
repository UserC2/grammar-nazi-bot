# Grammar Nazi Bot

Silently records your grammatical errors while you speak to your friends.

Mention the bot to reveal your lack of grammatical expertise.

### Installation:
- Install [Python](python.org/downloads)
- `pip install discord.py`
- `pip install language-tool-python`
- `git clone https://github.com/UserC2/grammar-nazi-bot`

### Use:
- [Create a bot account](discordpy.readthedocs.io/en/stable/discord.html)
- Create a file named `BOT_TOKEN` and paste your bot's token in it.
- `./start` to start the bot
- `./stop` to stop the bot
- The bot's log is stored in `bot.out` and will be deleted the next time the
bot starts up.

### macOS Users:
- `grep` is incompatible with the `-P` flag, so you will need to install GNU grep.
- Install GNU grep: `brew install grep`
- [Homebrew](brew.sh) is required to run this command.
- You will also have to modify `stop`, see `stop` for instructions.
