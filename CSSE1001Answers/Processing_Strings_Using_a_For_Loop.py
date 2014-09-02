def occurrences(text1, text2):
    """Return the number of times characters from text1 occur in text2

    occurrences(string, string) -> int
    """
    # add your code here
    sum = 0;
    for letter in text2:
        if is_in(letter,text1):
            sum = sum+1
    return sum



def is_in(char, string):
    """Return True iff char is in string

    is_in(char, string) -> bool

    """
    for c in string:
        if c == char:
            return True
    return False
