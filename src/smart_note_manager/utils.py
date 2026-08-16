from datetime import datetime, timezone

def get_datetime() -> str: 
    return str(datetime.now(timezone.utc).isoformat())

def get_datetime_readable() -> str:
    return datetime.now(timezone.utc).strftime("%d-%m-%Y")

def iso_to_readable(iso):
    # Implement this
    date_obj = datetime.fromisoformat(iso)
    return date_obj.strftime("%d-%m-%Y")