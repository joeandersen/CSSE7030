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

'''


The Cube displays data with 6 faces of 9 stickers

Faces
0-U, 1-F, 2-L, 3-D, 4-B, 5-R

The top left is sticker 0,
top centre is sticker 1
top right is sticker 2
mid left is sticker 3
mid mid is sticker 4
mid right is sticker 5
bot left is sticker 6
bot mid is sticker 7
bot right is sticker 8

Now, the colours of a piece will change
according to its orientation.
depending on it's position, the colours
will be rotated once clockwise for each orientation
and in others they will be rotated once acw for each

all of these different values are stored in arrays
these lists of number map the faces, pieces and stickers
so that the data can be converted.

'''

from Tkinter import *
from math import *
from ModelPointers import *


class Cube(Canvas):
    '''
    the visual cube
    a canvas with polygons
    '''
    def __init__(self,master, func = False):
        '''
        make a new cube canvas
        init(tk, function) --> void
        '''

        #inherit from canvas
        Canvas.__init__(self,master)

        #if given a function then store it
        self.func = func

        #change height and width
        self.config(height = 300, width = 300)

        #empty space proportion
        self.ss = 5.0

        #init colours
        self.colours = ['white', 'red', 'green', 'yellow', 'orange', 'blue']

        #init controls
        self.controls = {'U':'U','F':'F','L':'L',
                         'D':'D','B':'B','R':'R'}

        #init vector data
        self.data = [5,3,1,2,0,4]
        #rightmost vector is R = 5
        #downmost vector is D = 3
        #forwardmost vector is F = 1
        #leftmost vector is L = 2
        #upmost vector is U = 0
        #backmost vector is B = 4

        #change movetype
        self.changeangle(10, 'block')

        #it's not moving
        self.stopspinning()

        #setup all the polygons
        self._polygons = {}
        for face in range(6):
            for num in range(9):
                self._polygons[face,num] = \
                    Canvas.create_polygon(self,0,0,0,0,0,0, outline = 'black')

        #bind each canvas with the rotate controls
        for bindchar in ['a', 'q', 't', ';', 'b', 'p']:
            self.bind(bindchar, self.linkrotate)
            self.bind("<KeyRelease-%s>"%bindchar, self.linkrotate)

        #renew the display
        self.resetview()
        self.tcolours(self.tconvertdata(None))

        self.bind('<FocusOut>', self.stopspinning)

    def resetview(self):
        '''
        set the vectors to default
        resetview()-->void
        '''
        #set the vectors to default
        temp = self.method
        self.method = 'reset'
        self.rotate()
        self.method = temp


    def tmove(self):
        '''
        render new orientation of cube
        tmove() --> void
        '''
        #only need x and y components
        i,j,k = map(lambda x: x[:2], [self.i, self.j, self.k])
        #also store the reversed vectors
        ir,jr,kr = map(lambda x: self.trev(x), [i,j,k])
        #and the abs move vector
        l = self.l


        # the corners positions can be found by adding the
        #vectors that lead to them
        #ie corner UFR = j + k + i (j will be inverted later)
        #find the coords of the different corners
        c = (self.tadd3(l,i,j,k), self.tadd3(l,ir,j,k),
             self.tadd3(l,ir,j,kr), self.tadd3(l,i,j,kr),
             self.tadd3(l,i,j,k), self.tadd3(l,i,jr,k),
             self.tadd3(l,ir,jr,kr), self.tadd3(l,i,jr,kr))

        #get the corneres of the different faces
        faces = [[c[2],self.tface(i,k)],  #U
                 [c[1],self.tface(i,jr)],  #F
                 [c[2],self.tface(k,jr)],  #L
                 [c[7],self.tface(ir,k)],  #D
                 [c[3],self.tface(ir,jr)],  #B
                 [c[0],self.tface(kr,jr)]] #R

        #pointer to self._polygons
        p = self._polygons

        #for every face
        for face in range(6):

            #get the different corners of the face
            temp = faces[face]

            #get the coords of 'top-left' corner
            x = temp[0][0]
            y = temp[0][1]
            dat = temp[1]

            #for each of the stickers
            for num in range(9):
                #set the coords
                tdat = dat[num]
                tcoords = (tdat[0]+x, tdat[1]+y, \
                  tdat[2] + x, tdat[3] + y, \
                  tdat[4] + x, tdat[5] + y, \
                  tdat[6] + x, tdat[7] + y)
                self.coords(p[face,num], tcoords)

        #lift the ones that are closest (z) to the viewer
        if self.i[2] >= 0:
            for i in range(9):
                self.lift(self._polygons[5,i])
        else:
            for i in range(9):
                self.lift(self._polygons[2,i])
        if self.k[2] >= 0:
            for i in range(9):
                self.lift(self._polygons[1,i])
        else:
            for i in range(9):
                self.lift(self._polygons[4,i])
        if self.j[2] >= 0:
            for i in range(9):
                self.lift(self._polygons[0,i])
        else:
            for i in range(9):
                self.lift(self._polygons[3,i])

    def tcolours(self,data):
        '''
        redo colours of the cube
        tcolours(list) --> void
        '''
        #for every sticker        
        for face in range(6):
            for num in range(9):
                #change the colour
                self.itemconfigure(self._polygons[face,num],
                                fill = data[face][num])

    def linkrotate(self, event):
        '''
        handler for rotation events
        gets rid of lag and some other tkiner things
        linkrotate(event) --> void
        '''

        #if it's the same key as last time do nothing
        if (event.char, event.type) == \
           (self.lastchar, self.lasttype):
            return

        #eventtype 2 is down, 3 is up
        self.turn = event.type == '2'

        #if you bring a key up, but it's not the one you pressed last
        #keep turning
        if (self.lasttype == '2') and (self.lastchar <> event.char)\
           and (event.type == '3'): self.turn = True

        #store event details for later comparison
        self.lastchar = event.char
        self.lasttype = event.type

        #if key down
        if event.type == '2':

          #link for abs turning
          #pick the axes and rotate unit vectors about them
          if self.method == 'const':

            #0 == i, 1 ==j, 2==k
            #rotate these vectors using normal rotation matrix
            link = {'a': (2,0), 'p': (0,1), 't': (1,2),
                    ';': (0,2), 'b': (2,1), 'q': (1,0)}

            #reference matrix
            link2 = [(2,0),(0,1),(1,2),
                     (0,2),(2,1),(1,0)]

            #set r1 and r2 depending on the event
            self.r1, self.r2 = link[event.char]

          #link for rel turning
          #pick the two vectors to turn about the third
          if self.method == 'block':
            
            link = {'a': 4, 'p': 5, 't': 3,
                    ';': 1, 'q': 2, 'b': 0}

            #reference matrix
            dat = [(2,0),(0,1),(2,1),
                   (0,2),(1,0),(1,2)]

            #pick the two vectors needed to rotate
            self.r1, self.r2 = dat[self.data[link[event.char]]]

            if self.cosang == cos(90*pi/180):
                #if it's jump..rotate once only
                self.rotate()
                return

        #if there is already a turn going
        if self.turnrepeat:
            #cancel it's timer
            self.after_cancel(self.turnrepeat)

        #start a turning event
        if self.turn: self.repeatrotate()

    def repeatrotate(self):
        '''
        keeps running rotate at set intervals until stopped
        repeatrotate()--> void
        '''
        #if turnign
        if self.turn:
            #rotate
            self.rotate()
            #call in 20 ms
            self.turnrepeat = self.after(20, self.repeatrotate)

    def rotate(self):
        '''
        rotate()--> void
        '''

        #if reseting view set i,j,k to default
        if self.method == 'reset':
            self.i = [60.0,0,0]
            self.j = [0,-60.0,0]
            self.k = [0,0,60.0]
            self.l = [150, 150, 0]

        #pointers to vectors
        i = self.i
        j = self.j
        k = self.k

        #abs rotation method
        if self.method == 'const':

          #for every unit vector
          for unitvec in [i, j, k]:

            #rotate 2 components about the third axis
            unitvec[self.r1],unitvec[self.r2] = \
                    unitvec[self.r1]*self.cosang-unitvec[self.r2]*self.sinang,\
                    unitvec[self.r1]*self.sinang+unitvec[self.r2]*self.cosang        

        #rel rotation method
        if self.method == 'block':

            #for the unit vectors
            unitvec = [i,j,k]

            #pick 2 and rotate about the third
            unitvec[self.r1], unitvec[self.r2] = \
                self.tadd23d(self.tmult(unitvec[self.r1], self.cosang),
                self.tmult(unitvec[self.r2], self.sinang)),  \
                self.tadd23d(self.tmult(unitvec[self.r2], self.cosang),\
                self.tmult(unitvec[self.r1], -self.sinang))

            #copy vectors back
            self.i, self.j, self.k = unitvec
            i,j,k = self.i, self.j, self.k

        #display change
        self.tmove()

        #if a function should be called call it
        #used to record movement
        if self.func:
            self.func()

        #redefine the controls
        
        #UFLDBR
        valx = [j[0],k[0], -i[0],-j[0],-k[0],i[0]]
        valy = [j[1],k[1],-i[1],-j[1],-k[1],i[1]]
        valz = [j[2],k[2],-i[2],-j[2],-k[2],i[2]]

        #make a copy
        valx, valy, valz = map(lambda y: map(lambda x: int(x),y[:]),\
                            [valx,valy,valz])

        #set up variables
        donemaxx,donemaxy,donemaxz=[None for i in range(3)]


        #define 3 prototype functions

        #get rid of bad vectors
        ops0 = lambda y: filter(lambda x: x <> None, y)

        #find index of opposite
        ops = lambda y: map(lambda x:x%3 + 3 - 3*(x/3),ops0(y))

        #add to get all 6 vectors
        ops2 = lambda y: ops0(y) + ops(y)

        #find vector with largest x value
        Rval = max(valx)
        if valx.count(Rval) == 1:
            donemaxx = valx.index(Rval)

        #add the y vals of those not picked
        dat = []
        for i in range(6):
            if i not in ops2([donemaxx]):
                dat.append(valy[i])

        #find the hightest
        Uval = max(dat)

        #if there is only one pick it 
        if valy.count(Uval) == 1:
            donemaxy = valy.index(Uval)

        #otherwise store those that are max
        else:
            uvals = []
            for i in range(6):
                if valy[i] == Uval:
                    uvals.append(i)

        #make list of z values for those not picked
        dat = []
        for i in range(6):
            if i not in ops2([donemaxx, donemaxy]):
                dat.append(valz[i])

        #find max
        Fval = max(dat)

        #if only one max, pick it
        if valz.count(Fval) == 1:
            donemaxz = valz.index(Fval)

        #otherwise get a list of biggest ones
        else:
            fvals = []
            for i in range(6):
                if valz[i] == Fval:
                    fvals.append(i)

        #if no x val was picked
        if donemaxx == None:

            #get a x value list of those not picked
            dat = []
            for i in range(6):
                if i not in ops2([donemaxy, donemaxz]):
                    dat.append(valx[i])            

            #get list of them with max x
            rvals = []
            for i in range(6):
                if valx[i] == max(dat):
                    rvals.append(i)

            #just add the first one you come across
            for i in rvals:
                if i not in ops2([donemaxy, donemaxz]):
                    donemaxx = i
                    break

        #if no y val was picked
        if donemaxy == None:

            #add y list of those not picked
            dat = []
            for i in range(6):
                if i not in ops2([donemaxx, donemaxz]):
                    dat.append(valy[i])            

            #get list of those at max
            uvals = []
            for i in range(6):
                if valy[i] == max(dat):
                    uvals.append(i)

            #pick the first one
            for i in uvals:
                if i not in ops2([donemaxx, donemaxz]):
                    donemaxy = i
                    break

        #if no z vec picked
        if donemaxz == None:

            #get z-list of those not picked
            dat = []
            for i in range(6):
                if i not in ops2([donemaxx, donemaxy]):
                    dat.append(valz[i])            

            #get list of those at max
            fvals = []
            for i in range(6):
                if valz[i] == max(dat):
                    fvals.append(i)

            #pick the first one
            for i in fvals:
                if i not in ops2([donemaxx, donemaxy]):
                    donemaxz = i
                    break

        #last section was redundant..but need it to be error proof

        #get the list of vectors
        data = [donemaxx, donemaxy, donemaxz]
        self.data = ops2(data)
        self.facelist = self.data

        #masks for values        
        facemap = ['U','F','L','D','B','R']
        facemap2 = ['R','D','F','L','U','B']
        
        #make list from mask and list
        a = map(facemap.__getitem__,self.facelist)

        #set controls accordingly
        for i in range(6):
            self.controls[facemap2[i]] = a[i]

    def changeangle(self,angle, method = 'const'):
        '''
        change the rotation properties
        changeangle(int, str) --> void
        '''

        #set the method
        self.method = method

        #set the angle in rads
        ang = angle*pi/180

        #find the trig proportions of the angle
        self.sinang = sin(ang)
        self.cosang = cos(ang)        
              
    def tadd3(self,a,b,c,d):
        '''
        add 4 2d vectors
        tadd3(list*4) --> list
        '''
        
        return [a[0]+b[0]+c[0]+d[0],a[1]+b[1]+c[1]+d[1]]

    #could be combined with *Args
    def tadd2(self,a,b):
        '''
        add 2 2d vectors
        tadd2(list*2) --> list
        '''
        return a[0]+b[0], a[1]+b[1]

    def tadd8(self,a,b):
        '''
        add 2 vectors to get different points of square
        tadd(list*2) --> (list*8)
        '''
            
        return a[0]+b[0], a[1]+b[1], a[2]+b[0], a[3]+b[1],\
                   a[4]+b[0], a[5]+b[1], a[6]+b[0], a[7]+b[1]

    def tadd23d(self, a,b):
        '''
        add 2 3d vectors
        tadd23d(list*2) --> [list*3]
        '''
        return [a[0]+b[0], a[1]+b[1], a[2]+b[2]]

    def trev(self,a):
        '''
        reverse a vector
        trec(list) --> list
        '''

        return map(lambda x: -x, a)

    def tdiv(self,a,q):
        '''
        scalar division of a vector
        tdiv(list, float) --> list
        '''

        return map(lambda x: x/q, a)

    def tmult(self,a,p):
        '''
        scalar multiple of a vector
        tmult(list, float) --> list
        '''

        return map(lambda x: x*p, a)

    def tface(self,prim, sec):
        '''
        get coordinates for stickers on a face given 2 vectors
        tface(list, list) --> list
        '''

        #find the proportions for the spaces
        #ss is ratio of sticker to space
        ss = self.ss

        #ratio of total length
        ft = 0.5*ss*3.0+2.0

        #equiv of space vec
        i = self.tdiv(prim,ft)
        j = self.tdiv(sec, ft)

        #vectors between relative corneres of adj stickers
        si = self.tmult(i,ss+1)
        sj = self.tmult(j,ss+1)

        #all the different coords of the 'top left' corner of stickers
        b = []
        b.append(self.tadd2(i,j)+ self.tadd2(si,j)+\
                 self.tadd2(si,sj)+ self.tadd2(i,sj))
        b.append(self.tadd8(b[0], si))
        b.append(self.tadd8(b[1], si))
        b.append(self.tadd8(b[0], sj))
        b.append(self.tadd8(b[3], si))
        b.append(self.tadd8(b[4], si))
        b.append(self.tadd8(b[3], sj))
        b.append(self.tadd8(b[6], si))
        b.append(self.tadd8(b[7], si))

        return b

    def tconvertdata(self, data):
        '''
        get stickerinfo from pieceinfo

        all of these arrays provide maps between
        faces, pieces and stickers
        
        tconvertdata(list) --> list
        '''

        #if no data supplied assume solved cube
        if data == None:
            data = [[i,0] for i in range(12)]+[[i,0] for i in range(8)]

        #faces that corners are on
        #also understood as colours that the corners have
        clist = [[0,5,1],[0,1,2],[0,2,4],[0,4,5],
                 [3,1,5],[3,2,1],[3,4,2],[3,5,4]]

        #face that edges are on
        #also the colour of the different edges
        elist = [[0,5],[0,1],[0,2],[0,4],
                 [3,5],[3,1],[3,2],[3,4],
                 [1,5],[1,2],[4,2],[4,5]]

        #list of stickers
        #colour of pieces (corner and edge both <12)
        #for each sticker (piece number, face of piece number)
        slist = [[(2,0),(3,0),(3,0),(2,0),(0,0),(1,0),(1,0),(0,0)],
                 [(1,1),(1,1),(0,2),(9,0),(8,0),(5,2),(5,1),(4,1)],
                 [(2,1),(2,1),(1,2),(10,1),(9,1),(6,2),(6,1),(5,1)],
                 [(7,0),(7,0),(6,0),(4,0),(6,0),(4,0),(5,0),(5,0)],
                 [(3,1),(3,1),(2,2),(11,0),(10,0),(7,2),(7,1),(6,1)],
                 [(0,1),(0,1),(3,2),(8,1),(11,1),(4,2),(4,1),(7,1)]]

        #get face data for edges
        edat = [self.rote(elist[ep],eo) for ep,eo in data[:12]]
        #get face data for corners
        cdat = [self.rotc(clist[cp],co) for cp, co in data[12:]]

        #get output
        output = []
        for face in slist:
            #list of face nums
            temp = [cdat[face[0][0]][face[0][1]],
                    edat[face[1][0]][face[1][1]],
                    cdat[face[2][0]][face[2][1]],
                    edat[face[3][0]][face[3][1]],
                    slist.index(face),
                    edat[face[4][0]][face[4][1]],
                    cdat[face[5][0]][face[5][1]],
                    edat[face[6][0]][face[6][1]],
                    cdat[face[7][0]][face[7][1]]]
            temp2 = []
            for i in temp:
                #list of colours
                temp2.append(self.colours[i])
            output.append(temp2)

        #return list of colours
        return output

    def rote(self, data, orient):
        '''
        rotate edge (data) by orient
        rote(list, int) --> list        
        '''
        for i in range(orient%2):
            #move front entry to back
            data.append(data.pop(0))
        return data

    def rotc(self, data, orient):
        '''
        rotate corner (data) by orient
        rote(list, int) --> list
        '''
        
        for i in range(orient%3):
            #move front data to back
            data.append(data.pop(0))
        return data

    def tcomp(self, data, comp):
        '''
        gets a component of vectors
        tcomp(list) --> list
        '''
        output = []
        for i in data:
            #take component
            output.append(i[comp])
        return output

    def tlinecolour(self,colour):
        '''
        set border colour of polygones
        tlinecolour(str) --> void
        '''
        for face in range(6):
            for num in range(9):
                self.itemconfigure(self._polygons[face,num],
                                outline = colour)

    def stopspinning(self, event = None):
        '''
        just stop the cube spinning
        optional event for focusout
        stopspinning(event) --> void
        '''
        
        self.turn = False
        self.lastchar, self.lasttype = None, None
        self.turnrepeat = False 

'''root = Tk()
app = Cube3(root)
#app.configure()
root.mainloop()'''
