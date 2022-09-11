# Grammar Nazi Bot

Silently records your grammatical errors while you speak to your friends.

Mention the bot to reveal your lack of grammatical expertise.

### Installation:
- `pip install discord.py`
- `pip install language-tool-python`
- Follow the instructions for your operating system [here](https://www.mongodb.com/docs/manual/tutorial/) to install mongoDB
- Paste the command used to start mongoDB (on the above website) into dbstart
- Paste the command used to start mongoDB (on the above website) into dbstop

### Use:
- You will need to obtain the bot's token (or create your bot own and put its token in a file called `BOT_TOKEN`)
- `./dbstart` to start the database (first)
- `./start` to start the bot (second)

### macOS Users:
- `grep` is incompatible with the `-P` flag, so you will need to install GNU grep.
- Install GNU grep: `brew install grep`
- [Homebrew](https://brew.sh) is required to run this command.
- You will also have to modify `stop`, see `stop` for instructions.
