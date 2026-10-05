import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start} seconds")
        return result
    return wrapper

def validate_csv_file(file):
    if not file.filename.endswith('.csv'):
        return False
    # Simplified validation
    return True

def parse_sort_params(sort_by: str, sort_order: str):
    return sort_by, sort_order

def format_percentage(value: float) -> str:
    return f"{value * 100:.2f}%"
