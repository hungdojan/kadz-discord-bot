from datetime import date, datetime

import discord
from discord import Interaction, app_commands
from discord.ext import commands

import kadz_discord_bot.server_bot as server_bot
from kadz_discord_bot.models.hardle_results import HardleResultManager
from kadz_discord_bot.models.user import UserManager
from kadz_discord_bot.ui_views.hardle_result_daily_leaderboard_embed import (
    HardleResultDailyLeaderboardEmbed,
)
from kadz_discord_bot.ui_views.hardle_result_embed import HardleResultEmbed
from kadz_discord_bot.ui_views.hardle_user_stats_embed import HardleUserStatsEmbed
from kadz_discord_bot.utils import CHAR_MAP, TimePeriod


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
        :type member: discord.Member
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
        name="hardle-daily-leaderboard", description="Display a daily leaderboard."
    )
    @app_commands.describe(
        date_str="The day of the run in YYYY-MM-DD format. Defaults to today.",
        hide="Hide the output from everyone. Defaults to True",
    )
    async def daily_leaderboard(
        self,
        interaction: Interaction,
        date_str: str = f"{datetime.today().date()}",
        hide: bool = True,
    ):
        try:
            day = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            await interaction.response.send_message(
                "Incorrect date format, enter YYYY-MM-DD."
            )
            return
        results = HardleResultManager(self.bot.db_session).get_all_daily_results(day)
        embed = HardleResultDailyLeaderboardEmbed(results, interaction)
        await interaction.response.send_message(embed=embed, ephemeral=hide)

    @app_commands.command(name="hardle-user-profile", description="Display user stats.")
    @app_commands.describe(
        member="Member in question.",
        month_year="The month and year to display monthly stats in YYYY-MM format. Defaults to current month.",
        hide="Hide the output from everyone. Defaults to True",
    )
    async def user_stats(
        self,
        interaction: Interaction,
        member: discord.Member,
        month_year: str = datetime.today().strftime("%Y-%m"),
        hide: bool = True,
    ):
        try:
            day = datetime.strptime(month_year, "%Y-%m")
        except ValueError:
            await interaction.response.send_message(
                "Incorrect date format, enter YYYY-MM"
            )
            return
        user = UserManager(self.bot.db_session).get_user(member.name)
        if not user:
            await interaction.response.send_message(
                f"User {member.name} did not submitted any Hardle run."
            )
        results = HardleResultManager(self.bot.db_session).get_user_results_monthly(
            member.name, day.month, day.year
        )
        embed = HardleUserStatsEmbed(user, results, day, interaction)
        await interaction.response.send_message(embed=embed, ephemeral=hide)
