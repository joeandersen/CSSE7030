def all_gt(nums, n):
    """Return the list of all numbers from nums that are bigger than n.

    all_gt(list<number>, number) -> list<number>
    """
    # add your code here
    answer = []
    for number in nums:
        if number>n:
                answer.append(number)
            

    return answer
        
        
    
