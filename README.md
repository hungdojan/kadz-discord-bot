# Kadz Discord Server Bot

## Installation

### Using `poetry`
```sh
poetry install
```

### Using virtual environment
```sh
python -m venv .venv
. .venv/bin/activate
pip install --no-cache -r requirements.txt -e .
```

## Running
### Set environment variables
Turn on developer mode on Discord to fetch both IDs.
```sh
cat <<EOF > .env
DISCORD_TOKEN=<bot-token>
DISCORD_GUILD_ID=<guild-id>
DISCORD_HARDLE_CHANNEL_ID=<channel-id>
# when empty, new file will be created in $HOME/.local/share/kadz_discord_bot/database.db
# otherwise the directory must exist, the database.db file will be created if not exist
DATABASE_DIRNAME=<path-to-db-file>
EOF
```

### Using `poetry`
```sh
# for poetry v2.0+
eval $(poetry env activate)

# for older poetry versions
poetry shell

# run bot
kadz-discord-bot
# or
poetry run kadz-discord-bot
```

### Using virtual environment
```sh
# with active virtual environment
python -m kadz_discord_bot

# or
kadz-discord-bot
```

## Project structure
```
.
├── .env                    # environment setup
├── compose.yaml
├── DevContainerfile        # dockerfile
├── poetry.lock
├── pyproject.toml          # project configuration
├── README.md               # basic readme
├── requirements.txt        # pip dependencies to install
├── src
│   └── kadz_discord_bot
│       ├── cogs            # modular command files
│       │   ├── hardle_commands.py      # hardle slash commands
│       ├── database.py     # initializes sqlite database
│       ├── __init__.py
│       ├── __main__.py     # main function
│       ├── models          # database models
│       │   ├── base.py
│       │   ├── hardle_results.py
│       │   └── user.py
│       ├── server_bot.py   # the server bot class
│       └── utils.py        # helper functions and variables
└── tests
    └── __init__.py
```
