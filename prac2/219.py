n = int(input())
episodes = {}
for _ in range(n):
    l = input().split()
    name = l[0]
    count = int(l[1])
    if name in episodes:
        episodes[name] += count
    else:
        episodes[name] = count
for name in sorted(episodes.keys()):
    print(name, episodes[name])
