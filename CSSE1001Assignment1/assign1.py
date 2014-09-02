
###################################################################
#
#   CSSE1001/7030 - Assignment 1
#
#   Student Number: s342261
#
#   Student Name: Joseph Andersen
#
###################################################################

#####################################
# Support given below - DO NOT CHANGE
#####################################

from assign1_support import *
from datetime import *
#####################################
# End of support 
#####################################

# Add your code here

def load_data(dateStr):
    """Takes a string representing a date in the correct format
    returns a list of the data for each minute of the day in order

    load_data(string) -> list_of_4-tuples

    precondition: string refers to a valid date in dd/mm/yyyy format
    (or d/mm/yyyy, dd/m/yyyy, d/m/yyyy)

    This function gets the data from the server, using the
    appropriate support function, as a string of CSV and converts
    to the required data structure"""

    #load the raw data using the support function
    
    data = get_data_for_date(dateStr)

    #seperate the data by time record - each time is a 'word'
    data = data.split()

    #read in each 'word' of data, process into the appropriate
    #format. Store in 'answer'

    answer = []

    for word in data:
        
        letters = word.split(',')
        
        time = letters[0]
        temperature = float(letters[1])
        sunlight = float(letters[2])
        tuple_of_powers = (int(letters[3]),)
        for j in range(4,len(letters)):
            
            tuple_of_powers += (int(letters[j]),) 
        answer_tuple = (time,temperature,sunlight,tuple_of_powers)
        answer.append(answer_tuple) 

    return answer

def max_temperature(data):
    """Takes the data produced by load_data and returns a pair
    consisting of the maximum temperature and the list of times when
    the temperature was maximum.

    precondtion: data is list of 4-tuples produced by load_data

    max_temperature(list_of_4-tuples) -> (float,list)"""
    
    max_temp = 0 
    for a_tuple in data:
        if a_tuple[1] > max_temp:
            max_temp = a_tuple[1]
    times = []
    for a_tuple in data:
        if a_tuple[1] == max_temp:
            times.append(a_tuple[0])
    return (max_temp,times)
    

def total_energy(data):
    """takes the data produced by load_data and returns the total
    power produced (in kWhr) by all the arrays over the entire day.

    precondtion: data is list of 4-tuples produced by load_data

    total_energy(list_of_4-tuples) -> float"""
    total_power = 0
    for a_tuple in data:
        powers = a_tuple[3]
        for array_power in powers:
            total_power += array_power/60000.0
    return total_power

def maximum_power(data):
    """takes the data produced by load_data and returns the list of
    pairs of array names and maximum power for the day for that array
    in kW.

    precondtion: data is list of 4-tuples produced by load_data

    maximum_power(list_of_4-tuples) -> list_of_pairs"""

    max_powers = []

    for count,array_name in enumerate(ARRAYS):
        max_power = 0
        for a_tuple in data:
            powers = a_tuple[3]
            array_power = powers[count]
            if array_power > max_power:
                max_power = array_power
        max_powers.append((array_name,max_power/1000.))

    return max_powers

def display_stats(date):
    """takes a date in the correct format and prints out the required
    statistics.

    precondition: date is a string referring to a valid date in dd/mm/yyyy format
    (or d/mm/yyyy, dd/m/yyyy, d/m/yyyy)

    display_stats(string) -> none"""

    #get the data in from the server
    
    data = load_data(date)

    #get the maximum temperatures

    max_temps = max_temperature(data)

    maximum_temperature = max_temps[0]
    times = max_temps[1]
    time_string = ''
    for time in times:
        time_string += time+', '
    time_string = time_string[:-2]
    max_temp_string = 'Maximum temperature: '+str(maximum_temperature)+'C at times '+time_string

    #get the maximum power outputs

    max_powers = maximum_power(data)
    
    #output the data
    print
    print 'Statistics for',date
    print
    print max_temp_string
    print
    print 'Maximum Power Outputs'
    print

    for an_array in max_powers:
        """
        #I'm guessing the required length...
        array_string  = '                                         '
        power_string = '%.1fkW' %an_array[1]
        array_string = an_array[0] + array_string[len(an_array[0]):]
        array_string = array_string[:-(len(power_string))]+power_string

        
        print array_string
        """
        print STATS_ROW.format(an_array[0], an_array[1])

    
def display_weekly_stats(start_date):
    """takes a start date and prints out the information for the 7 days
    from that date

    precondtion: start_date is a string and refers to a valid date in
    dd/mm/yyyy format
    (or d/mm/yyyy, dd/m/yyyy, d/m/yyyy)

    display_weekly_stats(start_date) -> none"""

    print WEEKLY_HEADER
    
    date_strings = []
    start_date_date = datetime.strptime(start_date,DATE_FORMAT)

    #generate list of date_strings from start_date for 7 days
    for j in range(0,7):
        time_step = timedelta(days=j)
        a_date = datetime.strftime(start_date_date+time_step,DATE_FORMAT)
        #print a_date
        

        #generate daily stats for each day
        #print a_date
        #print type(a_date)
        data = get_max_data(a_date)
        data = data.split(',')
        max_temp = float(data[1])
        max_sun = float(data[2])
        max_powers = (data[3:])
        max_power =0
        for a_power in max_powers:
            max_power += float(a_power)
        #print the daily stats
      
        print WEEKLY_ROW.format(a_date,max_temp,max_sun,max_power/1000.0)


    
    pass
    



def get_command():
    """ this function prompts the user for input and preps the input to
    be used in interact

    get_command() -> [string]
    
    
"""
    command = raw_input('Command: ')
    command = command.strip()
    command = command.split( )

    return command



def interact():
    """ top-level function defining the text-based user interface

    valid commands q - quit; date 'date_string' - displays stats for
    the date specifed; week 'date_string' - displays statistics for the
    week beginning on the specified date.

    It is assumed that te date is entered as a string referring to a
    valid date in dd/mm/yyyy format
    (or d/mm/yyyy, dd/m/yyyy, d/m/yyyy)

    other commands will display an error and prompt the user to try again.

"""

    
    print 'Welcome to PV calculator'
    print
    print
    

    
    command = get_command()

    
    flag = True #flag is designed to be false when a valid command is detected
    while command[0] != 'q':     
        
        if len(command) !=2:
            flag = True
        elif command[0] == 'date':
            date_string = command[1]
            display_stats(date_string)
            flag = False
        elif command[0] == 'week':
            date_string = command[1]
            display_weekly_stats(date_string)
            flag = False

        if flag:
            print 'Unknown command:', ' '.join(command)

        command = get_command()
     
     
    
##################################################
# !!!!!! Do not change (or add to) the code below !!!!!
# 
# This code will run the interact function if
# you use Run -> Run Module  (F5)
# Because of this we have supplied a "stub" definition
# for interact above so that you won't get an undefined
# error when you are writing and testing your other functions.
# When you are ready please change the definition of interact above.
###################################################

if __name__ == '__main__':
    interact()

