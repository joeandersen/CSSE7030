def add_sizes(strings):
    """Return the list of pairs consisting of the elements of strings together
    with their sizes.

    add_sizes(list<string>) -> list<(string, integer)>
    """
    answer = []
    for str in strings:
        answer.append((str,len(str)))
    return answer
    
