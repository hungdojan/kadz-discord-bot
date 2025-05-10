import re
from datetime import datetime, timezone
from pathlib import Path

import discord
from discord.ext import commands
from discord.message import Message
from sqlalchemy.orm import Session

from kadz_discord_bot.cogs.hardle_commands import HardleCommands
from kadz_discord_bot.database import Database
from kadz_discord_bot.models.hardle_results import HardleResultManager
from kadz_discord_bot.models.user import UserManager
from kadz_discord_bot.utils import decode_hardle_result


class ServerBot(commands.Bot):
    def __init__(self, channel_ids: dict[str, int], guild_id: int, database_path: Path):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

        self.channel_ids = channel_ids
        self.guild_id = guild_id
        self.db = Database(database_path)

    @property
    def db_session(self) -> Session:
        return self.db.session

    async def setup_hook(self) -> None:
        await self.add_cog(HardleCommands(self))
        await self.tree.sync()

    async def on_ready(self):
        print("Hardle bot is online")

    async def on_message(self, message: Message, /) -> None:
        # logic for hardle channel
        if message.channel.id == self.channel_ids.get("hardle", -1):
            self.hardle_channel_logic(message)

    def hardle_channel_logic(self, message: Message) -> None:
        """Handle messages in `hardle` channel.

        :param message: The message object.
        :type message: Message
        """
        # ignore non-hardle messages
        if not re.match("Hardle", message.content) or not re.search(
            r"Play .* on hardle\.org", message.content
        ):
            return

        data = message.content.splitlines()
        day, nof_tries, run = decode_hardle_result(data)
        username = message.author.name

        user = UserManager(self.db_session).get_or_insert_user(username)
        HardleResultManager(self.db_session).insert_result(
            user.username, nof_tries, day, datetime.now(timezone.utc), run
        )
