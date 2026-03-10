import random

print(random.random())
print(random.randint(1, 10))
items = ["apple", "banana", "cherry"]
print(random.choice(items))
nums = [1, 2, 3, 4, 5]
random.shuffle(nums)
print(nums)