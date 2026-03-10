from datetime import datetime

d1 = datetime(2026, 2, 20, 10, 0, 0)
d2 = datetime(2026, 2, 24, 12, 0, 0)

diff = d2 - d1
print(diff.total_seconds())