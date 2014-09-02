
#create a string, with a 'number' in it
x = "There are %d types of people." % 10
binary = "binary"
do_not = "don't"

#create a string with two other strings in it
y = "Those who know %s and those who %s." % (binary,do_not)

#print them
print x
print y

#print more strings with 'raw' strings in them...
print "I said: %r." % x
print "I also said: '%s'." % y

#set hilarious to a boolean
hilarious = False

#define a string variable with a formatter in it
joke_evaluation = "Isn't that joke so funny?! %r"

#insert the bool into a string
print joke_evaluation % hilarious

w = "This is the left side of ..."
e = "a string with a right side."

#string concatenation
print w+e
