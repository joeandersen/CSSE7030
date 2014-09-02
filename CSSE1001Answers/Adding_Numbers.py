def minus1(x):
  return x-1

def plus1(x):
  return x+1

def add_pos(x, y):
    if y==0:    
        # It's the base case
        return x
    else:
        # It's the step case - what's the smaller problem?
        # Make the recursive call for the smaller problem
        # and use that result to compute the result for add_pos(x,y)
        return plus1(add_pos(x,minus1(y)))
    
        
