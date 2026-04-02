from datetime import datetime, timedelta, timezone

def get_ph_time():
    """
    Returns the current time in Philippines Standard Time (UTC+8).
    """
    return datetime.now(timezone(timedelta(hours=8)))
