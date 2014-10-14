#Pynances.py finance tracker application
#
#Designed to read in a text file containing previous balances, add in a new set of
#of balances and then plot various time serieses
#
#


def create_data(filename):
    """Initializes a data file"""
    pass

def add_account(filename,account_name):
    """adds a new account to the datafile"""
    pass


def read_data(filename):
    """opens up the data file specified and loads the contents into a list

    read_data(str) -> [(floats)]"""
    pass

def write_data(filename, data):
    """writes existing data to specified filename.

    write_data(str,[(floats)]) -> none"""
    pass
def plot_data(data):
    """plots the data"""
    pass

def add_data(data,new_data):
    """appends a new days worth of data to the data list"""
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

    print 'Welcome to Pynances'
    print
    print

    command = get_command()
    print command

    
    
    




















#Runs module in 'interactive mode'

if __name__ == '__main__':
    interact()
