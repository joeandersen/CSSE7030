def string2int(mystring):
    if all_digits(mystring):
        answer = int(mystring)
    else:
        raise SyntaxError('not an integer')
    return answer
    
