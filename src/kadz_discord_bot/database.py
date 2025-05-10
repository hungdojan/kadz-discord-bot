from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from kadz_discord_bot.models.base import Base


class Database:

    def __init__(self, filepath: Path) -> None:
        self.engine = create_engine(f"sqlite:///{str(filepath.resolve())}", echo=True)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self._session = Session()

    @property
    def session(self) -> Session:
        return self._session
