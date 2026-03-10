import math
import sys

r_line = sys.stdin.readline().strip()
while r_line == "":
    r_line = sys.stdin.readline().strip()
r = float(r_line)

ax, ay = map(float, sys.stdin.readline().split())
bx, by = map(float, sys.stdin.readline().split())

dx, dy = bx - ax, by - ay
dd = dx * dx + dy * dy

if dd == 0.0:
    inside = (ax * ax + ay * ay) <= r * r + 1e-12
    print(f"{(0.0 if not inside else 0.0):.10f}")
    sys.exit(0)

ad = ax * dx + ay * dy
aa = ax * ax + ay * ay
rr = r * r

A = dd
B = 2.0 * ad
C = aa - rr

disc = B * B - 4.0 * A * C

if disc < 0.0:
    inside0 = aa <= rr + 1e-12
    length = math.sqrt(dd) if inside0 else 0.0
else:
    sqrt_disc = math.sqrt(max(0.0, disc))
    t1 = (-B - sqrt_disc) / (2.0 * A)
    t2 = (-B + sqrt_disc) / (2.0 * A)
    if t1 > t2:
        t1, t2 = t2, t1

    lo = max(0.0, t1)
    hi = min(1.0, t2)
    length = 0.0
    if hi > lo:
        length = (hi - lo) * math.sqrt(dd)

print(f"{length:.10f}")