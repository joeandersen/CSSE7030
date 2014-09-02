"""
AutoCUT 1.0

Copyright (C) 2008 Jonathan Keller -s4079854@student.uq.edu.au

Program functions and algorithms written by Jonathan Keller

Splash screen image by Brett Wissemann, 2008 -bwissemann@hotmail.com

DESCRIPTION

AutoCUT 1.0 is the first version of a Computer Aided Modelling software
package. This software package aids in the automation of a 2 degree of freedom
bandsaw (Rotation and Translation). AutoCUT 1.0 supports IGES file importing
for CAD draft drawings in 2D.

AutoCUT 1.0 only supports IGES files with line and arc entities.
AutoCUT 1.0 does not support I/O to an automated bandsaw

LICENSE

I, Jonathan Keller, Hereby grant the rights to distribute, modify, and edit the
source to AutoCUT 1.0, on the condition that this agreement, and my ownership
of the code contained herewithin be maintained.

Furthurmore, I grant the right to use excerpts from the source to AutoCUT 1.0
without express permission, with exclusion of commercial application.
"""



from Tkinter import *
from math import *
import time, tkFileDialog

try:
    import Image, ImageTk
    PIL=True
except:
    PIL=False


class mainWindow:
    def __init__(self, master):
        """Initialise main AutoCUT Window

        Note: Canvas is set to 50 pixels less than screen width
                and 130 pixels less than screen height
        """
        self.JCode = []
        lessThanHeight, lessThanWidth = 130, 50
        self.master = master
        self.nodeRes, self.turnRes, self.turnRate = 3.0, 1.5, 2.0
        master.title("Auto CUT")
        self.mainFrame = Frame(master)
        self.mainFrame.pack(side=TOP)
        self.picFrame = Frame(master)
        self.picFrame.pack(side=BOTTOM)
        self.IGESFileLoaded = self.JCodeFileLoaded = None
        
        Label(self.mainFrame, text="File Loaded: ").pack(side=LEFT)
        self.fileLoadedLabel=Label(self.mainFrame, text="NO FILE")
        self.fileLoadedLabel.pack(side=LEFT,padx=20)
        
        self.menuBar = Menu(master)                 #Menu Bar
        master.config(menu=self.menuBar)

        self.fileMenu = Menu(self.menuBar)          #File Menu
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="Open JCode File",
                                  command=self.openJCodeFile)
        self.fileMenu.add_command(label="Save JCode File",
                                  command=self.saveJCodeFile,
                                    state=DISABLED)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.exitApp)

        self.importMenu = Menu(self.menuBar)        #Import Menu
        self.menuBar.add_cascade(label="Import", menu=self.importMenu)
        self.importMenu.add_command(label="Import IGES File",
                    command=self.importIGES)
        
        #To be implemented later
        self.importMenu.add_command(label="Import DXF File",state=DISABLED)  
        self.importMenu.add_command(label="Import STL File",state=DISABLED)
        self.importMenu.add_command(label="Import 3DM File",state=DISABLED)

        self.optionsMenu = Menu(self.menuBar)       #Options Menu
        self.menuBar.add_cascade(label="Options", menu=self.optionsMenu)
        self.optionsMenu.add_command(label="Options",
                                     command=self.optionsDialog)
        self.optionsMenu.add_command(label="Calculate JCode",
                                     command=self.calcJCode,
                                     state=DISABLED)

        self.cutMenu = Menu(self.menuBar)
        self.menuBar.add_cascade(label="Cut", menu=self.cutMenu)
        self.cutMenu.add_command(label="Cut Shape", state=DISABLED)
        self.cutButton = self.cutMenu.add_command(label="Cut with VirtualCUT",
                                 command=self.cutWithVCut,
                                 state=DISABLED)

        self.aboutMenu = Menu(self.menuBar)          #About Menu
        self.menuBar.add_cascade(label="About", menu=self.aboutMenu)
        self.aboutMenu.add_command(label="About", command=self.aboutBox)
        
        self.picSpace = Canvas(self.picFrame,
                        width=self.master.winfo_screenwidth()-lessThanWidth,
                        height=self.master.winfo_screenheight()-lessThanHeight)
        self.picSpace.pack()

        
    def openJCodeFile(self):
        """Open JCode file using tkFileDialog and read file contents into
        self.JCode

        openJCodeFile() --> void
        """
        
        self.JCode = []
        JCodeFile = tkFileDialog.askopenfilename(filetypes = [
            ("JCode", "*.JCD"), ("JCode", "*.jcd"), ("All Files", "*")])
        
        if self.JCodeFileLoaded != JCodeFile:
            if JCodeFile:
                self.fileLoadedLabel.config(text=JCodeFile)
                self.JCodeFileLoaded = JCodeFile
                f = open(JCodeFile, 'r')
                data = f.readlines()
                for entry in data:
                    entry = entry[:-1]
                    if entry.isalpha():
                        self.JCode.append(entry)
                    elif entry.startswith("["):
                        dat1, dat2 = entry.split(",")
                        dat1, dat2 = dat1.lstrip("["), dat2.rstrip("]")
                        dat1, dat2 = float(dat1), float(dat2)
                        temp = [dat1, dat2]
                        self.JCode.append(temp)
                    else:
                        self.JCode.append(float(entry))
                f.close()
        self.cutMenu.entryconfigure(2, state=NORMAL)
                

    def saveJCodeFile(self):
        """Save current JCode file to .JCD file. Write contents of self.JCode
        line by line to file. Note: Disabled until JCode file opened or IGES
        file imported and JCode calculated

        saveJCodeFIle() --> void
        """

        JCodeFile = tkFileDialog.asksaveasfilename(defaultextension = ".JCD",
                                                   filetypes = [
            ("JCode", "*.JCD"), ("JCode", "*.jcd"), ("All Files", "*")])
         
        if JCodeFile:
            if self.JCode:
                f = open(JCodeFile, "w")
                for entry in self.JCode:        # Can't write a list of list 
                    f.write(str(entry)+"\n")    # directly to file
        f.close()
        self.fileLoadedLabel.config(text=JCodeFile)
        

    def exitApp(self):
        """Exit application by destroying master"""
        
        self.master.destroy()


    def importIGES(self):
        """Import IGES file selected with tkFileDialog and send filename of
        IGES file to function readIGESFile, which returns self.PPars and
        self.units.  Draw design

        importIGES() --> void
        """

        self.optionsMenu.entryconfigure(2, state=NORMAL)
        
        IGESFile = tkFileDialog.askopenfilename(filetypes = [("IGES", "*.iges"),
                                                             ("IGES", "*.igs")])
        if self.IGESFileLoaded != IGESFile:
            if IGESFile != '':
                self.fileLoadedLabel.config(text=IGESFile)
                if self.IGESFileLoaded==None:
                    firstRun = True
                    self.lineTags = []
                else: firstRun = False
                self.IGESFileLoaded = IGESFile
                self.PPars, self.units = readIGESFile(self.IGESFileLoaded)
                
                self.drawDesign(self.PPars, firstRun)

        
    def drawDesign(self, PPars, firstRun):
        """Draw Design in PPars to self.picSpace. Stretch factor is found with
        function findStretch then whitespace is removed from the data points
        and the data points are scaled. data points are passed into par110 or
        drawARC depending on what entity the line is and a line or arc is
        created on the canvas

        drawDesign(list<list<int, float, float...>>, bool) --> void
        """

        if firstRun == False:
            self.picSpace.delete(ALL)        
        
        xBuffer = yBuffer = 50
        stretch, midy, xMin, yMin = findStretch(PPars,
                                                self.picSpace.winfo_width(),
                                                self.picSpace.winfo_height(),
                                                xBuffer, yBuffer, False)
        self.xMin = xMin
        for entry in PPars:
            if entry[0] == 110:
                data = scale(stretch,
                             removeWhite(xMin, yMin, par110(entry, midy)))
                self.picSpace.create_line(fitLine(data, xBuffer, yBuffer))
               
            if entry[0] == 100:
                data = scale(stretch,
                             removeWhiteArc(xMin, yMin, parARC(entry, midy)))
                x1,y1,x2,y2,extD,startD = drawARC(data, xBuffer, yBuffer)
                self.picSpace.create_arc(x1,y1,x2,y2,extent=extD,start=startD,
                                         style=ARC)


