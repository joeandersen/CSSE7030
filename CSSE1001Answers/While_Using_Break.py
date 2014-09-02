def div_7_11(start):
    """find the sum of integers from start up to the first number divisible by either 7 or 11
    """

    sum = 0
    count = start
    while count<=start*7:
        sum = sum+1
        if count%7==0 or count%11==0:
            break
        count = count+1

    return sum
    
