from datetime import datetime, timezone

def get_datetime() -> str: 
    return str(datetime.now(timezone.utc).isoformat())

