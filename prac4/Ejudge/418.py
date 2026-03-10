import sys

x1, y1 = map(float, sys.stdin.readline().split())
x2, y2 = map(float, sys.stdin.readline().split())

x2r = x2
y2r = -y2

dx = x2r - x1
dy = y2r - y1

t = -y1 / dy

xr = x1 + t * dx
yr = 0.0

print(f"{xr:.10f} {yr:.10f}")