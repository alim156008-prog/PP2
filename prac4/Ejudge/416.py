from datetime import datetime, timedelta

def parse(s):
    date_part, time_part, tz_part = s.split()
    sign = 1 if tz_part[3] == "+" else -1
    h, m = map(int, tz_part[4:].split(":"))
    offset = timedelta(hours=sign * h, minutes=sign * m)

    dt = datetime.strptime(date_part + " " + time_part, "%Y-%m-%d %H:%M:%S")
    return dt - offset

start = parse(input().strip())
end = parse(input().strip())

print(int((end - start).total_seconds()))