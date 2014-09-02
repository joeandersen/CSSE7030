def get_digits(str1):
    """Return the digits of str1.

    get_digits(string) -> string
    """

    answer = ''
    for j in str1:
        if j.isdigit()==1:
            answer = answer+j

    return answer
