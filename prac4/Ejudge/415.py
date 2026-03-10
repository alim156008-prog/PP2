from datetime import datetime, timedelta

def is_leap(y):
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

def parse_line(s):
    date_part, tz_part = s.split()
    sign = 1 if tz_part[3] == "+" else -1
    h, m = map(int, tz_part[4:].split(":"))
    offset = timedelta(hours=sign * h, minutes=sign * m)
    d = datetime.strptime(date_part, "%Y-%m-%d")
    utc_moment = d - offset
    return d.date(), offset, utc_moment

birth_date, birth_offset, _ = parse_line(input().strip())
current_date, current_offset, current_utc = parse_line(input().strip())

bm, bd = birth_date.month, birth_date.day
year = current_date.year

def birthday_utc(y):
    mm, dd = bm, bd
    if bm == 2 and bd == 29 and not is_leap(y):
        mm, dd = 2, 28
    local = datetime(y, mm, dd)
    return local - birth_offset

cand = birthday_utc(year)
if cand < current_utc:
    cand = birthday_utc(year + 1)

delta_seconds = int((cand - current_utc).total_seconds())
if delta_seconds <= 0:
    print(0)
else:
    print((delta_seconds + 86400 - 1) // 86400)