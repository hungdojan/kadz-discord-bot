from datetime import date, datetime

from sqlalchemy import Date, ForeignKey, and_, delete, extract, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime, Integer, String

from kadz_discord_bot.models.base import Base, BaseManager
from kadz_discord_bot.models.user import UserManager
from kadz_discord_bot.utils import CHAR_MAP


class HardleResults(Base):
    __tablename__ = "hardle_results"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[int] = mapped_column(
        ForeignKey("users.username", ondelete="CASCADE"), nullable=False, index=True
    )
    nof_tries: Mapped[int] = mapped_column(Integer, nullable=False)
    day_play: Mapped[date] = mapped_column(Date, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    rounds: Mapped[str] = mapped_column(String)

    def generate_run_str(self) -> str:
        output = []
        for i, r in enumerate(self.rounds.split(",")):
            row = "".join([CHAR_MAP[symbol] for symbol in r])
            output.append(f"{i+1:02}. {row}")
        return "\n".join(output)

    @property
    def score(self) -> float:
        """Calculate the custom scoring of the run.

        The score is calculated based on the number of discovered letters.
        We want to promote players that had tougher runs.

        Each yellow letter/tile is worth 1 point, a green one is worth 2 points.
        If the user manage to get a full row of black tiles, it is worth 5 points.
        The final sum is divided by the number of tiles. If the user did not manage
        to guess the word, the sum will be divided by 10 rounds * 5 tiles.

        The interpretation of the final score is the average gained/known information
        per round. The player with a lower score is considered more skilled.
        """
        score = 0
        for row in self.rounds.split(","):
            if row == "bbbbb":
                score += 5
                continue
            for symbol in row:
                if symbol == "y":
                    score += 1
                elif symbol == "g":
                    score += 2

        rounds = 10 if self.nof_tries == -1 else self.nof_tries
        return score / (rounds * 5)


class HardleResultManager(BaseManager):

    def get_results(self) -> list[HardleResults]:
        query = select(HardleResults)
        result = self.session.execute(query).scalars().all()
        return [item for item in result]

    def get_user_results(self, username: str) -> list[HardleResults]:
        user = UserManager(self.session).get_user(username)
        if not user:
            return []
        query = select(HardleResults).where(HardleResults.username == user.username)
        result = self.session.execute(query).scalars().all()
        return [item for item in result]

    def get_user_results_daily(self, username: str, day: date) -> HardleResults | None:
        query = select(HardleResults).where(
            and_(
                HardleResults.username == username,
                HardleResults.day_play == day,
            )
        )
        result = self.session.execute(query).scalar()
        return result

    def get_user_results_monthly(self, username: str, month: int, year: int):
        query = select(HardleResults).where(
            # NOTE: not tested
            and_(
                HardleResults.username == username,
                extract("year", HardleResults.day_play) == year,
                extract("month", HardleResults.day_play) == month,
            )
        )
        result = self.session.execute(query).scalars().all()
        return [item for item in result]

    def insert_result(
        self,
        username: str,
        nof_tries: int,
        day_play: date,
        timestamp: datetime,
        rounds: str,
    ) -> HardleResults:
        user = UserManager(self.session).get_user(username)
        if not user:
            raise ValueError(f"User {username} not found.")
        hr = HardleResults(
            username=username,
            nof_tries=nof_tries,
            day_play=day_play,
            timestamp=timestamp,
            rounds=rounds,
        )
        self.session.add(hr)
        self.session.commit()
        return hr

    def delete_result(self, _id: int):
        query = delete(HardleResults).where(HardleResults.id == _id)
        self.session.execute(query)
