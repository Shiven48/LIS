import io
from typing import Any, List, Optional
from datetime import datetime
import os

from pydantic import FilePath

def is_number(value: Any) -> bool:
    return isinstance(value, (int, float))

def is_none(value: Any) -> bool:
    return value is None

def is_array(value: Any) -> bool:
    return isinstance(value, List)

def is_string(value: Any) -> bool:
    return isinstance(value, str)

def safe_get(record: list, index: int, default: str = "") -> str:
    """Safely get an item from a list at a given index"""
    try:
        return record[index] if index < len(record) else default
    except (IndexError, TypeError):
        return default

def parse_datetime(date_str: str) -> Optional[str]:
    """Parse ASTM datetime format (YYYYMMDDHHMMSS) to ISO format"""
    if not date_str or len(date_str) < 8:
        return None
    try:
        if len(date_str) == 8:
            dt = datetime.strptime(date_str, "%Y%m%d")
        elif len(date_str) == 14:
            dt = datetime.strptime(date_str, "%Y%m%d%H%M%S")
        else:
            return date_str
        return dt.isoformat()
    except ValueError:
        return date_str
    
def log_to_file(data, folder_path, filename):
    """
    Logs `data` to a file in the specified `folder_path`.
    If `filename` is not provided, it uses a timestamp-based default.
    """
    
    os.makedirs(folder_path, exist_ok=True)
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"log_{timestamp}.txt"

    file_path = os.path.join(folder_path, filename)

    with io.open(file_path, mode='a', encoding='utf-8') as file:
        file.write(data)
        if not data.endswith('\n'):
            file.write('\n')
    return file_path