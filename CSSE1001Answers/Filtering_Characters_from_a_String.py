def is_in(char, string):
    """Return True iff char is in string

    is_in(char, string) -> bool

    """
    for c in string:
        if c == char:
            return True
    return False


def filter_string(str1, str2):
    """Return a copy of str1 with characters from str2 removed.

    filter_string(string, string) -> string
    """
    # add your code here
    answer = ''
    for letter in str1:
 
        if not is_in(letter,str2):
            answer = answer+letter
    return answer
