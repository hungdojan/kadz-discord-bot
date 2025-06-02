import calendar
from datetime import date

import discord

from kadz_discord_bot.models.hardle_results import HardleResults
from kadz_discord_bot.models.user import Users
from kadz_discord_bot.utils import CHAR_MAP, display_username


class HardleUserStatsEmbed(discord.Embed):
    def __init__(
        self,
        user: Users,
        results: list[HardleResults],
        month_year: date,
        interaction: discord.Interaction,
    ):
        super().__init__(title="User stats")
        self.add_field(
            name="User", value=display_username(user.username, interaction), inline=True
        )
        self.add_field(name="Active Days", value=len(results), inline=True)
        successful_runs = [run for run in results if run.nof_tries > 0]
        if successful_runs:
            self.add_field(
                name="Avg Rounds",
                value=f"{sum([run.nof_tries for run in successful_runs])
                         / len(successful_runs):.3f}",
                inline=False,
            )
            self.add_field(
                name="Avg Score",
                value=f"{sum([run.score for run in successful_runs])
                         / len(successful_runs):.3f}",
                inline=True,
            )
        else:
            self.add_field(name="Avg Rounds", value=0, inline=False)
            self.add_field(name="Avg Score", value=0, inline=True)
        self.add_field(
            name="Calendar",
            value=self._generate_calendar(results, month_year),
            inline=False,
        )

    def _generate_calendar(self, results: list[HardleResults], month_year: date) -> str:
        content = ["```", "PoUtStCtPa SoNe"]
        first_day = date(month_year.year, month_year.month, 1).isoweekday() - 1
        all_days = ""
        for i in range(first_day):
            if i == 5:
                all_days += " "
            all_days += "\u2b1c"
        _, nof_days = calendar.monthrange(month_year.year, month_year.month)
        for day in range(nof_days):
            curr_day = date(month_year.year, month_year.month, day + 1)
            if not results or curr_day != results[0].day_play:
                all_days += CHAR_MAP["b"]
            else:
                curr_result = results.pop(0)
                if curr_result.nof_tries < 0:
                    all_days += CHAR_MAP["r"]
                elif curr_result.nof_tries <= 6:
                    all_days += CHAR_MAP["g"]
                else:
                    all_days += CHAR_MAP["y"]
            if curr_day.isoweekday() == 5:
                all_days += " "
            elif curr_day.isoweekday() == 7:
                all_days += ","

        content.extend(all_days.rstrip(",").split(","))
        content.append("```")
        return "\n".join(content)
