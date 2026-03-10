def fun(text, keyword):
    w = text.split()
    for n in w:
        if n == keyword:
            yield True

txt = "geeks for geeks"
s = fun(txt, "geeks")
print(sum(s))