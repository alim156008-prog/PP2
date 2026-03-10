class Rev:
    def __init__(self, d):
        self.d = d
        self.i = len(d)

    def __iter__(self):
        return self

    def __next__(self):
        if self.i == 0:
            raise StopIteration
        self.i -= 1
        return self.d[self.i]
                            
        if self.i == 0:
            raise StopIteration
        self.i -= 1
        return self.d[self.i]

a = input()
for char in Rev(a):
    print(char, end="")
