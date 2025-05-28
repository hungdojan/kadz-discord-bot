class KadzException(BaseException):
    """Base exception class for project."""
    pass

class DailyResultExistError(KadzException):
    """There already exists a daily run in the database."""
    pass
