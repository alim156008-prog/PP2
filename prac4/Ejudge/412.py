import json
import sys

a = json.loads(sys.stdin.readline())
b = json.loads(sys.stdin.readline())

MISSING = object()
diffs = []

def jdump(x):
    if x is MISSING:
        return "<missing>"
    return json.dumps(x, separators=(",", ":"), sort_keys=True)

def walk(x, y, path):
    if isinstance(x, dict) and isinstance(y, dict):
        keys = set(x.keys()) | set(y.keys())
        for k in keys:
            nx = x.get(k, MISSING)
            ny = y.get(k, MISSING)
            new_path = k if path == "" else path + "." + k
            walk(nx, ny, new_path)
        return

    if x is MISSING or y is MISSING:
        diffs.append((path, jdump(x), jdump(y)))
        return

    if x != y:
        diffs.append((path, jdump(x), jdump(y)))

walk(a, b, "")

if not diffs:
    print("No differences")
else:
    diffs.sort(key=lambda t: t[0])
    for p, oldv, newv in diffs:
        print(f"{p} : {oldv} -> {newv}")