##    def removeLine(self):
##        pass

    
    def optionsDialog(self):
        """Pop up options box. Pass in JCode settings. Get settings once options
        window is destroyed.

        optionsDialog() --> void
        """
        
        Options = optionsBox(self.turnRate, self.nodeRes, self.turnRes)
        self.turnRate = Options.turnRate
        self.nodeRes = Options.nodeRes
        self.turnRes = Options.turnRes
        

    def aboutBox(self):
        """Pop up about box

        aboutBox() --> void
        """
        
        aboutBox()


    def cutWithVCut(self):
        """Send current self.JCode variable to virtualCut class to demonstrate
        the calculated tool path

        cutWithVCut() --> void
        """
        
        virtualCut(self.JCode)


    def calcJCode(self):
        """Calculate JCode from current IGES file. Calculating the JCode is a
        complicated process, basically calcJCode iterates through self.PPars, if
        an entry is a line entity it codes first a change of orientation from
        previous orientation, then a translating segment until at end of line.
        If the entity is an arc it codes first a change of orientation, then a
        small change of orientation, small translation, until it has moved
        through the arc.
        
            self.PPars contains data entries
            self.units contains files units

        calcJCode() --> void
        """
        
        parD = {100:par100,110:par110} #dict for calling coord getter
        tempCode, pCoOrds, doneIndexes, nodeRes = [], [], [], self.nodeRes
        xmax = xmin = ymax = ymin = yI = 0
        turnRes, lastOrient, turnRate = self.turnRes,  270.0, self.turnRate
        first, last, firstLoop = True, False, True
        xBuff = yBuff = 10.0
        
        # Find coord to start from (Find ymax)
        # startCoOrd is (index of maximum ycoord, 0 for ystart, 1 for yend)
        for entry in self.PPars:
            if entry[0] in parD:
                x1, y1, x2, y2 = parD.get(entry[0])(entry)
                if y1 > ymax:
                    ymax = y1
                    xStart = x1
                    startCoOrd = (yI,0)
                if y2 > ymax:
                    ymax = y2
                    xStart = x2
                    startCoOrd = (yI,1)
            yI += 1
            
        width, height, xMin, yMax = findStretch(self.PPars, 0, 0, 0, 0, True)
        trueWidth, trueHeight = width*self.units, height*self.units
        
        tempCode.extend(("DIM",[trueWidth+2*xBuff,trueHeight+2*yBuff],"INIT"))
        
        moveInit = (xStart - xMin)*self.units + xBuff
        numMoves = int(moveInit/nodeRes)
        remainder = moveInit - (numMoves*nodeRes)
        
        for i in range(numMoves):
            tempCode.append(nodeRes)
        if remainder:
            tempCode.append(remainder)
        tempCode.append("CUT")

        initDist = yBuff + abs(ymax - yMax)
        numMoves = int(initDist/nodeRes)
        remainder = initDist - (numMoves*nodeRes)

        for i in range(numMoves):
            tempCode.append([nodeRes, 0])
        if remainder:
            tempCode.append([remainder, 0])
       
        while not last:
            
            if first == True:
                coOrd = startCoOrd
                first = False
            else:
                coOrd = nextCoOrd
            
            if self.PPars[coOrd[0]][0] == 110: ####LINE entries
                if coOrd[1] == 1:   #If starting from end point flip coords
                    x2,y2,x1,y1 = par110(self.PPars[coOrd[0]])
                else:
                    x1,y1,x2,y2 = par110(self.PPars[coOrd[0]])
                    
                orient = findAngle(x1,y1,x2,y2)
                
                dOrient = orient - lastOrient
                if dOrient > 180:
                    dOrient = -(360-dOrient)
                elif dOrient < -180:
                    dOrient = -(-360-dOrient)

                while abs(dOrient) > turnRate:
                    if dOrient > 0:
                        tempCode.append([0, turnRate])
                        dOrient -= turnRate
                    else:
                        tempCode.append([0, -turnRate])
                        dOrient += turnRate

                if dOrient:
                    tempCode.append([0, dOrient])

                dx,dy=(x2-x1)*self.units ,(y2-y1)*self.units
                length = hypot(dx, dy)
                numNodes = int(length/nodeRes)
                remainder = length-(numNodes*nodeRes)
                
                for i in range(numNodes):
                    tempCode.append([nodeRes, 0])
                if remainder:
                    tempCode.append([remainder, 0])
                  
                lastOrient = orient
                doneIndexes.append(coOrd[0])

            if self.PPars[coOrd[0]][0] == 100: ####ARC entries
                if coOrd[1] == 1: #Starting at end point
                    xC,yC,x2,y2,x1,y1 = parARC(self.PPars[coOrd[0]])
                else:
                    xC,yC,x1,y1,x2,y2 = parARC(self.PPars[coOrd[0]])

                #APPEND INITIAL DOrient
                orient = findAngle(xC,yC,x1,y1)
                if coOrd[1] == 1:
                    orient -= 90
                else:
                    orient += 90

                dOrient = orient - lastOrient
                
                if dOrient > 180:
                    dOrient = -(360-dOrient)
                elif dOrient < -180:
                    dOrient = -(-360-dOrient)

                while abs(dOrient) > turnRate:
                    if dOrient > 0:
                        tempCode.append([0, turnRate])
                        dOrient -= turnRate
                    else:
                        tempCode.append([0, -turnRate])
                        dOrient += turnRate

                if dOrient:
                    tempCode.append([0, dOrient])

                   
                distX, distY = (xC-x1)*self.units, (yC-y1)*self.units
                d = hypot(distX, distY)
                a = turnRes
                #FIND DOrient for each move
                #BISECTION METHOD: 0 = asin(alpha)-dsin(theta)
                th1, th2, tol = 0.0, 180.0, 10e-8
                
                while abs(th1-th2) > tol:
                    th3 = (th1 + th2)/2
                    res = sinRuleFunc(th1,a,d)*sinRuleFunc(th3,a,d)
                    
                    if res < 0:
                        th2 = th3
                    else:
                        th1 = th3  
                
                if coOrd[1] == 1:
                    dOrient = -(th1+th2)/2
                else:
                    dOrient = (th1+th2)/2

                startAngle = findAngle(xC,yC,x1,y1)
                endAngle = findAngle(xC,yC,x2,y2)

                theta = endAngle - startAngle
                
                if coOrd[1] == 1:
                    if theta > 0:
                        theta -= 360
                if coOrd[1] == 0:
                    if theta < 0:
                        theta += 360
                
                numSegments = int(theta/dOrient)
                
                for i in range(numSegments):
                    tempCode.append([0, dOrient])
                    tempCode.append([turnRes, 0])
                    theta -= dOrient
                if theta:
                    tempCode.append([0, theta])
                    #Sin Rule to find magnitude of move to get to last coOrd
                    lastMove = d*sin(radians(abs(theta)))/  \
                               sin(radians((180-abs(theta))/2))
                    tempCode.append([lastMove, 0])

                #Find final orientation and save as lastOrient
                lastOrient = findAngle(xC,yC,x2,y2)
                if coOrd[1] == 1:
                    lastOrient -= 90
                else:
                    lastOrient += 90
                    
                doneIndexes.append(coOrd[0])
                
            ###FIND NEXT LINE with one point tolerance
            yN = 0
            for entry in self.PPars:
                
                if firstLoop:
                    if yN == doneIndexes[0]:
                        firstLoop = False
                        yN += 1
                        continue
                    
                if yN not in doneIndexes[1:]:
                   
                    if entry[0] in parD:
                        
                        xN1, yN1, xN2, yN2 = parD.get(entry[0])(entry)
                        if xN1 > x2-1 and xN1 < x2+1:
                            if yN1 > y2-1 and yN1 < y2+1:
                                nextCoOrd = (yN,0)
                        if xN2 > x2-1 and xN2 < x2+1:
                            if yN2 > y2-1 and yN2 < y2+1:
                                nextCoOrd = (yN,1)
                
                yN += 1
            
            if nextCoOrd[0] == startCoOrd[0]:
                last = True
        
        self.JCode = tempCode
        
        self.fileMenu.entryconfigure(2, state=NORMAL)
        self.cutMenu.entryconfigure(2, state=NORMAL)


