with open("text.txt", "a") as f:
    f.write("Now the file has more content!")

with open("text.txt") as f:
    print(f.read())