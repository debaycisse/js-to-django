from datetime import datetime, timezone

def get_today():
    today = datetime.now(timezone.utc)
    iso_repr_today = today\
        .isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    return iso_repr_today
