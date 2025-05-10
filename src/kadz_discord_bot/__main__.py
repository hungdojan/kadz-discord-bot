import os
from pathlib import Path

import discord
from dotenv import load_dotenv

from kadz_discord_bot.server_bot import ServerBot


def main():
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True

    token = os.getenv("DISCORD_TOKEN", "")
    try:
        guild_id = int(os.getenv("DISCORD_GUILD_ID", "0"))
        channel_ids = {"hardle": int(os.getenv("DISCORD_HARDLE_CHANNEL_ID", "0"))}
    except (ValueError, TypeError) as e:
        print(e)
        exit(1)

    sqldirname = os.getenv("DATABASE_DIRNAME", "")

    if sqldirname:
        sqldirname = Path(sqldirname)
        if not sqldirname.exists():
            print(f"Path {str(sqldirname.resolve())} does not exist!")
            exit(1)
    else:
        sqldirname = Path.home() / ".local" / "share" / "kadz_discord_bot"
        sqldirname.mkdir(parents=True, exist_ok=True)
    sqlpath = sqldirname / "database.db"

    bot = ServerBot(channel_ids, guild_id, sqlpath)
    bot.run(token)


if __name__ == "__main__":
    main()
