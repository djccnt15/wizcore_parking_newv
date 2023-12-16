from enum import StrEnum


class WebDriverState(StrEnum):
    SUCCESS = "loading webdriver success"
    ERROR = "loading webdriver error"


class UrlState(StrEnum):
    SUCCESS = "get url success - %s"
    ERROR = "get url error"


class SearchCarState(StrEnum):
    SUCCESS = "search car success"
    ERROR = "search car error - %s"


class SelectCarState(StrEnum):
    SUCCESS = "selecting car success"
    ERROR = "selecting car error"


class DiscountResult(StrEnum):
    SUCCESS = "discount success - %s"
    ERROR = "discount error - %s"
