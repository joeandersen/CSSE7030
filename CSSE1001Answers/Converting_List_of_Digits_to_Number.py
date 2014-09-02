def base2dec(digits,base):
    #print digits
    if len(digits)==1:
        return digits[0]
    else:
        return base*base2dec(digits[0:-1],base)+digits[-1]
    
    
