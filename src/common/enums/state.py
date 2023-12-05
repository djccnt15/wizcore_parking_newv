from enum import StrEnum


class LogMsg(StrEnum):
    START = "Program Starts"
    REFRESH = "Refresh Page"
    QUIT = "WebDriver Quit"
    LOG_LEVEL = "log_level must be one of %s"


class WebDriverState(StrEnum):
    SUCCESS = "loading webdriver success"
    ERROR = "loading webdriver error"


class UrlState(StrEnum):
    SUCCESS = "get url success - %s"
    ERROR = "get url error"


class LoginState(StrEnum):
    SUCCESS = "login success - %s"
    ERROR = "login error - %s"


class SearchCarState(StrEnum):
    SUCCESS = "search car success"
    ERROR = "search car error - %s"


class SelectCarState(StrEnum):
    SUCCESS = "selecting car success"
    ERROR = "selecting car error"


class DiscountResult(StrEnum):
    SUCCESS = "discount success - %s"
    ERROR = "discount error - %s"
