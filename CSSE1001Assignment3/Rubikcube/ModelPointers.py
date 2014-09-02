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

from random import *

class Model:
    '''
    Model stores piece information about a cube
    stored as postion edge pairs
    now would go back and make this inherit from list
    designed for speed in solving
    all of the face function could be stored in a single list
    however, this takes much more time so they were written out fully
    '''


    '''
    Model stores piece information about a cube
    stored as postion edge pairs
    now would go back and make this inherit from list
    designed for speed in solving
    all of the face function could be stored in a single list
    however, this takes much more time so they were written out fully
    '''

    '''

    The first 12 places of Model.data are the edge pieces
    The other 8 are the corner pieces

    Faces U, D, F, B, L and R are used to describe positions
    Up, Down, Front, Back, Left and Right

    The first value describes the initial posiition in the cube
    corner 0 - UFR
    c1 - UFL
    c2 - UBL
    c3 - UBR
    c4 - DFR
    c5 - DFL
    c6 - DBL
    c7 - DBR

    edges
    0 - UR, 1 - UF, 2 - UL, 3 - UB
    4 - DR, 5 - DF, 6 - DL, 7 - DB
    8 - FR, 9 - FL, 10- BL, 11- BR

    The second value describes the orientation of the piece
    corners are oriented correctly if their top/down face is lined up
    corners have orientation 1 if they need to be rotated once clockwise
    corners have orientation 2 if they need to be rotated twice clockwise

    edges are oriented if their primary face matches the primary face
    of the position it is in.
    primary face is U/D
    secondary is F/B
    tertiary is L/R

    U1 --> R3 were the fastest implimentation
    of a basic face turn that i could find.
    it moves the pieces in the absolute positions around
    this works because you are just changing the position
    of the list pointers.

    for example,
    U1 rotates all pieces on the top face
    it doesn't change the orientation of pieces,
    because their orientation relative to the top face won't change

    the top corners are 0-->3
    which correspond to positions 12 --> 15 in Model.data
    
    the top edges are 0-->3
    which correspond to positions 0-->3 in Model.data
        

    '''
    
    def __init__(self, data=None):
        '''
        init the model
        init(array) --> void      
        '''
        
        self.data = data
        if data == None:
            self.reset()

    def getData(self):
        '''
        returns the data from the object
        getData() --> list
        '''
        return self.data

    def reset(self):
        '''
        reset the model data
        '''
        
        t = [[0,0],[1,0],[2,0],[3,0],
             [4,0],[5,0],[6,0],[7,0],
             [8,0],[9,0],[10,0],[11,0],
             [0,0],[1,0],[2,0],[3,0],
             [4,0],[5,0],[6,0],[7,0]]
        
        self.data = t

    def scramble(self):
        '''
        scramble the cube
        scramble() --> void
        '''

        #list of possible face turns
        moves = [self.U1, self.U2, self.U3,
                 self.D1, self.D2, self.D3,
                 self.F1, self.F2, self.F3,
                 self.B1, self.B2, self.B3,
                 self.L1, self.L2, self.L3,
                 self.R1, self.R2, self.R3]

        #turn 100 times
        for i in range(100):
            moves[randint(0,17)]()

    def U1(self):
        '''
        U1() --> void
        '''
        
        t = self.data
        
        temp = t[0]
        t[0] = t[3]
        t[3] = t[2]
        t[2] = t[1]
        t[1] = temp
        temp = t[12]
        t[12] = t[15]
        t[15] = t[14]
        t[14] = t[13]
        t[13] = temp

    def U2(self):
        '''
        U2() --> void
        '''
        
        t = self.data
        
        t[2], t[0] = t[0], t[2]
        t[1], t[3] = t[3], t[1]
        t[14], t[12] = t[12], t[14]
        t[13], t[15] = t[15], t[13]

    def U3(self):
        '''
        U3() --> void
        '''
        
        t = self.data
        
        temp = t[0]
        t[0] = t[1]
        t[1] = t[2]
        t[2] = t[3]
        t[3] = temp
        temp = t[12]
        t[12] = t[13]
        t[13] = t[14]
        t[14] = t[15]
        t[15] = temp

    def D1(self):
        '''
        D1() --> void
        '''
        
        t = self.data
        
        temp = t[4]
        t[4] = t[5]
        t[5] = t[6]
        t[6] = t[7]
        t[7] = temp
        temp = t[16]
        t[16] = t[17]
        t[17] = t[18]
        t[18] = t[19]
        t[19] = temp

    def D2(self):
        '''
        D2()-->void
        '''
        
        t = self.data
        
        t[6], t[4] = t[4], t[6]
        t[5], t[7] = t[7], t[5]
        t[18], t[16] = t[16], t[18]
        t[17], t[19] = t[19], t[17]

    def D3(self):
        '''
        D3()-->void
        '''
        
        t = self.data
        
        temp = t[4]
        t[4] = t[7]
        t[7] = t[6]
        t[6] = t[5]
        t[5] = temp
        temp = t[16]
        t[16] = t[19]
        t[19] = t[18]
        t[18] = t[17]
        t[17] = temp

    def F1(self):
        '''
        F1()-->void
        '''
                
        t = self.data
        
        temp = t[8]
        t[8] = t[1]
        t[1] = t[9]
        t[9] = t[5]
        t[5] = temp
        temp = t[12]
        t[12] = t[13]
        t[13] = t[17]
        t[17] = t[16]
        t[16] = temp
    
        t[8][1] += 1
        t[9][1] += 1
        t[5][1] += 1
        t[1][1] += 1
        t[16][1] += 1
        t[17][1] -= 1
        t[13][1] += 1
        t[12][1] -= 1

    def F2(self):
        '''
        F2()-->void
        '''
                
        t = self.data
        
        t[1], t[5] = t[5], t[1]
        t[8], t[9] = t[9], t[8]
        t[13],t[16] = t[16], t[13]
        t[12],t[17] = t[17], t[12]

    def F3(self):
        '''
        F3()-->void
        '''
                
        t = self.data
        
        temp = t[1]
        t[1] = t[8]
        t[8] = t[5]
        t[5] = t[9]
        t[9] = temp
        temp = t[12]
        t[12] = t[16]
        t[16] = t[17]
        t[17] = t[13]
        t[13] = temp
        
        t[8][1] += 1
        t[9][1] += 1
        t[5][1] += 1
        t[1][1] += 1
        t[16][1] += 1
        t[17][1] -= 1
        t[13][1] += 1
        t[12][1] -= 1

    def B1(self):
        '''
        B1()-->void
        '''
        
        t =self.data
        
        temp = t[3]
        t[3] = t[11]
        t[11] = t[7]
        t[7] = t[10]
        t[10] = temp
        temp = t[14]
        t[14] = t[15]
        t[15] = t[19]
        t[19] = t[18]
        t[18] = temp

        t[3][1] += 1
        t[11][1] += 1
        t[7][1] += 1
        t[10][1] += 1
        t[14][1] -= 1
        t[15][1] += 1
        t[19][1] -= 1
        t[18][1] += 1

    def B2(self):
        '''
        B2()-->void
        '''
                
        t = self.data
        
        t[3], t[7] = t[7], t[3]
        t[11],t[10]= t[10],t[11]
        t[14],t[19] = t[19],t[14]
        t[15],t[18] = t[18],t[15]

    def B3(self):
        '''
        B3()-->void
        '''
                
        t = self.data

        temp = t[3]
        t[3] = t[10]
        t[10] = t[7]
        t[7] = t[11]
        t[11] = temp
        temp = t[14]
        t[14] = t[18]
        t[18] = t[19]
        t[19] = t[15]
        t[15] = temp

        t[3][1] += 1
        t[10][1] += 1
        t[7][1] += 1
        t[11][1] += 1
        t[14][1] -= 1
        t[15][1] += 1
        t[19][1] -= 1
        t[18][1] += 1

    def L1(self):
        '''
        L1()-->void
        '''
                
        t = self.data

        temp = t[13]
        t[13] = t[14]
        t[14] = t[18]
        t[18] = t[17]
        t[17] = temp
        temp = t[2]
        t[2] = t[10]
        t[10] = t[6]
        t[6] = t[9]
        t[9] = temp

        t[13][1] -= 1
        t[14][1] += 1
        t[18][1] -= 1
        t[17][1] += 1

    def L2(self):
        '''
        L2()-->void
        '''
                
        t = self.data
        
        t[13],t[18] = t[18], t[13]
        t[14],t[17] = t[17], t[14]
        t[2], t[6] = t[6], t[2]
        t[9],t[10] = t[10], t[9]

    def L3(self):
        '''
        L3()-->void
        '''
        
        t = self.data

        temp = t[13]
        t[13] = t[17]
        t[17] = t[18]
        t[18] = t[14]
        t[14] = temp
        temp = t[2]
        t[2] = t[9]
        t[9] = t[6]
        t[6] = t[10]
        t[10] = temp

        t[13][1] -= 1
        t[14][1] += 1
        t[18][1] -= 1
        t[17][1] += 1

    def R1(self):
        '''
        R1()-->void
        '''
        
        t = self.data

        temp = t[0]
        t[0] = t[8]
        t[8] = t[4]
        t[4] = t[11]
        t[11] = temp
        temp = t[12]
        t[12] = t[16]
        t[16] = t[19]
        t[19] = t[15]
        t[15] = temp

        t[12][1] += 1
        t[16][1] -= 1
        t[19][1] += 1
        t[15][1] -= 1

    def R2(self):
        '''
        R2()-->void
        '''
        
        t = self.data

        t[0], t[4] = t[4], t[0]
        t[8], t[11] = t[11], t[8]
        t[12], t[19] = t[19], t[12]
        t[16], t[15] = t[15], t[16]

    def R3(self):
        '''
        R3()-->void
        '''
        
        t  = self.data

        temp = t[0]
        t[0] = t[11]
        t[11] = t[4]
        t[4] = t[8]
        t[8] = temp
        temp = t[12]
        t[12] = t[15]
        t[15] = t[19]
        t[19] = t[16]
        t[16] = temp

        t[12][1] += 1
        t[16][1] -= 1
        t[19][1] += 1
        t[15][1] -= 1

'''
a = Model(None)
a.reset()

start = time()
for i in (a.U1, a.U2, a.U3, a.D1, a.D2, a.D3, a.F1, a.F2, a.F3,\
          a.B1, a.B2, a.B3, a.L1, a.L2, a.L3, a.R1, a.R2, a.R3,\
          ):
    t1 = time()
    for j in range(18**0):
        i()
        a.getData()
    print time() -t1

print "total: %f seconds" %(time() - start)


data1 = []
start = time()
for j in range(18**4):
  for i in (a.U1, a.D1, a.F1, a.B1, a.L1, a.R1,\
          ):
    i()
    data1.append(a.getData())
    i()
    data1.append(a.getData())
    i()
    data1.append(a.getData())
    i()

print "total: %f seconds" %(time() - start)
'''
