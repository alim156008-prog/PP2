import sys
import importlib

q = int(sys.stdin.readline())
for _ in range(q):
    module_path, attr = sys.stdin.readline().split()
    try:
        mod = importlib.import_module(module_path)
    except Exception:
        print("MODULE_NOT_FOUND")
        continue

    if not hasattr(mod, attr):
        print("ATTRIBUTE_NOT_FOUND")
        continue

    val = getattr(mod, attr)
    print("CALLABLE" if callable(val) else "VALUE")