def findArcMaxes(xC,yC,x1,y1,x2,y2,endToStart):
    """Return x and y Min and x and y Max. findArcMaxes does this by breaking
    the arc up into lots of points and finding the coordinates of each. The
    minimums and maximums can then be found easily.

    findArcMaxes(fl,fl,fl,fl,fl,fl,bool) --> fl,fl,fl,fl
    """

    if x1 > x2:
        xMax = x1
        xMin = x2
    else:
        xMax = x2
        xMin = x1
    if y1 > y2:
        yMax = y1
        yMin = y2
    else:
        yMax = y2
        yMin = y1
        
    d = hypot(x1-xC,y1-yC)
    
    startAngle = findAngle(xC,yC,x1,y1)
    endAngle = findAngle(xC,yC,x2,y2)

    if endToStart == 1:
        angle = startAngle - endAngle
        if angle < 0:
            angle += 360
        while angle > 2.0:
            startAngle -= 2.0
            if startAngle < 0: startAngle += 360
            x,y = d*cos(radians(startAngle)), d*sin(radians(startAngle))
            x+=xC
            y+=yC
            if x < xMin: xMin = x
            elif x > xMax: xMax = x
            if y < yMin: yMin = y
            elif y > yMax: yMax = y
                
            angle -= 2.0
    else:
        angle = endAngle - startAngle
        if angle < 0:
            angle += 360
        while angle > 0.0:
            startAngle += 2.0
            if startAngle > 360: startAngle -= 360
            x,y = d*cos(radians(startAngle)), d*sin(radians(startAngle))
            x+=xC
            y+=yC
            if x < xMin: xMin = x
            elif x > xMax: xMax = x
            if y < yMin: yMin = y
            elif y > yMax: yMax = y
            
            angle -= 2.0
            
    return xMin,yMin,xMax,yMax

    
