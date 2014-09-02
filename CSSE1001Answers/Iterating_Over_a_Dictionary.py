def big_keys(dictionary,integer):

    answer = []
    for k in dictionary:
        if dictionary[k]>integer:
            answer.append(k)
    return answer

    
        
