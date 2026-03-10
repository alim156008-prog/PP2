import json
import sys
import re

data = json.loads(sys.stdin.readline())
q = int(sys.stdin.readline())

token_re = re.compile(r'([A-Za-z_][A-Za-z0-9_]*)|\[(\d+)\]')

def resolve(root, query):
    cur = root
    if query.startswith(".") or ".." in query:
        return None, False
    parts = query.split(".") if query else []
    for part in parts:
        if part == "":
            return None, False
        pos = 0
        first = True
        while pos < len(part):
            m = token_re.match(part, pos)
            if not m:
                return None, False
            key, idx = m.group(1), m.group(2)
            if key is not None:
                if not first and pos != 0:
                    pass
                if not isinstance(cur, dict) or key not in cur:
                    return None, False
                cur = cur[key]
            else:
                if not isinstance(cur, list):
                    return None, False
                i = int(idx)
                if i < 0 or i >= len(cur):
                    return None, False
                cur = cur[i]
            pos = m.end()
            first = False
    return cur, True

for _ in range(q):
    query = sys.stdin.readline().rstrip("\n")
    val, ok = resolve(data, query)
    if not ok:
        print("NOT_FOUND")
    else:
        print(json.dumps(val, separators=(",", ":"), sort_keys=True))