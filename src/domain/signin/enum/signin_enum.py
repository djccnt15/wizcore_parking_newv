from enum import StrEnum


class LoginState(StrEnum):
    SUCCESS = "login success - %s"
    ERROR = "login error - %s"
