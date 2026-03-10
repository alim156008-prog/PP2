def is_valid(num):
    for x in str(num):
        if int(x) % 2 == 1:
            return False
    return True

a= int(input())
if is_valid(a):
    print("Valid")
else:
    print("Not valid")