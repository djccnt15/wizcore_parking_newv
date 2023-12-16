from enum import StrEnum


class LogMsg(StrEnum):
    START = "Program Starts"
    REFRESH = "Refresh Page"
    QUIT = "WebDriver Quit"
    LOG_LEVEL = "log_level must be one of %s"