def findAngle(x1,y1,x2,y2):
    """Return angle in degrees of line from x1,y1->x2,y2

    findAngle(float,float,float,float) --> float
    """
    
    dx,dy = x2-x1, y2-y1
    
    if dx == 0:
        if dy > 0:
            orient = 90
        else:
            orient = 270
    elif dy == 0:
        if dx > 0:
            orient = 0
        else:
            orient = 180
    else:
        orient = degrees(atan(abs(dy/dx)))
        if dy > 0:
            if dx > 0:
                pass
            else:
                orient = 180 - orient        
        else:
            if dx > 0:
                orient = 360 - orient
            else:
                orient = 180 + orient
    return orient


def sinRuleFunc(theta, a, d):
    """Function for easier implementation of the bisection method in calcJCode.

    sinRuleFunc(float, float, float) --> float
    """

    return (a*sin(radians((180-theta)/2)))-(d*sin(radians(theta)))


def removeWhite(minX, minY, tup):
    """Return x,y coords with whitespace before shape outline, removed

    removeWhite(fl, fl, (fl, fl, fl, fl)) --> (fl, fl, fl, fl)
    """

    return tup[0]-minX, tup[1]-minY, tup[2]-minX, tup[3]-minY


def removeWhiteArc(minX, minY, tup):
    """Return x,y coords with whitespace before shape removed -> for arcs

    removeWithArc(fl, fl, (fl, fl, fl, fl, fl, fl) --> (fl, fl, fl, fl, fl, fl)
    """

    return tup[0]-minX, tup[1]-minY, tup[2]-minX, tup[3]-minY, \
           tup[4]-minX, tup[5]-minY


def scale(stretch, dataTuple):
    """Return scaled tuple of coordinates by stretch

    scale(float, (float, float...) --> (float, float...)
    """

    return tuple([stretch*i for i in dataTuple])


def fitLine(tup, xBuffer, yBuffer):
    """Return coordinates tuple with the x and y buffers added

    fitLine((fl, fl, fl, fl), fl, fl) --> (fl, fl, fl, fl)
    """
    
    return tup[0]+xBuffer,tup[1]+yBuffer,tup[2]+xBuffer,tup[3]+yBuffer


def fitArc(tup, xBuffer, yBuffer):
    """Return arc coordinate tuple with the x and y buffers added

    fitArc((fl, fl, fl, fl, fl, fl), fl, fl) --> (fl, fl, fl, fl, fl, fl)
    """

    return tup[0]+xBuffer,tup[1]+yBuffer,tup[2]+xBuffer,tup[3]+yBuffer, \
                                         tup[4]+xBuffer,tup[5]+yBuffer
        
    
def readIGESFile(fileName):
    """Open user-selected IGES file and return Parameter data and file's units

    readIGESFile(string) --> list<list<int, float, float...>>, float
    """
    
    IGESFile = open(fileName, 'r')

    dataFile = []
    
    for line in IGESFile:
        dataFile.append(line)
    IGESFile.close()

    noParsLine = dataFile[-1]
    pars = getNoPar(noParsLine)
    
    SPars, GPars, DPars, PPars,  DParsM, PParsM = [], [], [], [], [], []

    for i in range(pars[0]):
        SPars.append(dataFile[i])
        
    for i in range(pars[0],pars[0]+pars[1]):
        GPars.append(dataFile[i])

    for i in range(pars[0]+pars[1],pars[0]+pars[1]+pars[2]):
        DPars.append(dataFile[i])

    for i in range(pars[0]+pars[1]+pars[2],pars[0]+pars[1]+pars[2]+pars[3]):
        PPars.append(dataFile[i])

    fileUnits = findUnits(GPars)
    readDPars(DPars,DParsM)    #Directory Data not used in AutoCUT 1.0
    readPPars(PPars,PParsM)

    return filterPPars(PParsM), fileUnits


def findUnits(GPars):
    """Find units of file from global section

    findUnits(list<str>) --> float
    """

    globalstring = ''
    for dataLine in GPars:
        globalstring += dataLine[:-10]

    Glist = globalstring.split(',')
    unitsCh = Glist[15][2:]
    if unitsCh == 'MM':     units = 1.0
    elif unitsCh == 'SP':   units = 3.5 #Special unit for demonstration
    elif unitsCh == 'CM':   units = 10.0
    elif unitsCh == 'M':    units = 1000.0
    elif unitsCh == 'IN':   units = 25.4
    elif unitsCh == 'FT':   units = 304.8
    else:   units = 1

    return units

    
