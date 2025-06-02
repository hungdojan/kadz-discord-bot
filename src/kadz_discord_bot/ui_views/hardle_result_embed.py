import discord

from kadz_discord_bot.models.hardle_results import HardleResults
from kadz_discord_bot.utils import display_username


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
        self.add_field(
            name="Player",
            value=f"{display_username(result.username, interaction)}",
            inline=True,
        )
        self.add_field(name="Results", value=f"{result.nof_tries} / 10", inline=True)
        self.add_field(name="Score", value=f"{result.score:.3f}")
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
