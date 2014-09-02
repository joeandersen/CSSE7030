
########################################################################
#                                                                      #
#  PolyominOhs!                                                        #
#  Code written by Nicholas Hughes except where noted.                 #
#                                                                      #
#  Permission is hereby granted, free of charge, to any person         #
#  obtaining a copy of this software and associated documentation      #
#  files (the "Software"), to deal in the Software without             #
#  restriction, including without limitation the rights to use,        #
#  copy, modify, merge, publish, distribute, sublicense, and/or sell   #
#  copies of the Software, and to permit persons to whom the           #
#  Software is furnished to do so.                                     #
#                                                                      #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,     #
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES     #
#  OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND            #
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR        #
#  ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF      #
#  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION  #
#  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.     #
#                                                                      #
########################################################################


""" helpers.py: A few helper functions and classes which are used by multiple
other classes and so don't belong anywhere else. """


def rect_list(width, height, value=None):
    """ Return a rectangular 2D list of size width * height, filled with value
    and indexed by [row][column].
    
    rect_list(int, int, object) -> list<list<object>>
    """
    
    rect_list = []
    for i in xrange(height):
        rect_list.append([])
        for j in xrange(width):
            rect_list[i].append(value)
    return rect_list


class Point:
    
    """ A 2D point. Used mostly as a position vector. """
    
    def __init__(self, x, y):
        """ Initialise the point with the x and y co-ordinates given.
        
        __init__(int, int) -> void
        """
        
        self.x = x
        self.y = y
    
    def __repr__(self):
        return 'Point(%d, %d)' % (self.x, self.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __ne__(self, other):
        return not self.__eq__(other)
