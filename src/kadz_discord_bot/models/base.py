from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    @staticmethod
    def get_columns():
        return [c.name for c in __class__.__table__.columns]


class BaseManager:
    def __init__(self, session: Session):
        self.session = session
