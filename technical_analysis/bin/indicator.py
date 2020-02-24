from dataclasses import dataclass, field

@dataclass
class Adx:
    time_period: int = 10
    interval: str = "daily"
    series_type: str = "close"
    data_key = "Technical Analysis: ADX"
    key: str = "ADX"

@dataclass
class Rsi:
    time_period: int = 10
    interval: str = "daily"
    series_type: str = "close"
    data_key = "Technical Analysis: RSI"
    key: str = "RSI"


@dataclass
class BBands: 
    time_period: int = 5
    interval: str = "daily"
    series_type: str = "close"
    up: int = 3
    down: int = 3
    data_key = "Technical Analysis: BBANDS"
    # TODO: Also read "Real Lower Band"
    # Ignore "Real Middle Band", "Real Lower Band" key
    key: str = "Real Upper Band"
