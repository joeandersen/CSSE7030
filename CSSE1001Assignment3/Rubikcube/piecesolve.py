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


from ModelPointers import *
from random import *
from time import *

class PieceSolver(Model):
    '''
    solves the cube piece by piece
    starts at specific corner and puts in pieces piece by piece
    saves moves sequences for next time

    this solver works by iteratating a single model
    through every single combination to a given length
    if it finds a path it stops and returns the path as a string

    it uses turn, double turn, turn, double turn because
    double turns take less time to run
    this is especially true for front and back

    if there is no match, the cube will return to starting position
    this makes recursion easier
    
    '''

    #information for recursion
    array = [ 
        [Model.U1, 'U1', Model.U2, 'U3', Model.U3, 'U2'],
        [Model.D1, 'D1', Model.D2, 'D3', Model.D3, 'D2'],
        [Model.F1, 'F1', Model.F2, 'F3', Model.F3, 'F2'],
        [Model.B1, 'B1', Model.B2, 'B3', Model.B3, 'B2'],
        [Model.L1, 'L1', Model.L2, 'L3', Model.L3, 'L2'],
        [Model.R1, 'R1', Model.R2, 'R3', Model.R3, 'R2']]
    
    def solve(self, iterat, edges, corners, dont = ''):

        #make pointer to self.getData()
        dat = self.getData()

        #assume there is a match
        #go through until there isn't
        match = True
        for p in edges:
            if [dat[p][0],dat[p][1]%2] <> [p,0]:
                match = False
                break
        #if there is a match in edge, check for corners
        if match:
            for p in corners:
                if [dat[p+12][0], dat[p+12][1]%3] <>[p,0]:
                    match = False
                    break

        #if there is a match don't turn it
        if match:
            return 'I0'

        #if this is last iteration and no match return false
        if iterat == 0:
            return False 

        #this stuff should probably be moved outside the loop

        #recursive prototype
        f = lambda x: self.solve(iterat-1, edges, corners,x)

        #recurse through different cube combinations
        #if a match is found cube is left in position
        #else cube returned to starting position
        for i in self.array:

            #the letter of the turn
            l = i[1][0]

            #don't turn the same face twice
            if l <> dont:
                
                #turn face once cw
                i[0](self)
                #recurse
                a = f(l)
                #if there's a match return
                if a: return i[1] + a

                #double turn the face
                i[2](self)
                #recurse
                a = f(l)
                #if there's a match return
                if a: return i[3] + a

                #turn face once acw
                i[4](self)
                #recurse
                a = f(l)
                #if there's a match return
                if a: return i[5] + a

                #double turn face (total = I0)
                i[2](self)

    def minsolve(self,iterat, edges, corners):
        '''
        used to ensure that the solution reached is minimal
        minsolve(int, list, list) --> str
        '''

        #do solves for solvelengths up to iterat
        for i in range(iterat+1):

            #solve
            mindat = self.solve(i, edges, corners)

            #if solution return
            if mindat: return mindat

    def solveCorner(self):
        '''
        solve using corner method
        solveCorner() --> str
        '''
        path = ''

        #the different stages of solving an L shape
        stages = [
            [1,12, (3,[],[0])], #get corner 0 in place
            [2,0, (3,[0],[0])], #get e0 as well
            [3,1, (3,[0,1],[0])], #get e1
            [4,8, (3,[0,1,8],[0])], #get e8 (2x2x2 cube)
            [5,13,(3,[0,1,8],[0,1])], #get corner 1
            [6,2, (3,[0,1,8,2],[0,1])], #get e2
            [7,9, (3,[0,1,8,2,9],[0,1])], #get e9 (2x2x3 cube)
            [8,16,(3,[0,1,8,2,9],[0,1,4])], #get c4
            [9,4, (3,[0,1,8,2,9,4],[0,1,4])], #get e 4
            [10,5,(7,[0,1,8,2,9,4,5],[0,1,4])] # get e5 (L shape)
            ]

        #for all stages
        #stage is the stage number
        #num is the piece that is being moved
        #indat is the list of pieces you want to solve
        for stage, num, indat in stages:

            #store pointer to data
            dat = self.getData()

            #if it's an edge
            if num/12 == 0:
                #find the initial position and orientation of it
                for i in range(12):
                    if dat[i][0] == num:
                        initpos = str((i, dat[i][1]%2))
            #otherwise it is a corner
            else:
                #find the intial position and orientaiton of it
                for i in range(8):
                    if dat[i+12][0] == num-12:
                        initpos = str((i+12, dat[i+12][1]%3))

            #check against the saved paths
            if initpos in self.step[stage].keys():
                #if it is add the path to the solution
                path += self.step[stage][initpos]
                #and run the algorithm
                self.runalg(self.step[stage][initpos])

            #otherwise solve from scratch
            else:
                '''print initpos'''

                #solve for it
                next = self.minsolve(indat[0],indat[1],indat[2])

                #if there is a solution
                if next <> None:
                    #add it to the path
                    path += next
                    #add it to be saved
                    self.step[stage][initpos] = next
                else:
                    '''print str(stage)'''
                    break

        #fill in the last pillar
        stages = [
            [11,[17],8],
            [12,[6,17],10]
            ]

        #stage is the stage of solving
        #pieces is the piecenum
        #iterate gives how many
        for stage, pieces, iterat in stages:
            #pointer to data
            dat = self.getData()

            #empty str for initial pos of piece
            initpos = ''

            #find the initial position of the piece
            for i in range(20):
                if dat[i][0]+12*(i/12) == pieces[0]:
                    initpos += str((i,dat[i][1]%(2+pieces[0]/12)))

            #if it has already been solved
            if initpos in self.step[stage].keys():
                #add it to the path
                path += self.step[stage][initpos]
                #run the alg
                self.runalg(self.step[stage][initpos])
                
            #otherwise solve from scratch
            else:
                '''print initpos'''
                #solve it                       #previously solved pieces
                next = self.minsolve2(iterat,[0,1,8,2,9,4,5,12,13,16]+pieces)

                #if there is a solution
                if next <> None:
                    #add the path
                    path += next
                    #save the alg
                    self.step[stage][initpos] = next
                else:
                    '''print str(stage)'''
                    break

        #for the top layer
        stages = [
            [13,[],[3,7,10,11],11], #orient edges
            [14,[14,15],[3,7,10,11],11], #get 2 edges positioned
            [15,[14,15,18,19],[3,7,10,11],11], #get all edges positioned
            [16,[14,15,18,19],[3,7,10,11,14,15,18,19],15], #flip corners
            [17,[3,14,15,18,19],[3,7,10,11,14,15,18,19],14], #pos 1 edge
            [18,[3,7,14,15,18,19],[3,7,10,11,14,15,18,19],14] #solve
            ]

        #stage is stage
        #pos is list of pieces to be positioned
        #ori is list of pieces to be oriented
        #iterat is num iterations deep
        
        for stage, pos, ori, iterat in stages:

            #pointer to data
            dat = self.getData()
            initpos = ''


            ''' NO IDEA WHERE THIS CAME FROM :S
            #pieces to be fixed
            pieces = []
            for i in pos:
                if i not in pieces: pieces.append(i)
            for i in ori:
                if i not in pieces: pieces.append(i)'''

            #these various init poses just store the
            #unique current cube position for the data
            #mods are used to ensure that orientation is unique

            #initpos for st 13
            if stage == 13:
                initposarr = [(dat[3][1]%2+dat[3][0]/8)%2,
                              (dat[7][1]%2+dat[7][0]/8)%2,
                              (dat[10][1]%2+dat[10][0]/8+1)%2,
                              (dat[11][1]%2+dat[11][0]/8+1)%2]

            #initpos for st 14
            if stage == 14:
                initposarr = []
                for i in range(8):
                    if dat[i+12][0] == 2:
                        initposarr.append(i+12)
                for i in range(8):
                    if dat[i+12][0] == 3:
                        initposarr.append(i+12)

            #initpos for st 15
            if stage == 15:
                initposarr = []
                for i in range(8):
                    if dat[i+12][0] == 6:
                        initposarr.append(i+12)
                for i in range(8):
                    if dat[i+12][0] == 7:
                        initposarr.append(i+12)

            #initpos for st 16
            if stage == 16:
                initposarr = [dat[14][1]%3,
                              dat[15][1]%3,
                              dat[18][1]%3,
                              dat[19][1]%3]

            #initpos for st 17
            if stage == 17:
                initposarr = []
                for i in range(12):
                    if dat[i][0] == 3:
                        initposarr.append(i)

            #initpos for st 18
            if stage == 18:
                initposarr = [dat[7][0],
                              dat[10][0],
                              dat[11][0]]

            #initpos
            initpos = str(initposarr)

            #check for presolved
            if initpos in self.step[stage].keys():
                #add to path and run alg
                path += self.step[stage][initpos]
                self.runalg(self.step[stage][initpos])
            else:
                '''print initpos'''
                #try and solve
                next = self.minsolve3(iterat,pos,ori)
                #if solution
                if next <> None:
                    #add it and save it
                    path += next
                    self.step[stage][initpos] = next
                else:
                    '''print str(stage)'''
                    break

        #return the str for the path
        return path

    def solve2(self,iterat, pieces, dont = ''):
        '''
        solve2 uses less moves to solve within a subset faster
        solve2(int, array, str)
        '''

        #pointer to data
        dat = self.getData()

        #check for match
        match = True
        for p in pieces:
            if [dat[p][0],dat[p][1]%(2+p/12)] <> [p%12,0]:
                match = False
                break

        #if match return identity turn
        if match:
            return 'I0'

        #if iterated as far as can then return false
        if iterat == 0:
            return False 

        f = lambda x: self.solve2(iterat-1, pieces ,x)

        #3 turns for the L-shape
        for i in[ 
        [self.B1, 'B1', self.B2, 'B3', self.B3, 'B2'],
        [self.L1, 'L1', self.L2, 'L3', self.L3, 'L2'],
        [self.D1, 'D1', self.D2, 'D3', self.D3, 'D2']
        ]:

        #same as for solve but with less turns
            l = i[1][0]
            if l <> dont:
                fturn = i[1][0]
                i[0]()
                a = f(l)
                if a: return i[1] + a
                i[2]()
                a = f(l)
                if a: return i[3] + a
                i[4]()
                a = f(l)
                if a: return i[5] + a
                i[2]()
        

    def minsolve2(self,iterat, pieces):
        '''
        ensures minimum solve using solve2
        minsolve(int, list) --> str
        '''
        
        #same as minsolve(but runs solve2 instead)
        for i in range(iterat+1):
            mindat = self.solve2(i, pieces)
            if mindat: return mindat

    def solve3(self,iterat, positioned, oriented, dont = ''):
        '''
        used to solve last layer stuff
        some face turns should be commented out for speed
        otherwise this would take forever...but it would work eventually
        solve3(int, list, list, str)
        '''

        #pointer
        dat = self.getData()

        #check for match
        match = True

        #check initial pieces
        for p in [0,1,2,4,5,6,8,9,12,13,16,17]:
            if [dat[p][0],dat[p][1]%(2+p/12)] <> [p%12,0]:
                match = False
                break

        #check that pieces are poisionted
        if match:
            for p in positioned:
                if dat[p][0] <> p%12:
                    match = False
                    break

        #check orientation edges
        if match:
            for i in range(12):
                if dat[i][0] in oriented:
                    if dat[i][1]%2 <> (i/8+dat[i][0]/8)%2:
                        match = False
                        break

        #check orientation of corners
        if match:        
            for i in range(8):
                if dat[i+12][0]+12 in oriented:
                    if dat[i+12][1]%3 <> 0:
                        match = False
                        break

        #if match return identity turn
        if match:
            return 'I0'

        #else return false
        if iterat == 0:
            return False 

        f = lambda x: self.solve3(iterat-1, positioned, oriented ,x)

        '''for i in[
        [self.U1, 'U1', self.U2, 'U3', self.U3, 'U2'],
        [self.B1, 'B1', self.B2, 'B3', self.B3, 'B2'],
        [self.L1, 'L1', self.L2, 'L3', self.L3, 'L2'],
        [self.R1, 'R1', self.R2, 'R3', self.R3, 'R2'],
        [self.D1, 'D1', self.D2, 'D3', self.D3, 'D2'],
        [self.F1, 'F1', self.F2, 'F3', self.F3, 'F2']
        ]:'''
        for i in self.array:

          #same as other solve methods
            l = i[1][0]
            if l <> dont:
                fturn = i[1][0]
                i[0](self)
                a = f(l)
                if a: return i[1] + a
                i[2](self)
                a = f(l)
                if a: return i[3] + a
                i[4](self)
                a = f(l)
                if a: return i[5] + a
                i[2](self)
        

    def minsolve3(self,iterat, positioned, oriented):
        '''
        same as minsolve but with solve3
        minsolve3(int, list, list) --> str
        '''

        #for all lengths
        for i in range(iterat+1):
            #try and solve
            mindat = self.solve3(i, positioned, oriented,'F')
            #if solve return path
            if mindat: return mindat

    def readfilestep(self,stepnum):
        '''
        reads the paths that have already been solved
        readfilestep(int) --> void
        '''

        #make list to hold stage arrays if doesn't exist
        try: self.step
        except:
            self.step = {}

        #open file
        filename = "piecemeth\\step%d.txt"%stepnum
        f = open(filename,"r")

        #make empty list for stage
        self.step[stepnum] = {}

        #read the file
        for i in f.readlines():
            #get rid of the linebreak
            a = i.rstrip("\n")
            #get rid of the spaces
            a = a.split(' ')
            #add the info to the stage array
            self.step[stepnum][a[0]+' '+a[1]] = a[2]+'I0'
            
        #close the file
        f.close()

    def readfilestep2(self,stepnum):
        '''
        read a file to get stage info
        readfilestep2(int) --> void
        '''

        #open file
        filename = "piecemeth\\step%d.txt"%stepnum
        f = open(filename,"r")

        #empty stage list
        self.step[stepnum] = {}

        #read through the lines of the file
        for i in f.readlines():

            #get rid of the line breaks
            a = i.rstrip("\n")

            #split it into initpos and path
            a = a.split('] ')
            a[0] += ']'

            #add it to the stage array
            self.step[stepnum][a[0]] = a[1]+'I0'

        #close the file
        f.close()
        
    def writefilestep(self, stepnum):
        '''
        output new paths to the file
        writefilestep(int)--> void
        '''
        
        #empty msg
        msg = ''

        #for every initpos
        for i in self.step[stepnum]:
            #add the initpos and a space
            msg += str(i)
            msg += ' '

            #add the path and a newline char
            msg += self.step[stepnum][i][:-2]
            msg += "\n"


        #open file
        filename = "piecemeth\\step%d.txt"%stepnum
        f = open(filename,"w")
        #write the file
        f.write(msg)
        #close the file        
        f.close()

    def setup(self):
        '''
        setup the solver
        setup() --> void
        '''
        #F2L solving
        for i in range(1,13):
            self.readfilestep(i)
        #top layer solving
        for i in range(13,19):
            self.readfilestep2(i)

        #define the controls
        self.controls = {'U1':self.U1, 'U2':self.U2, 'U3':self.U3,
                         'D1':self.D1, 'D2':self.D2, 'D3':self.D3,
                         'L1':self.L1, 'L2':self.L2, 'L3':self.L3,
                         'R1':self.R1, 'R2':self.R2, 'R3':self.R3,
                         'F1':self.F1, 'F2':self.F2, 'F3':self.F3,
                         'B1':self.B1, 'B2':self.B2, 'B3':self.B3,
                         'I0':lambda: 0}

    def runalg(self, alg):
        '''
        run a list of turns
        runalg(str) --> void
        '''
        salg = alg
        
        #for the number of moves
        for i in range(len(alg)/2):
            #turn the cubes
            self.controls[salg[:2]]()
            #cut the list
            salg = salg[2:]
        
    '''def scramble(self):
        
        #scramble (should inherit from model)
        #scramble() --> void
        
        
        for i in range(100):
            turn = randint(0,len(self.controls)-1)
            self.controls[self.controls.keys()[turn]]()'''



'''
FOR GENERATING SOLVE PATHS


a = PieceSolver(None)
a.setup()
    

a.reset()
b = []
starttime = time()
for i in range(500000):
    b.append(a.solveCorner())
    a.scramble()
    if (i+1)%100000 == 0:
        print "%d/%d completed" %(i+1,500000)
print time()-starttime
count = 0
amount = 0
turn = []
for i in range(len(b)):
    count += 1
    minidat = []
    for j in range(len(b[i])/2):
        dat = b[i][:2]
        if dat <> 'I0':
            minidat.append(dat)
        dat = dat[2:]
    amount += len(minidat)
            
        
print amount/count

for i in range(1,19):
    a.writefilestep(i)'''
