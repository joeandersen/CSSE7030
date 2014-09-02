def compose(f,g):
    return lambda x: f(g(x))



def repeatedlyApply(f,n):
    if n==1:
        return lambda x: f(x)
    else:
        return compose(f,repeatedlyApply(f,n-1))
    
