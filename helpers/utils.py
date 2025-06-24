import logging

def timestamp_to_ms(ts: str):
    try:
        minutes, seconds = map(int, ts.strip().split(":"))
        return (minutes * 60 + seconds) * 1000
    except Exception as e:
        logging.error(f"Invalid start time '{ts}': {e}")
        return None