def readDPars(DPars,DParsM):
    """Convert Directory Data List into a list of lists of data integers

    readDPars(list<str>,list<list<int>>) --> void

    NOTE: Directory Data is not used for simple shapes readable by AutoCUT 1.0
    """
    
    lineNo = 0
    
    for dataLine in DPars:
        data = []
        data.append(int(dataLine[0:8]))
        data.append(int(dataLine[8:16]))
        data.append(int(dataLine[16:24]))
        data.append(int(dataLine[24:32]))
        data.append(int(dataLine[32:40]))
        if lineNo % 2 == 0: #If line is "Python Even" read next 4 data points
            data.append(int(dataLine[40:48]))
            data.append(int(dataLine[48:56]))
            data.append(int(dataLine[56:64]))
            data.append(int(dataLine[64:72]))
        data.append(int(dataLine[73:80]))
        
        lineNo += 1
        
        DParsM.append(data)


def readPPars(PPars,PParsM):
    """Convert Parameter Data List into a list of lists of data integers

    readPPars(list<str>,list<list<int>>) --> void
    """
    
    tempParsM, i = [], 0
    
    for dataLine in PPars:
        
        pData, rawData = [], []

        data, index = dataLine[:-13], dataLine[-13:]
        dataIndex, pIndex = index.split('P')
        dataIndex, pIndex = int(dataIndex), int(pIndex)

        rawData = data.split(';')
        rawData = rawData[0].split(',')
        
        for entry in rawData:
            try:
                pData.append(float(entry))
            except:
                pass
               
        if i != 0:
            if dataIndex == tempParsM[-1][-1]:  
                tempParsM[-1].insert(-1,pData)
                continue
                
        pData.append(dataIndex)
        tempParsM.append(pData)              
        i+=1

    for dataList in tempParsM:
        tempData = []
        pData = str(dataList)
        pData = pData.replace('[','')
        pData = pData.replace(']','')
        
        pDataList = pData.split(',')
        
        for j in pDataList:
            try:    tempData.append(float(j))
            except: pass
            
        tempData.insert(1,int(tempData[0]))
        tempData.__delitem__(0)
        tempData.insert(-1,int(tempData[-1]))
        tempData.__delitem__(-1)
        
        PParsM.append(tempData)
      

def filterPPars(PParsM):
    """Filter drafting lines and useless Parameter data from PParsM

    filterPPars(list<list<int, fl, fl...>) --> list<list<int, fl, fl...>>
    """
    
    pData, pDataF, pCoOrds, delIndexes = [], [], [], []
    parD = {100:par100,110:par110} #dict for calling coord getter
    
    for line in PParsM:     #Make list of Useful parameter data
        if line[0] in (100,110):
            pData.append(line)

    for line in pData:      #Make corresponding coordinates list
        if line[0] in parD:
            pCoOrds.append(parD.get(line[0])(line))

##    for i in range(len(pData)):       FILTERING SOME GOOD LINES OUT
##        connected = False           
##        for j in range(len(pData)):     
##            if pCoOrds[i][0]==pCoOrds[j][2] and pCoOrds[i][1]==pCoOrds[j][3]:
##                pDataF.append(pData[i])

    for i in range(len(pData)):  #Filter off solid edge draft lines
        if pCoOrds[i][0]<500 and pCoOrds[i][0]>15:
            if pCoOrds[i][1]>65 and pCoOrds[i][1]<350:
                pDataF.append(pData[i])
    
    return pDataF


def par110(pars, *midy):
    """Return start and end co-ordinates for 110: Line Entity
    Send y coords to flipHor that flips about midy if midy passed in

    Line Par: [110, X1, Y1, Z1, X2, Y2, Z2]

    par110(list<int, fl, fl...>, *float) --> (float, float, float, float)
    """

    xStart, yStart = pars[1], flipHor(pars[2], midy)
    xEnd,   yEnd   = pars[4], flipHor(pars[5], midy)

    return xStart,yStart,xEnd,yEnd


def par100(pars, *midy):
    """Return start and end co-ordinates for 100: Arc Entity
    Send y coords to flipHor which flips about midy if midy passed in

    Arc Par Data: [100, XT, XCenter, YCenter, X1, Y1, X2, Y2]
    
    par100(list<int, fl, fl...>, *float) --> (float, float, float, float)
    """
    
    xStart, yStart = pars[4], flipHor(pars[5], midy)
    xEnd,   yEnd   = pars[6], flipHor(pars[7], midy)

    return xStart,yStart,xEnd,yEnd


def parARC(pars, *midy):
    """Return centre point coords and start and end coords for Arc entity
    Send y coords to flipHor that flips about midy if midy passed in

    Arc Par Data: [100, XT, XCenter, YCenter, X1, Y1, X2, Y2]
    
    parARC(list<int, fl, fl...>, *float) --> (fl, fl, fl, fl, fl, fl)
    """

    xCentre, yCentre = pars[2], flipHor(pars[3], midy)
    xStart,  yStart  = pars[4], flipHor(pars[5], midy)
    xEnd,    yEnd    = pars[6], flipHor(pars[7], midy)

    return xCentre,yCentre,xStart,yStart,xEnd,yEnd
    

def drawARC(pars, xBuff, yBuff):
    """Return information needed to draw an arc entity
    return extent, start angle and xy coords for bounding square
    
    pars: [xCentre,yCentre,xStart,yStart,xEnd,yEnd]

    drawARC(list<float>, fl, fl) --> (fl, fl, fl, fl, fl, fl)
    """

    pars = fitArc(pars, xBuff, yBuff)
    xC,yC,x1,y1,x2,y2 = pars[0], pars[1], pars[2], pars[3], pars[4], pars[5]
    r = hypot(xC-x1, yC-y1)
    
    startAngle = findAngle(xC,y1,x1,yC)
    endAngle = findAngle(xC,y2,x2,yC)
    
    if endAngle < startAngle:
        endAngle += 360
        
    extDeg = endAngle - startAngle
    
    return xC - r, yC - r, xC + r, yC + r, extDeg, startAngle
    

def flipHor(yord, midy):
    """If midy passed in, return y ordinate flipped about middle y point,
    otherwise return y ordinate.

    flipHor(float, (float)) --> float
    """
    
    if midy == ():
        return yord
    
    return (yord + 2 * (midy[0] - yord))
            
    
