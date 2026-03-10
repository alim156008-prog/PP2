n = int(input())
document = {}
output = []
for _ in range(n):
    cmd = input().split()
    if cmd[0] == "set":
        document[cmd[1]] = cmd[2]
    else: 
        key = cmd[1]
        output.append(document.get(key, f"KE: no key {key} found in the document"))
print("\n".join(output))