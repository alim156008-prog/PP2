import sys

g = 0
q = int(sys.stdin.readline())

commands = [sys.stdin.readline().split() for _ in range(q)]

def outer():
    n = 0

    def inner():
        nonlocal n
        global g
        local_var = 0
        for scope, value in commands:
            x = int(value)
            if scope == "global":
                g += x
            elif scope == "nonlocal":
                n += x
            elif scope == "local":
                local_var += x

    inner()
    return n

n_final = outer()
print(g, n_final)