def findStretch(parameters, canvasX, canvasY, bufferx, buffery, dim):
    """If dim False, return stretch factor to fit shape in canvas best as well
        as midy, xmin and ymin
       If dim True, return width, height, xmin, ymax

    findStretch(list<int, fl, fl...>, fl, fl, fl, fl, bool) --> fl, fl, fl, fl
                                                            --> fl, fl, fl, fl
    """
    
    xmin=xmax=ymin=ymax = 0
    
    for entry in parameters:
        if entry[0] == 110: #Line entities
            
            if xmin == 0:
                if par110(entry)[0] >= par110(entry)[2]:
                    xmax = par110(entry)[0]
                    xmin = par110(entry)[2]
            else:
                if par110(entry)[0] > xmax: xmax = par110(entry)[0]
                if par110(entry)[2] > xmax: xmax = par110(entry)[2]
                if par110(entry)[0] < xmin: xmin = par110(entry)[0]
                if par110(entry)[2] < xmin: xmin = par110(entry)[2]
            if ymin == 0:
                if par110(entry)[1] >= par110(entry)[3]:
                    ymax = par110(entry)[1]
                    ymin = par110(entry)[3]
            else:
                if par110(entry)[1] > ymax: ymax = par110(entry)[1]
                if par110(entry)[3] > ymax: ymax = par110(entry)[3]
                if par110(entry)[1] < ymin: ymin = par110(entry)[1]
                if par110(entry)[3] < ymin: ymin = par110(entry)[3]
                
        if entry[0] == 100: #Arc entities
      
            xC,yC,x1,y1,x2,y2 = parARC(entry)
            xMin,yMin,xMax,yMax = findArcMaxes(xC,yC,x1,y1,x2,y2,0)

            
            if xmin == 0:
                xmin = xMin
                xmax = xMax
            else:
                if xMin < xmin: xmin = xMin
                if xMax > xmax: xmax = xMax
            if ymin == 0:
                ymin = yMin
                ymax = yMax
            else:
                if yMin < ymin: ymin = yMin
                if yMax > ymax: ymax = yMax
            
    canvasX = canvasX - 4 - (2 * bufferx) #There seems to be 4 pixels added
    canvasY = canvasY - 4 - (2 * buffery) # to canvas dimensions

    width, height = xmax - xmin, ymax - ymin

    midy = (ymax + ymin) / 2
    stretchx, stretchy = canvasX / width, canvasY / height

    if dim:
        return width, height, xmin, ymax
    else:
        if stretchx < stretchy:
            return stretchx, midy, xmin, ymin
        else:
            return stretchy, midy, xmin, ymin
            
    
def getNoPar(lines):
    """Return number of lines of data sections

    getNoPar(str) --> list<int>

    Precondition: Last line of IGES file must have "S   #G   #D   #P   #T   #"
    """

    char = ["S","G","D","P","T"]
    numbers = []
    for i in range(4):
        before, rest = lines.split(char[i])
        num, rest = rest.split(char[i+1])
        numbers.append(int(num))
    return numbers


