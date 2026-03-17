from functools import reduce

print(list(map(lambda x: x * 2, [1, 2, 3])))

print(list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4])))

print(reduce(lambda x, y: x + y, [1, 2, 3]))