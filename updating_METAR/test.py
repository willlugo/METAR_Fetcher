from datetime import datetime, timezone


now = datetime.now(timezone.utc)
nowform = now.strftime("%Y-%m-%dT%H:%MZ")
print(nowform)