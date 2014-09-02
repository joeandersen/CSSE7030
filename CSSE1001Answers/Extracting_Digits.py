def getdigits(n):
    if n<10:
        foo = []
        foo.append(n)
        print type(foo)
        return foo
    else:
        foo = getdigits(n/10)
        foo.append(n%10)
        return foo

