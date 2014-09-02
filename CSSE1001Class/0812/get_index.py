def get_index(c, string):
    """Return the indices of c in string

    get_index(str, str) -> tuple of int

    precondition: c is in string (which my version should check for now)"""

    answer = ()

    if c in string:
        for number,character in enumerate(string):
            if character==c:
                answer += (number,)
            

    else:
        answer = 'c not in string'
        """Should throw an exception"""

    return answer
