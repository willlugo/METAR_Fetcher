from datetime import datetime, timezone

def datform():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")