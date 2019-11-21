from requests import get
from random import randint
from sys import exit
from typing import Union


def get_status_code() -> Union[int, None]:

    try:
        response = get(f"https://postman-echo.com/delay/{randint(1, 5)}")
    except Exception:
        return None

    return response.status_code


def exit_with_code() -> None:
    code = get_status_code()
    if code == 200:
        exit(0)
    elif code is None:
        exit(2)
    else:
        exit(1)


if __name__ == "__main__":
    exit_with_code()
