from enum import Enum, auto


class DiscountType(Enum):
    M10 = auto(), "10min"
    M30 = auto(), "30min"
    H1 = auto(), "1hour"
