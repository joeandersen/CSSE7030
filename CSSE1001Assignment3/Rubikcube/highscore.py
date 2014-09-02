'''
BBCUBER'S CUBE
Copyright (c) 2008, Josh Hicks
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. 
Neither the name of Josh Hicks nor the names of his contributors may be used to endorse or promote products derived from this software without specific prior written permission. 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

from Tkinter import *

class HighScore(Frame):
    '''
    class for storing high score information


    displays a matrix of labels with the highscore information
    these labels are bound so that they run a function
    that is given by the parent in constructor
    this function will generate a response in the human replay screen
        
    '''
    def __init__(self, frame, func, records):
        '''
        makes a highscore frame in a given widget with a pointer to a function
        init(frame, func) --> void
        '''
        #make highscore
        Frame.__init__(self, frame)

        #link to records
        self.replay = records

        #update it
        self.update()

        #give link to function
        #instead of link to parent
        self.func = func
            
    def update(self):
        '''
        update the highscore frame
        update(bool) --> void
        '''

        #set up empty lists
        self.highscores = []
        self.records = {}
        self.links = {}

        #for name, value
        for n,v in self.replay.returndata():
            self.highscores.append(Record(n,v))
        
        #sort the highscores
        self.highscores.sort()

        #for the first 10 (or less) highscores
        for i in range(min(10, len(self.highscores))):

            #empty array
            self.records[i] = []
            #add label with number
            self.records[i].append(Label(self, text = i+1, width = 5))

            #add label with time
            self.records[i].append(Label(self,
                text = self.highscores[i].getTime(), width = 14,anchor = E))

            #add label with name
            self.records[i].append(Label(self,
                text = self.highscores[i].name, width = 30))

            #bind all labels to self.click
            #grid all labels
            #store reference for their row number
            for j in range(3):
                self.links[self.records[i][j]] = i
                self.records[i][j].grid(row = i, column = j)
                self.records[i][j].bind('<Button-1>', self.click)

    def click(self, event):
        '''
        when clicked return the row the label is in
        click(event) --> void
        '''
        #run the function setup in init (points to something in parent)
        #shows the record linked with row number
        self.func(self.links[event.widget])
        
class Record:
    def __init__(self, name, val):
        '''
        make a new record from msg
        init(str) --> void
        pre req msg in right format

        the main purpose of records is converting
        second time values into strings that can
        be shown throughout the game.
        Usually a dummy instance is made as a
        converter.
        
        '''

        self.name = name

        self.value = val
        
    def __lt__(self,other):
        '''
        compares records based on time val
        lt(record) --> bool
        '''
        return self.value < other.value

    def getTime(self):
        '''
        get time value in xh xm xs format
        getTime() --> str
        '''

        #msg is the number of seconds
        msg = self.value

        #now change it

        #if it is less than -10 make it 10
        if msg < -10: msg = 10

        #if it is negative invert it
        elif msg < -1: msg = -int(msg)

        #if it is 0 make it 'GO!'
        elif msg < 0:
            msg = 'GO!'

        #otherwise put it in xxh xxm xxs with optional parts
        else:

            #get h,m,s values
            secs = msg%60
            mins = msg%3600/60
            hours = msg/3600

            #make different string parts
            secsmsg = ''
            minsmsg = ''
            hoursmsg = ''

            #if there needs to be 2 second digits
            if secs < 10 and not msg < 10:
                secsmsg = '0%.1fs'%(secs)
            else:
                secsmsg = '%.1fs'%(secs)

            #if time >= 1 min
            if msg >= 60:
                #if there only needs to be 1 digit
                if msg < 600:
                    minsmsg = '%dm'%(mins)
                else:
                    minsmsg = '%.2dm'%(mins)

            #add the h on to hours if time > 1 hour
            if msg >= 3600:
                hoursmsg = '%dh'%(hours)

            #string them together
            msg = '%s %s %s'%(hoursmsg, minsmsg, secsmsg)

        #return the string
        return msg
                  
'''
root = Tk()
app = HighScore(root)
app.pack()
root.mainloop()
'''
