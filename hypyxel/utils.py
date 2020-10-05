from datetime import datetime


def timestamp_to_datetime(t: int, b: int = 1000) -> datetime:
    """
    Convert Hypixel Timestamp (Unix Epoch Milliseconds) to datetime object
    :param t: Hypixel timestamp
    :param b: Base (default to 1000: milliseconds)
    :return: datetime
    """
    return datetime.fromtimestamp(t / b)
