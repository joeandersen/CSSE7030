
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


""" event_handler.py: Contains the Event_Handler class. """


from pygame.constants import *

import config


class Event_Handler:
    
    """ A class for handling events, including keyboard input. """
    
    def __init__(self, pygame):
        """ Initialise.
        
        __init__(pygame) -> void
        """
        
        self._pygame = pygame
        self._filter = [KEYDOWN, KEYUP, QUIT]
        self._filter.extend(config.CUSTOM_EVENTS)
    
    def clear_queue(self):
        """ Clear the events queue. """
        
        self._pygame.event.clear(self._filter)
    
    def get_events(self):
        """ Return all events which have occured since the method
        was last called, as a list. Events not useful are filtered out.
        
        get_events() -> list<pygame.event>
        """
        
        return [e for e in self._pygame.event.get() if e.type in self._filter]
