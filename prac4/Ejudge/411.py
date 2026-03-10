import json
import sys

source = json.loads(sys.stdin.readline())
patch = json.loads(sys.stdin.readline())

def apply_patch(src, p):
    if not isinstance(src, dict) or not isinstance(p, dict):
        return p
    for k, v in p.items():
        if v is None:
            if k in src:
                del src[k]
        elif isinstance(v, dict) and isinstance(src.get(k), dict):
            apply_patch(src[k], v)
        else:
            src[k] = v
    return src

res = apply_patch(source, patch)
print(json.dumps(res, separators=(",", ":"), sort_keys=True))
