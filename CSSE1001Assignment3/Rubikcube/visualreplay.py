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

from Visual import *
from time import *
from highscore import *


class ReplayCube(Cube):
    '''
    replaycube is the widget that deals with replays
    consists of a cube that replays itself
    and a control panel with stop(bkbk), pause and play(fd)


    the cube stores data as [time, str, params]
    depending on the string, it will run the params differently
    if str is turn, it will just turn the right face
    if str is move, it will copy the values into i,j and k vectors

    when it has completed a move, it will call itself back when the
    next instruction is due to happen. if it is behind, this has the
    result of it catching up. This means that it balances out, and is
    accurate enough and easy to understand and implement.

    when it is paused, it stores the equivilant of an offset value
    so that when it is started again, it can run to the same point

    when unpausing, the program just runs through all steps until it
    reaches the correct position

    '''
    def __init__(self, master):
        '''
        init the cube
        disable bindings
        add controls and bind them
        '''
        Cube.__init__(self, master)

        for bindchar in ['a', 'q', 't', ';', 'b', 'p']:
            self.unbind(bindchar)
            self.unbind("<KeyRelease-%s>"%bindchar)

        #make it so the widget cannot be selected
        self.config(takefocus = 0)
        #list for records
        self.records = []
        #load list from file
        self.openrecords()
        #sort the list
        self.records.sort()

        #abs reference for controls
        x = 150-28
        y = 290

        ##SETUP CONTROLS##

        #coordinates for a step back polygon
        self.bkbk = self.create_polygon(x+10, y, x+15, y-5, x+15, y,
            x+20, y-5, x+20, y+5, x+15, y, x+15, y+5)

        #coordinates for a pause button
        self.ps = self.create_polygon(x+25, y+5, x+25, y-5, x+27, y-5,
            x+27, y+5, x+29, y+5, x+29, y-5, x+31, y-5, x+31, y+5)

        #coordinates for a forward button
        self.fd = self.create_polygon(x+36, y+5, x+41, y, x+36, y-5)

        #bind mouseclick
        self.bind("<Button-1>", self.clickhandle)

        #set init state
        self.playstate = 'bk'
        self.stoptime = 0
        self.current =0 

        #make a timer
        self.timer = self.create_text(100,20, text = 'hi there')

        #make a time converter
        self.timeconv = Record(0,'none')

        self.model = Model()

    def updatetimer(self):
        '''
        update the timer
        updatetimer()-->void
        '''

        #get the new timevalue to display
        newtime = time()-self.playtime+self.currentrecord[0][0]

        #store it in the record
        self.timeconv.value = newtime

        #edit the text
        self.itemconfig(self.timer, text = self.timeconv.getTime())

        #if not on last instruction
        if self.instruction < len(self.currentrecord)-1:
            #repeat in 20 ms
            self.stoptimer()
            self.timedevent = self.after(20, self.updatetimer)
        #otherwise
        else:
            #set the value of the timer to the recorded endtime
            self.timeconv.vaule = self.currentrecord.time
            #update the text
            self.itemconfig(self.timer, text = self.timeconv.getTime())
        
    def openrecords(self):
        '''
        read the records from the files
        openrecords() --> void
        '''
        #try to open the 10 files
        for i in range(10):
            try:
                #open, read and close file
                f = open('replays\\highrec%d.txt'%i, 'r')
                record = f.readlines()
                f.close()

                
                recordc1 = []

                #for every line, append it to recordc1
                for i in record:
                    recordc1.append(i.rstrip('\n'))

                #evaluate every line
                recordc2 = map(eval, recordc1)

                #take the summary data from the first line
                newrecord = ReplayData(*recordc2[0])

                #append the rest of the information
                for line in record[1:]:
                    newrecord.append(eval(line))

                #append the record
                self.records.append(newrecord)
            except:
                pass   

    def saverecords(self):
        '''
        save the top 10 records
        saverecords() --> void
        '''
        #for the top 10 (or less)
        for i in range(min(10,len(self.records))):
            #open the file
            f = open('replays\\highrec%d.txt'%i, 'w')
            #write with record.__repr__
            f.write(self.records[i].__repr__())
            #close the file
            f.close()        

    def funcfd(self):
        '''
        function handler for fd button
        setup replayvisual for play
        funcfd() --> void
        '''

        #state = fd
        self.playstate = 'fd'

        #set time val
        self.playtime = time() - self.stoptime

        #first instruction
        self.instruction = 0

        #run it
        self.runfd()

        #update the timer
        self.updatetimer()

        #redo the colours
        self.tcolours(self.tconvertdata(self.model.getData()))
     
    def runfd(self):
        '''
        while the cube is playing
        runfd() --> void
        '''

        #if it is playing
        if self.playstate == 'fd':

            #find the current instruction
            move = self.currentrecord[self.instruction]

            #if it's a move instruction
            if move[1] == 'move':

                #set the i,j and k vectors
                self.i = move[2]
                self.j = move[3]
                self.k = move[4]
                #render poly coords
                self.tmove()

            #if it's a turn instruction
            if move[1] == 'turn':
                #turn it
                eval("self.model."+move[2]+"()")
                #change polygon colours
                self.tcolours(self.tconvertdata(self.model.getData()))               

           #if not last instruction
            if self.instruction < len(self.currentrecord)-1:
                #increment instruction counter
                self.instruction += 1

                #find time till next instruction
                timeafter = self.currentrecord[self.instruction][0]-\
                    time() + self.playtime - self.currentrecord[0][0]

                #change to int in ms
                timeafter = int(timeafter*1000)

                #time next callback when next instruction should occur
                try: self.after_cancel(self.fdevent)
                except: pass
                self.fdevent = self.after(timeafter, self.runfd)
                
            else:
                #if done then pause
                self.timeconv.value = self.currentrecord.time
                self.itemconfig(self.timer,
                            text = self.timeconv.getTime())
                self.playstate = 'ps'
        

    '''def funcbk(self):
        print 'bk'''

    def funcps(self):
        '''
        pause the cube replay
        funcps() --> void
        '''

        #if playing
        if self.playstate == 'fd':
            #init from currenttime next play
            self.stoptime = time() - self.playtime
        else:
            #else start next timer from start
            self.stoptime = 0

        #gamestate = pause
        self.playstate = 'ps'
        #stop the timer
        self.stoptimer()

        #load the current record again
        self.loadrecord(self.current)

    '''
    def funcfdfd(self):
        print 'done'
        self.playstate = 'fdfd'
    '''
        

    def funcbkbk(self):
        '''
        reset the cube replay
        funcbkbk() --> void
        '''
        
        #set state fd
        self.playstate = 'fd'
        #load record again
        self.loadrecord(self.current)
        #run 1 step (orient cube)
        self.runfd()
        #stop the timer
        self.stoptimer()

        #init from start when play
        self.stoptime = 0
        #playstate is set to back
        self.playstate = 'bk'

        #rerender the colours
        self.tcolours(self.tconvertdata(self.model.getData()))

        #set the timer value
        self.timeconv.value = self.currentrecord[0][0]
        self.itemconfig(self.timer, text = self.timeconv.getTime())

    def stoptimer(self):
        '''
        stop the timer if it is active
        stoptimer() --> void
        '''
        try: self.after_cancel(self.timedevent)
        except: pass

        

    def clickhandle(self, event = None):

        '''
        handler for clicking on controls
        clickhandle(event) --> void
        '''

        #find the closest widget and run appropriate function
        ID = self.find_closest(event.x, event.y)[0]

        if ID == self.fd: self.funcfd()
        #if ID == self.bk: self.funcbk()
        if ID == self.ps: self.funcps()
        #if ID == self.fdfd: self.funcfdfd()
        if ID == self.bkbk: self.funcbkbk()

    def loadrecord(self, number):
        '''
        load a record from the list
        loadrecord(int) --> void

        pre congood num
        '''

        #store number
        self.current = number

        #sort records
        self.records.sort()

        #pointer to record
        r = self.records[number]
        
        #load modeldata with copy of initdata
        self.model = Model(eval(str(r.initdata)))

        #store currentrecord
        self.currentrecord = r

        #instruction to 0
        self.instruction = 0

        #set playtime
        self.playtime = time()+r[0][0]

    def returndata(self):
        '''
        give a list of name, value pairs
        returndata(self) --> list
        '''

        output = []

        #for all the records
        for i in self.records:
            output.append((i.name, i.time))

        return output
        
class ReplayData(list):
    '''
    replaydata is a list with name, initdata and time
    '''
    
    def __init__(self, name, initdata, time = 0, *args):
        '''
        init(str, list, flt, *(3tuple)) --> void
        '''

        list.__init__(self)

        #add args        
        for i in args:
            self.append(i)

        #add name, init and time data
        self.name = name
        self.initdata = initdata
        self.time = time

    def __lt__(self, other):
        '''
        comparison by time value
        lt(replaydata) --> bool
        '''
        return self.time < other.time

    def __repr__(self):
        '''
        give information for saving
        repr()-->str
        '''

        msg = str((self.name, self.initdata, self.time))

        #save only 2 dp for time to save space
        for i in self:
            msg = msg + "\n[%.2f, "%i[0] + str(i[1:])[1:]

        return msg

'''
root = Tk()
app = replayCube(root)
#app.configure()
root.mainloop()
'''
