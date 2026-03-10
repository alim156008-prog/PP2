from datetime import datetime, timedelta

def parse(s):
    date_part, tz_part = s.split()
    sign = 1 if tz_part[3] == "+" else -1
    h, m = map(int, tz_part[4:].split(":"))
    offset = timedelta(hours=sign * h, minutes=sign * m)

    d = datetime.strptime(date_part, "%Y-%m-%d")
    return d - offset

d1 = parse(input().strip())
d2 = parse(input().strip())

diff = abs(d1 - d2)
print(diff.days)