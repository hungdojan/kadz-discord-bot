import discord
from tabulate import tabulate

from kadz_discord_bot.models.hardle_results import HardleResults
from kadz_discord_bot.utils import display_username


class HardleResultDailyLeaderboardEmbed(discord.Embed):
    def __init__(self, results: list[HardleResults], interaction: discord.Interaction):
        super().__init__(title="Daily ranking")
        self.results = sorted(
            results, key=lambda x: (x.nof_tries if x.nof_tries > 0 else 11, x.score)
        )
        if self.results:
            self._generate_view(interaction)
        else:
            self._generate_empty_view()

    def _generate_empty_view(self):
        self.description = "No run registered on the given day."

    def _generate_view(self, interaction: discord.Interaction):

        self.add_field(
            name="Date",
            value=self.results[0].day_play.strftime("%d/%m/%Y"),
            inline=True,
        )
        self.add_field(
            name="Winner",
            value=display_username(self.results[0].username, interaction),
            inline=True,
        )
        self.add_field(
            name="Ranking", value=f"```{self._generate_ranking()}```", inline=False
        )

    def _generate_ranking(self) -> str:
        def _display_nof_tries(nof_tries: int):
            return "X" if nof_tries < 0 else f"{nof_tries}"

        selected_items = self.results[:5] if len(self.results) > 5 else self.results
        data = [
            [ind + 1, i.username, _display_nof_tries(i.nof_tries), f"{i.score:.3f}"]
            for ind, i in enumerate(selected_items)
        ]
        return tabulate(data, headers=["Pos", "Username", "Nof Tries", "Score"])