class virtualCut():
    def __init__(self, JCode):
        """Initialise virtual cut window

        Note: Canvas is set to 130 pixels less than screen height and 50 pixels
        less than screen width

        virtualCut(list<str, list<float>, float>) --> void
        """
        
        self.JCode = JCode
        self.lessThanHeight, self.lessThanWidth = 130, 50
        vCut = Toplevel()
        vCut.title("Virtual CUT")
        
        self.buttonFrame = Frame(vCut)
        self.buttonFrame.pack(side=TOP)

        self.drawFrame = Frame(vCut)
        self.drawFrame.pack(side=BOTTOM)        

        Button(self.buttonFrame, text="RUN", padx=80,
               command=self.runVCut).pack(side=LEFT)
        Button(self.buttonFrame, text="CLOSE", padx=80,
               command=vCut.destroy).pack(side=RIGHT)
        
        self.drawSpace = Canvas(self.drawFrame,
                    width = vCut.winfo_screenwidth() - self.lessThanWidth,
                    height = vCut.winfo_screenheight() - self.lessThanHeight)
        self.drawSpace.pack()
       
        self.bladeX = (self.drawSpace.winfo_reqwidth()-4)/2
        self.bladeY = (self.drawSpace.winfo_reqheight()-4)/2
        
        self.materialWidth, self.materialHeight = self.JCode[1]
        self.bladeWidth, self.bladeHeight = 4,8

        #Draw initial material and blade
        drawMaterial(self.drawSpace, self.bladeX, self.bladeY,
                     self.bladeX+self.materialWidth, self.bladeY,
                     self.bladeX+self.materialWidth, self.bladeY+\
                     self.materialHeight, self.bladeX, self.bladeY+\
                     self.materialHeight)
        drawBlade(self.drawSpace, self.bladeX, self.bladeY,
                  self.bladeWidth, self.bladeHeight)
        self.drawSpace.update()

        
    def runVCut(self):
        """Iterate through self.JCode and change where the material is drawn
        accordingly.

        self.JCode --  [["DIM"],
                        [width(float), height(float)],
                        ["INIT"],
                        [fl],[fl],...,
                        ["CUT"],
                        [translation(float), dOrient(float)]...]

        Initialise material and draw it at 0,0 with width and height. Move
        material to the left by number between INIT and CUT each repetition.
        After CUT, only translation or dOrient is non-zero in each entry, if
        translation is non-zero, move material and trail up by amount, if
        dOrient is non-zero rotate material and trail by dOrient degrees.

        runVCut(void) --> void
        """
        
        self.x = self.y = self.orient = 0
        
        x1,y1 = self.bladeX, self.bladeY
        x2,y2 = self.bladeX+self.materialWidth, self.bladeY
        x3,y3 = self.bladeX+self.materialWidth, self.bladeY+self.materialHeight
        x4,y4 = self.bladeX, self.bladeY+self.materialHeight
        
        dx1=dy1=dy2=dx4=0
        dx2=dx3=self.materialWidth
        dy3=dy4=self.materialHeight

        trail = []
        
        for entry in self.JCode:
            if type(entry) == str:
                if entry == "CUT":
                    self.orient+=90
                    trail.extend((0,0))
            elif type(entry) == float:
                x1,x2,x3,x4=x1-entry,x2-entry,x3-entry,x4-entry
                self.x+=entry
                dx1,dx2,dx3,dx4=dx1-entry,dx2-entry,dx3-entry,dx4-entry
                drawMaterial(self.drawSpace, x1, y1, x2, y2, x3, y3, x4, y4)
                drawBlade(self.drawSpace, self.bladeX, self.bladeY,
                          self.bladeWidth, self.bladeHeight)
                self.drawSpace.update()
                time.sleep(0.01)
                                
            elif type(entry) == list:
                if entry[0] and entry[1]:
                    pass
                elif entry[0]:
                    y1,y2,y3,y4=y1-entry[0],y2-entry[0],y3-entry[0],y4-entry[0]
                    oriRad = radians(self.orient)
                    x,y = entry[0]*cos(oriRad), entry[0]*sin(oriRad)
                    self.x, self.y = self.x+x, self.y+y
                    drawMaterial(self.drawSpace, x1, y1, x2, y2, x3, y3, x4, y4)
                    drawBlade(self.drawSpace, self.bladeX, self.bladeY,
                              self.bladeWidth, self.bladeHeight)
                    trail = moveTrail(trail, entry[0])
                    trail.extend((0,0))
                    self.drawTrail(self.drawSpace, trail)
                    self.drawSpace.update()
                    time.sleep(0.02)
                    
                else:
                    dx1, dy1 = x1-self.bladeX, y1-self.bladeY
                    dx2, dy2 = x2-self.bladeX, y2-self.bladeY
                    dx3, dy3 = x3-self.bladeX, y3-self.bladeY
                    dx4, dy4 = x4-self.bladeX, y4-self.bladeY

                    i=0
                    for (dx,dy) in [(dx1,dy1),(dx2,dy2),(dx3,dy3),(dx4,dy4)]:
                        if dx == 0:
                            if dy > 0: ori = 90
                            else: ori = 270
                        elif dy == 0:
                            if dx > 0: ori = 0
                            else: ori = 180
                        else:
                            ori = degrees(atan(abs(dy/dx)))
                            if dx > 0:
                                if dy > 0: pass
                                else: ori = 360 - ori
                            elif dx < 0:
                                if dy > 0: ori = 180 - ori
                                else: ori = 180 + ori
                                
                        if ori < 0: ori += 360
                        if ori > 360: ori -= 360
                        
                        if i == 0: ori1 = ori
                        elif i == 1: ori2 = ori
                        elif i == 2: ori3 = ori
                        else: ori4 = ori
                        i+=1
                            
                    ori1, ori2 = entry[1] + ori1, entry[1] + ori2
                    ori3, ori4 = entry[1] + ori3, entry[1] + ori4
                                        
                    d1, d2 = hypot(dx1,dy1), hypot(dx2, dy2)
                    d3, d4 = hypot(dx3,dy3), hypot(dx4, dy4)

                    ddy1 = (d1 * sin(radians(ori1))) - dy1
                    ddx1 = (d1 * cos(radians(ori1))) - dx1
                    ddy2 = (d2 * sin(radians(ori2))) - dy2
                    ddx2 = (d2 * cos(radians(ori2))) - dx2
                    ddy3 = (d3 * sin(radians(ori3))) - dy3
                    ddx3 = (d3 * cos(radians(ori3))) - dx3
                    ddy4 = (d4 * sin(radians(ori4))) - dy4
                    ddx4 = (d4 * cos(radians(ori4))) - dx4
                    
                    x1, y1 = x1 + ddx1, y1 + ddy1
                    x2, y2 = x2 + ddx2, y2 + ddy2
                    x3, y3 = x3 + ddx3, y3 + ddy3
                    x4, y4 = x4 + ddx4, y4 + ddy4
                    
                    self.orient -= entry[1]
                    if self.orient < 0: self.orient+=360
                    if self.orient > 360: self.orient-=360
                    
                    drawMaterial(self.drawSpace, x1, y1, x2, y2, x3, y3, x4, y4)
                    drawBlade(self.drawSpace, self.bladeX, self.bladeY,
                              self.bladeWidth, self.bladeHeight)
                    trail = rotateTrail(trail, entry[1])
                    self.drawTrail(self.drawSpace, trail)
                    self.drawSpace.update()
                    time.sleep(0.005)
        
        newXYs = [] #Display final shape after demonstration has finished
        for i in range(0,len(trail),2):
            newXYs.extend((trail[i]+self.bladeX, trail[i+1]+self.bladeY))
        self.drawSpace.delete("all")
        self.drawSpace.create_polygon(newXYs, outline="Black", fill="Brown")
        drawBlade(self.drawSpace, self.bladeX, self.bladeY,
                  self.bladeWidth, self.bladeHeight)
        self.drawSpace.update()
        
                    
    def drawTrail(self, canvas, xys):
        """Add blade position to every point in trail list then display them as
        white lines

        drawTrail(Canvas, list<float>) --> void
        """

        newXYs = []
        for i in range(0,len(xys),2):
            newXYs.extend((xys[i]+self.bladeX, xys[i+1]+self.bladeY))
        canvas.create_line(newXYs, fill="White")
        

