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
from math import *
from Visual import *
from ModelPointers import *
from piecesolve import *
from highscore import *
from visualreplay import *
from tkColorChooser import askcolor
import tkFileDialog
import webbrowser

class MyApp:
    def __init__(self,parent):
        '''
        My app is the controller of the cube program
        it contains a menu, two main frames, name entry and various labels
        it links everything together in a running application
        __init__(MyApp, tk) --> void
        '''

        #setup the red cross for the app
        parent.protocol('WM_DELETE_WINDOW',self.finished)

        #change the title of the app
        parent.wm_title("BBCUBER'S CUBE")

        #change the icon of the 
        parent.wm_iconbitmap('icon.ico')

        #create a link back to the parent
        self.parent = parent

        #set up a frame to hold everything
        self.frame = Frame(parent)
        self.frame.pack()

        #setup the main model (for the speedsolver)
        self.model = Model(None)
        self.model.reset()

        #setup the name entry
        self.namevar = StringVar()
        self.namevar.set('default')
        self.name = Entry(self.frame, width = 20, textvariable = self.namevar)
        self.name.grid(row = 1, column = 0)
        self.name.bind("<Control-z>", self.setss)

        #set the gamestate
        self.gamestate = StringVar()
        self.gamestate.set('solved')

        #setup the timer
        self.timer = Label(self.frame, width = 26, text = 'PRESS SPACE TO SCRAMBLE',
                    anchor = E)
        self.starttime = time()+10
        self.timer.grid(row = 1, column = 1)

        #label that shows information for the right canvas
        self.repinfo = Label(self.frame, width = 26)
        self.repinfo.grid(row = 1, column = 2)

        #label that shows information for the right canvas
        self.repcontrol = Label(self.frame, width = 26)
        self.repcontrol.grid(row = 1, column = 3)
        self.repcontrol.config(text = 'Highscores')

        #setup the left canvas    
        self.view = Cube(self.frame, self.updaterecord)
        self.view.grid(row = 0, column = 0, columnspan = 2)
        self.view.focus_set()
        #bind the name entry so enter changes focus
        self.name.bind('<Return>', lambda x:self.view.focus_set())

        #init the replayview widget
        self.replayview = Cube(self.frame)

        #init the humanreplay canvas
        self.humanreplay = ReplayCube(self.frame)
        self.record = ReplayData(self.namevar.get(),
                   eval(str(self.model.getData())))

        #init the highscore widget
        self.highscores = HighScore(self.frame, self.loadreplay,
                                self.humanreplay)
        self.highscores.grid(row = 0, column = 2)

        #init the info widget
        self.info = Frame(self.frame)
        self.infobox = Label(self.info, anchor = W)
        self.infobox.pack(fill = 'both')

        #init the model for the replayvisual
        self.replaymodel = Model(None)
        self.replaymodel.reset()

        #init the solver
        self.piecesolve = PieceSolver(None)
        self.piecesolve.setup()

        #link the inputs to the view
        self.clink = {}
        for f in [self.model, self.replaymodel]:
            self.clink[f] = {'U1': f.U1, 'U2': f.U2, 'U3': f.U3,
                      'F1': f.F1, 'F2': f.F2, 'F3': f.F3,
                      'L1': f.L1, 'L2': f.L2, 'L3': f.L3,
                      'D1': f.D1, 'D2': f.D2, 'D3': f.D3,
                      'B1': f.B1, 'B2': f.B2, 'B3': f.B3,
                      'R1': f.R1, 'R2': f.R2, 'R3': f.R3}

        #setup controls
        self.controls = {'j': 'U1', 'f': 'U3',
                         'e': 'L3', 'd': 'L1',
                         'g': 'F3', 'h': 'F1',
                         'i': 'R1', 'k': 'R3',
                         'w': 'B1', 'o': 'B3',
                         's': 'D1', 'l': 'D3'}

        #bind the controls
        for c in self.controls:
            self.view.bind(c, self.keyinterp)

        self.view.bind('x', self.solve)
        self.replayview.bind('<Right>', self.replaysolve)
        self.replayview.bind('<Left>', self.replayunsolve)
        self.view.bind('<space>', self.scramble)
        self.view.bind('<Control-s>', self.savecube)
        self.view.bind('<Control-o>', self.opencube)
        

        #remember the initial colour of the widget
        self.defclr = parent.cget("bg")
        self.customcolour = \
            ['white', 'red', 'green', 'yellow', 'orange', 'blue']

        #####MENU STUFF####        
        self.menubar = Menu(parent)
        
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Reset",
            command = self.reset)
        self.filemenu.add_command(label="Open",
            command = self.opencube)
        self.filemenu.add_command(label="Save",
            command = self.savecube)
        self.filemenu.add_command(label="Times",
                command = self.showhighscoreinfo)
        self.filemenu.add_command(label="Exit",
                command = self.finished)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.colourscheme = IntVar()
        self.colourscheme.set(0)

        self.colourmenu = Menu(self.menubar, tearoff=0)
        self.colourmenu.add_radiobutton(label="Config 1",
            value = 0, variable = self.colourscheme,
                command = self.changecolour)
        self.colourmenu.add_radiobutton(label="Config 2",
            value = 1, variable = self.colourscheme,
                command = self.changecolour)
        self.colourmenu.add_radiobutton(label="Config 3",
            value = 2, variable = self.colourscheme,
                command = self.changecolour)
        self.colourmenu.add_radiobutton(label="Custom",
            value = 3, variable = self.colourscheme,
                command = self.changecolour)
        self.colourmenu.add_separator()
        self.colourmenu.add_command(label = "Customize",
            command = self.pickcolour)
        self.colourmenu.add_command(label = "Background",
            command = self.pickbg)
        
        self.menubar.add_cascade(label="Colour",menu = self.colourmenu)

        self.solvemeth = StringVar()
        self.solvemeth.set('pieces')

        self.solvemenu = Menu(self.menubar, tearoff=0)
        self.solvemenu.add_command(label="Solve",
            command = self.solve)
        self.solvemenu.add_separator()
        self.solvemenu.add_radiobutton(label="Pieces",
            value = 'pieces', variable = self.solvemeth)
        self.solvemenu.add_radiobutton(label="Petrus",
            value = 'Petrus', variable = self.solvemeth)
        self.solvemenu.add_radiobutton(label="Heise",
            value = 'Heise', variable = self.solvemeth)
        self.solvemenu.add_radiobutton(label="Fredrich",
            value = 'Fredrich', variable = self.solvemeth)
        self.menubar.add_cascade(label="Solve", menu=self.solvemenu)

        self.controlmenu = Menu(self.menubar, tearoff=0)

        self.speed = IntVar()
        self.speed.set(10)
        
        self.controlmenu.add_radiobutton(label = "Slow",
            value = 5, variable = self.speed,
            command = self.changespeed)
        self.controlmenu.add_radiobutton(label = "Medium",
            value = 10, variable = self.speed,
            command = self.changespeed)
        self.controlmenu.add_radiobutton(label = "Fast",
            value = 15, variable = self.speed,
            command = self.changespeed)

        self.controlmenu.add_separator()

        self.type = StringVar()
        self.type.set('block')
            
        self.controlmenu.add_radiobutton(label = "Abs",
            value = 'const', variable = self.type,
            command = self.changespeed)
        self.controlmenu.add_radiobutton(label = "Rel",
            value = 'block', variable = self.type,
            command = self.changespeed)
        self.controlmenu.add_radiobutton(label = "Jump",
            value = 'jump', variable = self.type, 
            command = lambda: self.view.changeangle(90, 'block'))

        self.controlmenu.add_separator()

        self.controlmenu.add_command(label = 'Reset View',
            command = self.view.resetview)

        self.menubar.add_cascade(label="Controls", menu = self.controlmenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)

        self.helpmenu.add_command(label = 'About',
                                  command = self.about)
        self.helpmenu.add_command(label = 'Help',
                                  command = self.helpme)
        self.helpmenu.add_command(label = 'See Petrus Method',
                                  command = self.seepetrus)
        self.helpmenu.add_command(label = 'See Heise Method',
                                  command = self.seeheise)
        self.helpmenu.add_command(label = 'See Fredrich Method',
                                  command = self.seefred)
        
        self.menubar.add_cascade(label="Help", menu = self.helpmenu)
        
        parent.config(menu = self.menubar)

        #setup solver stuff
        self.solve()
        self.replaysolve()

