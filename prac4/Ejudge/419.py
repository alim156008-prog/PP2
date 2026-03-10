import math
import sys

r = float(sys.stdin.readline().strip())
ax, ay = map(float, sys.stdin.readline().split())
bx, by = map(float, sys.stdin.readline().split())

def dist_point_to_segment(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    dd = dx * dx + dy * dy
    if dd == 0.0:
        return math.hypot(px - ax, py - ay)
    t = ((px - ax) * dx + (py - ay) * dy) / dd
    if t < 0.0:
        cx, cy = ax, ay
    elif t > 1.0:
        cx, cy = bx, by
    else:
        cx, cy = ax + t * dx, ay + t * dy
    return math.hypot(px - cx, py - cy)

eps = 1e-12
dseg = dist_point_to_segment(0.0, 0.0, ax, ay, bx, by)

ab = math.hypot(bx - ax, by - ay)
if dseg >= r - eps:
    print(f"{ab:.10f}")
    sys.exit(0)

d1 = math.hypot(ax, ay)
d2 = math.hypot(bx, by)

dot = ax * bx + ay * by
cos_theta = dot / (d1 * d2)
cos_theta = max(-1.0, min(1.0, cos_theta))
theta = math.acos(cos_theta)

alpha1 = math.acos(max(-1.0, min(1.0, r / d1)))
alpha2 = math.acos(max(-1.0, min(1.0, r / d2)))

phi = theta - alpha1 - alpha2
if phi < 0.0:
    phi = 0.0

t1 = math.sqrt(max(0.0, d1 * d1 - r * r))
t2 = math.sqrt(max(0.0, d2 * d2 - r * r))

arc = min(r * phi, r * (2.0 * math.pi - phi))
print(f"{(t1 + t2 + arc):.10f}")