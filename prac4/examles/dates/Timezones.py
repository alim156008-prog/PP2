from datetime import datetime
from zoneinfo import ZoneInfo

utc = datetime.now(ZoneInfo("UTC"))
moscow = utc.astimezone(ZoneInfo("Europe/Moscow"))

print(utc)
print(moscow)