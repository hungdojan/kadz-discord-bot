from datetime import datetime

import discord
from discord import Interaction, app_commands
from discord.ext import commands

import kadz_discord_bot.server_bot as server_bot
from kadz_discord_bot.models.hardle_results import HardleResultManager
from kadz_discord_bot.ui_views.hardle_result_embed import HardleResultEmbed
from kadz_discord_bot.utils import TimePeriod


class HardleCommands(commands.Cog):

    def __init__(self, bot: "server_bot.ServerBot"):
        self.bot = bot

    @app_commands.command(name="hardle-result", description="Get game run results.")
    @app_commands.describe(
        member="Member in question.",
        date_str="The day of the run in YYYY-MM-DD format. Defaults to today.",
        hide="Hide the output from everyone. Defaults to True",
    )
    async def results(
        self,
        interaction: Interaction,
        member: discord.Member,
        date_str: str = f"{datetime.today().date()}",
        hide: bool = True,
    ):
        """Display a specific game run of a user.

        :param interaction: A discord interaction object.
        :type interaction: Interaction
        :param member: A member of the server.
        :type member: discord.Memeber
        """

        # must be rewritten to string or find a better solution in the documentation
        try:
            day = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            await interaction.response.send_message(
                f"Incorrect date format, enter YYYY-MM-DD."
            )
            return

        result = HardleResultManager(self.bot.db_session).get_user_results_daily(
            member.name, day
        )
        embed = HardleResultEmbed(result, interaction)
        await interaction.response.send_message(embed=embed, ephemeral=hide)

    @app_commands.command(
        name="hardle-leaderboard",
        description="Display leaderboards for a selected time period.",
    )
    async def leaderboards(
        self,
        interaction: Interaction,
        time_period: TimePeriod,
    ):
        """Display leaderboard for a specific time period.

        :param interaction: A discord interaction object.
        :type interaction: Interaction
        :param time_period: Selected time period.
        :type time_period: TimePeriod
        """
        await interaction.response.send_message("leaderboard")

    @app_commands.command(
        name="hardle-stats",
        description="Display user stats for a selected time period.",
    )
    async def stats(
        self,
        interaction: Interaction,
        time_period: TimePeriod,
        member: discord.Member,
    ):
        """Display user stats for a selected time period.

        :param interaction: A discord interaction object.
        :type interaction: Interaction
        :param time_period: Selected time period.
        :type time_period: TimePeriod
        :param member: A member of the guild.
        :type member: discord.Member
        """
        await interaction.response.send_message("stats")