#TEST
        self.timeconv = Record(0,'none')

                         
    def keyinterp(self, event):
        '''
        this is the handler for turns
        it is accessed from events when self.view is focused
        keyinterp(event) --> void
        '''

        #translate the controls depending on the orientation of the cube
        #because controls are relative to the cubes onscreen orientation
        #and the function are absolute moves
        move = self.controls[event.char]
        move = self.view.controls[move[0]] + move[1]
        #only do moves if the user is solving
        if self.gamestate.get() == 'solving':
            self.updaterecord(move)
            self.turn(self.clink[self.model][move])

    def turn(self, turnf):
        '''
        makes a face turn
        renders the new model
        checks to see if it is solved
        turn(function) --> void
        '''

        #run the face turn function
        turnf()

        #render the new colours
        self.render(self.view, self.model.getData())

        #check to see if it's complete
        a = self.model.getData()
        for i in range(12):
            a[i][1] = a[i][1]%2
        for i in range(8):
            a[i+12][1] = a[i+12][1]%3

        #if it is complete:
        if self.model.getData() == [[i,0] for i in (range(12) + range(8))]:

            #store the finishing time
            endtime = time() - self.starttime

            #stop the timer
            self.timer.after_cancel(self.timedevent)

            #show the endtime in the timer label
            self.timerstuff(endtime)

            #set the state to solved
            self.gamestate.set('solved')

            #do highscore and record updating                
            self.record.time = endtime
            self.humanreplay.records.append(self.record)
            self.highscores.update()

            #show the scores
            self.showhighscoreinfo()

    def replayunsolve(self, event = None):
        '''
        go back a step for the ai solve
        replaysolve() --> void
        '''

        #if there is a move to undo
        if len(self.unsolvearray) > 0:

            #put the inverted move into the front of the solvelist
            move = self.unsolvearray.pop(0)
            self.solvearray.insert(0, move[0] + str(4-int(move[1])))

            #turn the cube
            self.clink[self.replaymodel][move]()

            #change the text showing how far through the solve you are
            if self.repcontrol.cget('text') == 'AI replay':
                self.updatereplayinfo()

        #render the cube
        self.render(self.replayview, self.replaymodel.getData())

    def replaysolve(self, event=None):
        '''
        go forward a step in the computer solve
        replaysovle() --> void
        '''

        #if there is a step to go forward
        if len(self.solvearray) > 0:

            #store the inverted move in the undo list
            move = self.solvearray.pop(0)
            self.unsolvearray.insert(0, move[0] + str(4-int(move[1])))

            #move the model
            self.clink[self.replaymodel][move]()

            #change the label showing how far through the solve you are
            self.updatereplayinfo()
        else:
            self.showhighscoreinfo()

        #change the colours in the view
        self.render(self.replayview, self.replaymodel.getData())

        #just make sure that the orientations are correctly modded
        a = self.replaymodel.getData()
        for i in range(12):
            a[i][1] = a[i][1]%2
        for i in range(8):
            a[i+12][1] = a[i+12][1]%3
    
    def solve(self, event=None):
        '''
        solve the cube currently in the view window
        show the solved canvas on the right
        '''

        if event <> None and self.gamestate.get() == 'solved':
            return

        #put the cube data into newdat1/2
        #this is because the solver will change this data
        #and you don't want to link it to the speedsolving model
        dat = self.model.getData()
        newdat = []
        newdat2 = []
        for i in dat:
            newdat.append([i[0],i[1]])
            newdat2.append([i[0],i[1]])

        solvedat = []

        #if the solving method is pieces then solve it using pieces
        if self.solvemeth.get() == 'pieces':
            self.piecesolve.data = newdat
            solvedat = self.piecesolve.solveCorner()

        #set up the solve and undo arrays
        self.solvearray = []
        self.unsolvearray = []
        for i in range(len(solvedat)/2):
            if solvedat[:2] <> 'I0':
                self.solvearray.append(solvedat[:2])
            solvedat= solvedat[2:]

        #set the data to the original and show it
        self.replaymodel.data = newdat2

        #if the cube isn't already solved
        if self.gamestate.get() <> 'solved':
            #show the canvas
            self.forgetme(self.replayview)
            self.replayview.focus_set()

            #render the canvas with the original data
            self.render(self.replayview, newdat2)

            #show how many moves the solve is
            self.updatereplayinfo()

            #change the text to say AI replay
            self.repcontrol.config(text = 'AI replay')

    def updatereplayinfo(self):
        '''
        show currentmove/solvelength in the repinfo label
        updatereplayinfo() --> void
        '''

        self.repinfo.config(text = '%d / %d' %(len(self.unsolvearray),
                len(self.unsolvearray)+len(self.solvearray)))

    def showhumanreplay(self):
        '''
        show the humanreplay canvas
        configure the repcontrol label text
        showhumanreplay() --> void
        '''
        #show the canvas
        self.forgetme(self.humanreplay)
        #change the label
        self.repcontrol.config(text = 'Human replay')

    def showhighscoreinfo(self):
        '''
        show the highscore canvas
        change the text in the labels to match
        showhighscoreinfo() --> void
        '''
        #show the canvas
        self.forgetme(self.highscores)

        #change the right label
        self.repcontrol.config(text = 'Highscores')

        #change the left label
        self.repinfo.config(text = '')

        #set focus back to speedsolver
        self.view.focus_set()
        

    def scramble(self, event=None):
        '''
        scramble the cube
        scramble() --> void
        '''

        #scramble the model
        self.model.scramble()

        #render the scrambled model
        self.render(self.view,self.model.getData())

        #if the timer is going stop it
        if self.gamestate.get() in ['solving','looking']:
            self.timer.after_cancel(self.timedevent)

        #start the timer and change the gamestate
        self.timerstuff()
        self.gamestate.set('looking')

        #start recording this with the name in the namelist
        self.record = ReplayData(self.namevar.get(),
            eval(str(self.model.getData())))

        #give 10 seconds + 1 second 'go' to look
        self.starttime = time()+11

        #save the position of the cube
        self.updaterecord()
    
    def reset(self, event=None):
        '''
        reset the cube to play again
        reset() --> void
        '''

        #reset the model
        self.model.reset()

        #render the view
        self.render(self.view, self.model.getData())

        #if running stop the timer
        if self.gamestate.get() in ['solving','looking']:
            self.timer.after_cancel(self.timedevent)

        #change the text of the timer
        self.timer.config(text = "PRESS SPACE TO SCRAMBLE")

        #set the gamestate
        self.gamestate.set('solved')

    def finished(self, event = None):
        '''
        exit the game
        finished() --> void
        '''
        #save the highscores and replays
        self.humanreplay.saverecords()

        #save the new move combos
        for i in range(1,19):
            self.piecesolve.writefilestep(i)

        #quit
        self.parent.quit()
        self.parent.destroy()

    def changecolour(self):
        '''
        sets the colour depending on the coloursheme option
        changecolour() --> void
        '''

        #set the speedsolver colours
        self.view.colours = [
            ['white', 'red', 'green', 'yellow', 'orange', 'blue'],
            ['white', 'orange', 'green', 'yellow', 'red', 'blue'],
            ['white', 'green', 'orange', 'blue', 'yellow', 'red'],
            self.customcolour][self.colourscheme.get()]

        #set the colours for the other cubes
        self.replayview.colours = self.view.colours
        self.humanreplay.colours = self.view.colours

        #render all the cubes
        self.render(self.view, self.model.getData())
        self.render(self.replayview, self.replaymodel.getData())
        self.render(self.humanreplay, self.humanreplay.model.getData())

    def pickcolour(self):
        '''
        runs through a series of pickcolour screens
        lets you customize the colour of the cube
        changecolour() --> void
        '''

        #face and title for the different screens
        for f,t in [(0,"Top Face"),(1,"Front Face"),(2,"Left Face"),
                  (3,"Down Face"),(4,"Back Face"),(5,"Right Face")]:
            
            #if a colour was picked change the colour
            c2, colour = askcolor(self.customcolour[f], title=t)
            if c2:
                self.customcolour[f] = c2
            if colour:
                self.customcolour[f] = colour

        #pick the customized colour option
        self.colourscheme.set(3)
        #update the cubes
        self.changecolour()

    def pickbg(self):
        '''
        pick a background colour for the cubes
        pickbg() --> void
        '''

        #check for a colour
        _, colour = askcolor(self.defclr, title = "Background")
        if colour:

            #update the replayview's bg
            self.replayview.config(bg = colour)

            #invert the colour to find the outline of stickers

            #setup map list
            invertlist = [i.__str__() for i in range(10)] +\
                ['a','b','c','d','e','f']

            #make new hex number
            msg = '#'
            for i in range(1,7):
                msg += invertlist[15-invertlist.index(colour[i])]

            #change the colours in all the cubes
            self.view.tlinecolour(msg)
            self.replayview.tlinecolour(msg)
            self.view.config(bg = colour, highlightcolor = msg)
            self.replayview.config(bg = colour, highlightcolor = msg)
            self.humanreplay.tlinecolour(msg)
            self.humanreplay.config(bg = colour, highlightcolor = msg)
            self.humanreplay.itemconfig(self.humanreplay.fd,
                                outline = colour, fill = msg)
            self.humanreplay.itemconfig(self.humanreplay.ps,
                                outline = colour, fill = msg)
            self.humanreplay.itemconfig(self.humanreplay.bkbk,
                                outline = colour, fill = msg)
            self.humanreplay.itemconfig(self.humanreplay.timer, fill = msg)

    def render(self, view, data):
        '''
        change the sticker colours in view to display some data
        render(Cube, list) --> void
        '''
        view.tcolours(self.view.tconvertdata(data))

    def changespeed(self):
        '''
        change the rotation speed of the cube
        '''

        #change the way the speedsolver and ai cubes rotate
        self.view.changeangle(self.speed.get(), self.type.get())
        self.replayview.changeangle(self.speed.get(), self.type.get())

        #reset these varibale for both of them
        #stops the cubes moving
        self.view.turnrepeat,self.view.turn = False, False
        self.view.lastchar, self.view.lasttype = None, None

    def timerstuff(self, setmsg = False):
        '''
        update the timer label
        timerstuff(self, float) --> void
        '''

        #show a certain number or get the time
        if setmsg: msg = setmsg
        else:      msg = time() - self.starttime

        if msg > 0: self.gamestate.set('solving')

        #convert the time to a nice format
        self.timeconv.value = msg
        msg = self.timeconv.getTime()     

        #set the timer
        self.timerdata = msg
        self.timer.config(text = msg)

        #if it wasn't a predefined message, update in 100 ms
        if not setmsg:
            self.timedevent = self.timer.after(100, self.timerstuff)

    def updaterecord(self, turn = False):
        '''
        make a new record
        if there is a turn, store turn data
        otherwise store orient data
        updaterecord(str) --> void
        '''
        #if in a state to record
        if self.gamestate.get()in['solving','looking']:

            #if there was a turn
            #store the turn info
            if turn:
                #store time, turn string and turn var
                nextentry = ([time()-self.starttime, 'turn', turn])
            else:
                #store time, move stirng and i,j and k vectors
                nextentry = ([time()-self.starttime, 'move',
                    map(int,self.view.i),
                    map(int,self.view.j),
                    map(int,self.view.k)])

            #add the record to the array
            self.record.append(nextentry)

    def loadreplay(self, number):
        '''
        load a replay into the right canvas
        loadreplay(int)-->void
        '''
        #load the record
        self.humanreplay.loadrecord(number)

        #show the replay canvas
        self.showhumanreplay()

        #reset the display
        self.humanreplay.funcbkbk()

        #change the repinfo info
        self.repinfo.config(text = "%s solve by %s"%\
                (self.highscores.highscores[number].getTime(),
                 self.highscores.highscores[number].name))

    def about(self):
        '''
        show basic about information in the right canvas
        about() --> void
        '''
        #show the info frame
        self.forgetme(self.info)
        
        #change the information
        msg = 'This program was created by Josh Hicks (41749450)\n'
        msg += 'Easter egg: name is a float...ctrl z'

        self.infobox.config(text = msg)

        self.repcontrol.config(text = 'INFORMATION')
        self.repinfo.config(text = '')
        
    def helpme(self):
        '''
        show controls
        helpme() --> void
        '''

        #store temp array for msg

        temp = {}

        #add various rotational commands
        temp['X1'] = 't'
        temp['X3'] = 'b'
        temp['Y1'] = ';'
        temp['Y3'] = 'a'
        temp['Z1'] = 'p'
        temp['Z3'] = 'q'

        #invert the key/value for self.controls into temp
        for k,v in self.controls.iteritems():
            temp[v] = k

        #put heading Controls
        msg = 'Controls\n\n'

        #show list of all moves shown below
        for i in ['U','D','L','R','F','B','X','Y','Z']:
            msg += '%s1: %s\t %s3: %s\n' % (i,
                temp[i+'1'].upper(),i, temp[i+'3'].upper())

        #show scramble and solve controls
        msg += '\nScramble: space\nSolve: x\n'

        #show the ai replay controls
        msg += '\nAI replay controls: left, right'

        #configure the box to show the info
        self.infobox.config(text = msg)

        #change the repcontrol text to reflect the change
        self.repcontrol.config(text = 'CONTROLS')
        self.repinfo.config(text = '')

        #show the info frame
        self.forgetme(self.info)
            

    def forgetme(self, frame):
        '''
        sets a widget to show in row 0, col2
        forgetme(widget) --> void
        '''

        #forget all possible widgets that could be there
        self.highscores.grid_forget()
        self.humanreplay.grid_forget()
        self.info.grid_forget()
        self.replayview.grid_forget()

        #add the given widget
        frame.grid(row = 0, column = 2, columnspan = 2)

    def savecube(self, event = None):
        '''
        save the cube data to a file
        savecube() --> void
        '''

        #if it's not being solved then go out
        if self.gamestate.get() not in ['looking', 'solving']:
            return

        #store currenttime
        currenttime = time() - self.starttime

        #get a savefile
        savefile = tkFileDialog.asksaveasfilename()
        if savefile:
            msg = ''
            #add the model data
            msg += str(self.model.data) + '\n'
            #add the i, j and k vectors
            msg += str(self.view.i) + '\n'
            msg += str(self.view.j) + '\n'
            msg += str(self.view.k) + '\n'
            #add the currenttime
            msg += str(currenttime)
            #note that replay data is not saved

            #open and write the file
            f = open(savefile, 'w')
            f.writelines(msg)
            f.close()

    def opencube(self, event = None):
        '''
        open a cube file
        opencube() --> void
        precondition files in right format
        '''

        #find a file
        openfile = tkFileDialog.askopenfilename()

        try:
          if openfile:
            #start the cube running
            self.scramble()

            #open the file
            f = open(openfile)
            
            #first line is model data
            self.model.data = eval(f.readline())
            
            #next are the i,j and k vectors
            self.view.i = eval(f.readline())
            self.view.j = eval(f.readline())
            self.view.k = eval(f.readline())

            #then the time
            currenttime = eval(f.readline())

            #close the file
            f.close()

            #set the starttime so that it matches what it was before saving
            self.starttime = time()-currenttime

            #refresh the display
            self.render(self.view,self.model.getData())
            self.view.tmove()

            
        #in case of errors. may occur later, but don't expect bad files
        except: pass



    def seeheise(self):
        '''
        open website explaining heise method
        seeheise() --> void
        '''
        webbrowser.open_new_tab('http://www.ryanheise.com/cube/')
        
    def seepetrus(self):
        '''
        open website explaining petrus method
        seepetrus() --> void
        '''
        webbrowser.open_new_tab('http://www.lar5.com/cube/')

    def seefred(self):
        '''
        open website explaining fredrich method
        seefred() --> void
        '''
        webbrowser.open_new_tab(\
            'http://www.ws.binghamton.edu/fridrich/cube.html')

    def setss(self, event = None):
        '''
        sets the size of space between cube stickers
        setss() --> void
        '''

        for cube in [self.view, self.replayview, self.humanreplay]:
            try:
                cube.ss = float(self.namevar.get())
                cube.tmove()
            except:
                pass
                    

#run the app
root = Tk()
myapp = MyApp(root)
root.mainloop()
