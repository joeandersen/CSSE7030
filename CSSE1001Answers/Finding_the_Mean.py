def mean(numbers):
    running_total = 0
    number_of_elements = 0
    for number in numbers:
        running_total = running_total+number
        number_of_elements = number_of_elements+1
    return running_total/float(number_of_elements)
    
