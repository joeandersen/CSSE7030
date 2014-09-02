if start>=end:
    ones = ''
    twos = ''
    back = ''
else:
    ones = text[start:end]
    twos = text[start:end:2]
    back = text[end:start:-1]
