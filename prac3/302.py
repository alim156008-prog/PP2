def is_usual(num):
    for x in (2, 3, 5):
        while num % x == 0:
            num //= x
    if num == 1:
        return True
    else:
        return False

a = int(input())
if is_usual(a):
    print("Yes")
else:
    print("No")