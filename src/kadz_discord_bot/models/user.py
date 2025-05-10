from datetime import date

from sqlalchemy import delete, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Date, String

from kadz_discord_bot.models.base import Base, BaseManager
from kadz_discord_bot.utils import allowed_columns


class Users(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String, primary_key=True)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)


class UserManager(BaseManager):
    def get_user(self, username: str) -> Users | None:
        """Fetch a user.

        :param username: User's username.
        :type username: str
        :return: Found user object or None.
        :rtype: Users | None
        """
        query = select(Users).where(Users.username == username)
        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def get_or_insert_user(
        self, username: str, date_of_birth: date | None = None
    ) -> Users:
        """Fetch a user or insert if not exist.

        :param username: User's username.
        :type username: str
        :param date_of_birth: A date of birth. Defaults to None.
        :type date_of_birth: date | None
        :return: A user object.
        :rtype: Users
        """
        user = self.get_user(username)
        if user:
            return user
        user = Users(username, date_of_birth) # type: ignore
        self.session.add(user)
        self.session.commit()
        return user

    def update_user(self, username: str, **data) -> Users | None:
        """Update the user.

        :param username: User's username.
        :type username: str
        :return: Updated user, None if user was not found.
        :rtype: User | None
        """
        user = self.get_user(username)
        if not user:
            return None
        valid_data = allowed_columns(data, Users)
        for k, v in valid_data.items():
            setattr(user, k, v)
        self.session.commit()
        return user

    def delete_user(self, username: str):
        """Delete a user if exists.

        :param username: User's username.
        :type username: str
        """
        query = delete(Users).where(Users.username == username)
        self.session.execute(query)
