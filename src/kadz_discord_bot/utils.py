import enum
from datetime import date, datetime

import kadz_discord_bot.models.base as base

BLACK_SQUARE = b"\xe2\xac\x9b"
YELLOW_SQUARE = b"\xf0\x9f\x9f\xa8"
GREEN_SQUARE = b"\xf0\x9f\x9f\xa9"

SQUARE_MAP = {
    BLACK_SQUARE.decode("utf-8"): "b",
    YELLOW_SQUARE.decode("utf-8"): "y",
    GREEN_SQUARE.decode("utf-8"): "g",
}

CHAR_MAP = {
    "b": BLACK_SQUARE.decode("utf-8"),
    "y": YELLOW_SQUARE.decode("utf-8"),
    "g": GREEN_SQUARE.decode("utf-8"),
}


class Month(enum.Enum):
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12

class TimePeriod(str, enum.Enum):
    daily = "daily"
    monthly = "monthly"
    all = "all"


def decode_hardle_result(content: list[str]) -> tuple[date, int, str]:
    """Decodes the Hardle message.

    :param content: The original message content split by the lines.
    :type content: list[str]
    :return: Parsed data. Contains the date of the run, the number of tries (-1 if lost)
        and the encoded run itself. The mapping is defined in utils.py::CHAR_MAP
    :rtype: tuple[date, int, str]
    """
    # pop unimportant lines
    content = content[1:-1]
    day, result = content.pop(0).split(" | ")
    date = datetime.strptime(day, "%m/%d/%Y").date()
    parsed_result = int(result.split("/")[0].replace("X", "-1"))

    encoded_run = ""
    for i, line in enumerate(content):
        if i != 0:
            encoded_run += ","
        for c in line[0:5]:
            encoded_run += SQUARE_MAP[c]

    return date, parsed_result, encoded_run


def allowed_columns(data: dict, obj: type[base.Base]) -> dict:
    return {k: v for k, v in data.items() if k in obj.get_columns()}
