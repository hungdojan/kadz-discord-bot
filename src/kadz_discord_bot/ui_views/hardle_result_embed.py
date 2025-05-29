import discord

from kadz_discord_bot.models.hardle_results import HardleResults


class HardleResultEmbed(discord.Embed):
    def __init__(self, result: HardleResults | None, interaction: discord.Interaction):
        super().__init__(
            title="Hardle Run",
        )
        if result:
            self._generate_result_view(result, interaction)
        else:
            self._generate_empty_view()

    def _generate_result_view(
        self, result: HardleResults, interaction: discord.Interaction
    ):
        def _get_member():
            """Get member tag.

            A plain username is used if user was not found (which should not happen).
            """
            if not interaction.guild:
                return result.username
            user = discord.utils.get(interaction.guild.members, name=result.username)
            return user.mention if user else result.username

        self.add_field(name="Player", value=f"{_get_member()}", inline=True)
        self.add_field(name="Results", value=f"{result.nof_tries} / 10", inline=True)
        self.add_field(name="Score", value=result.score)
        self.add_field(
            name=f"Run on {result.day_play.strftime('%d/%m/%Y')}",
            value=f"```{result.generate_run_str()}```",
            inline=False,
        )
        self.add_field(
            name="Submitted", value=f"{result.timestamp.isoformat()}", inline=False
        )

    def _generate_empty_view(self):
        """Embed view when the result was not found."""
        self.description = "Could not find any run for the given day."
