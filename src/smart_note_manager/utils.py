from datetime import datetime, timezone
import re

def get_datetime() -> str: 
    return str(datetime.now(timezone.utc).isoformat())

def get_datetime_for_folder_name() -> str:
    raw_datetime_str = get_datetime()

    return re.sub(r'[\\/:*?"<>|]', "", raw_datetime_str)

def valid_folder_name(str) -> str:

    return re.sub(r'[\\/:*?"<>|]', "", str)

def get_datetime_readable() -> str:
    return datetime.now(timezone.utc).strftime("%d-%m-%Y")

def iso_to_readable(iso):
    # Implement this
    date_obj = datetime.fromisoformat(iso)
    return date_obj.strftime("%d-%m-%Y")