def rotateTrail(xys, rotate):
    """Return xys with each coordinate rotated about the saw blade

    rotateTrail(list<float>, float) --> list<float>
    """

    newXYs = []
    for i in range(0,len(xys),2):
        x,y = xys[i], xys[i+1]
        d = hypot(x,y)
        if x == 0:
            if y > 0: ang = 90
            elif y < 0: ang = 270
            else:
                newXYs.extend((0,0))
                continue
        elif y == 0:
            if x > 0: ang = 0
            else: ang = 180
        else:
            ang = degrees(atan(abs(y/x)))
            if y > 0:
                if x > 0: pass
                else: ang = 180 - ang
            else:
                if x > 0: ang = 360 - ang
                else: ang = 180 + ang
        ang += rotate
        if ang > 360: ang -= 360
        if ang < 0: ang += 360
        newXYs.extend((d*cos(radians(ang)), d*sin(radians(ang))))
        
    return newXYs


def moveTrail(xys, yMove):
    """Return xys with yMove subtraced from the y ords in xys

    moveTrail(list<float>, float) --> list<float>
    """
    
    newXYs = []
    for i in range(len(xys)):
        if i%2==0:
            newXYs.append(xys[i])
        else:
            newXYs.append(xys[i]-yMove)
    return newXYs


def drawMaterial(canvas, x1, y1, x2, y2, x3, y3, x4, y4):
    """Clear canvas then draw material on canvas with a polygon through x,y
    coords

    drawMaterial(Canvas, fl, fl, fl, fl, fl, fl, fl, fl) --> void
    """

    canvas.delete('all')
    canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4,
                          fill="brown")
    

def drawBlade(canvas, x, y, w, h):
    """Draw blade in centre of Virtual CUT canvas

    drawBlade(Canvas, float, float, float, float) --> void
    """

    canvas.create_polygon(x,y, x-(w/2),y-(w/2), x-(w/2),y-h-(w/2),
                          x+(w/2),y-h-(w/2), x+(w/2),y-(w/2),
                          outline = "black", fill="yellow")


class splashScreen(Toplevel):
    """Display splash screen in middle of screen with no windows borders. If PIL
    module was loaded use slpash.jpg, otherwise use splash.gif.

    splashScreen() --> void
    """
    
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.overrideredirect(True)
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        if PIL:
            image_file = Image.open("splash.jpg")
            image = ImageTk.PhotoImage(image_file)
        else:
            image = PhotoImage(file="splash.gif")
        imgheight = image.height()
        imgwidth = image.width()
        self.geometry("%dx%d+%d+%d" % (imgwidth, imgheight,
                               width/2-imgwidth/2, height/2-imgheight/2))

        canvas = Canvas(self, height=imgheight, width=imgwidth)
        canvas.create_image(imgwidth/2, imgheight/2, image=image)
        canvas.pack()
        self.update()
        

class aboutBox(Toplevel):
    """Display about box"""
    def __init__(self):
        Toplevel.__init__(self)
        
        self.title("AutoCUT 1.0")
        width, height, rootX, rootY = 300, 200, 300, 200
        self.geometry("%dx%d+%d+%d" % (width, height, rootX, rootY))
        aboutTitle = Label(self, text="AutoCUT 1.0")
        aboutTitle.pack(side=TOP)
        aboutAuthour = Label(self,
                             text="All program functions and algorithms")
        aboutAuthour.pack(side=TOP)
        aboutInfo = Label(self,text="(C) 2008, Jonathan Keller")
        aboutInfo.pack()
        self.wait_window(self)


class optionsBox(Toplevel):
    """Initialise Options Box. Options box has entries for node resolution,
    turn rate, and turning node resolution. These values are stored in
    self.nodeRes, self.turnRes and self.turnRate so that the main program
    can get them directly :-(

    optionsBox() --> void
    """
    def __init__(self, turnRate, nodeRes, turnRes):
        Toplevel.__init__(self)
        self.title("JCode Options")
        width, height, rootX, rootY = 450, 150, 300, 200
        self.geometry("%dx%d+%d+%d" % (width, height, rootX, rootY))
        labelFrame = Frame(self)
        labelFrame.pack(side=LEFT)
        entryFrame = Frame(self)
        entryFrame.pack(side=LEFT)
        lastFrame = Frame(self)
        lastFrame.pack(side=LEFT)
        
        okButton = Button(self, text="OK", command=self.OK)
        okButton.pack(side=BOTTOM)

        self.bind("<Return>", self.OK)
        self.grab_set()
        
        Label(labelFrame, text="Node Resolution: ").pack(side=TOP)
        Label(labelFrame, text="Turning Node Resolution: ").pack(side=TOP)
        Label(labelFrame, text="Turning Rate: ").pack(side=TOP)
        
        self.node, self.trnN, self.trnR = DoubleVar(), DoubleVar(), DoubleVar()
        self.node.set(nodeRes)
        self.trnN.set(turnRes)
        self.trnR.set(turnRate)
        
        nodeEntry = Entry(entryFrame, textvariable=self.node)
        nodeEntry.pack(side=TOP)
        turn1Entry = Entry(entryFrame, textvariable=self.trnN)
        turn1Entry.pack(side=TOP)
        turn2Entry = Entry(entryFrame, textvariable=self.trnR)
        turn2Entry.pack(side=TOP)

        Label(lastFrame, text="Translation (mm) per iteration").pack(side=TOP)
        Label(lastFrame, text="Resolution (mm) of arc nodes").pack(side=TOP)
        Label(lastFrame, text="Rotation (degrees) per iteration").pack(side=TOP)

        self.wait_window(self)
        
        
    def OK(self, event=None):
        """return entry box data and destroy window

        OK() --> float, float, float
        """
        
        self.turnRate = self.trnR.get()
        self.nodeRes = self.node.get()
        self.turnRes = self.trnN.get()
        self.destroy()
        

root = Tk()

app = mainWindow(root)
root.withdraw()
splash = splashScreen(root)

time.sleep(4.50)

splash.destroy()
root.deiconify()

root.mainloop()
