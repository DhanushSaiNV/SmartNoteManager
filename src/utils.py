from datetime import datetime, timezone

def get_datetime() -> str: 
    return str(datetime.now(timezone.utc).isoformat())

def get_datetime_readable() -> str:
    return datetime.now(timezone.utc).strftime("%d-%m-%Y")

