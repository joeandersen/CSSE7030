def has_gt(nums, n):
    """Return True iff nums contains at least one number bigger than n.

    has_gt(list<number>, number) -> boolean
    """
    # add your code here
    answer = False
    for number in nums:
        if number>n:
            answer = True

    return answer
        
        
    
