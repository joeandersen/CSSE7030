def dec2base(n,b):
    if n<b:
        foo = []
        foo.append(n)
        print type(foo)
        return foo
    else:
        foo = dec2base(n/b,b)
        foo.append(n%b)
        return foo

