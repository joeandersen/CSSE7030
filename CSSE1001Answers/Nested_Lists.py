def recursiveRef(nested,a_list):
    foo = len(a_list)
    print foo

    if foo==1:
        return nested[a_list[0]]
    else:
        
        return recursiveRef(nested[a_list[0]],a_list[1:foo])
    
