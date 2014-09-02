########################################
#   Name: Robert Knight
#   Number: 41777903
#   Assignment 3


from pygame import *
import os, math, copy, random

####################################
#
#       Define levels
#
#####################################
level1 = [[0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 ,'C', 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 3 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 1 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          ['A', 0 , 0 , 3 , 1 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [1 , 1 , 1 , 2 , 1 , 1 , 1 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 2 , 0 , 0 , 0 , 0 , 0 , 1 , 0 , 0],
          [0 ,'B', 0 , 2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 0 , 0 , 1],
          [0 , 1 ,'X', 1 , 0 , 1 , 0 , 0 , 1 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1],
          ['Z', 0 , 0 , 0 , 0 , 3 , 0 , 0 , 3 , 0 , 0,'D'],
          [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1]]
level2 = [[1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [3 , 0 , 0 , 0 , 0 ,'Z', 0 , 0 , 0 , 0 , 0 , 3],
          [1 , 1 , 2 , 1 , 2 , 1 , 1 , 2 , 1 , 1 , 2 , 1],
          ['E', 0 , 2 , 0 , 2 , 0 , 0 , 2 , 0 , 0 , 2 ,'F'],
          [0 , 3 , 2 , 0 , 2 ,'A', 0 , 2 , 3 , 0 , 2 , 0],
          [1 , 1 , 1 , 2 , 1 , 1 , 2 , 1 , 1 , 2 , 1 , 1],
          [1 , 1 , 0 , 2 , 0 , 0 , 2 , 0 , 0 , 2 , 1 , 1],
          [1 , 1 , 0 , 2 , 0 , 0 , 2 , 0 , 0 , 2 , 1 , 1],
          [1 , 1 , 2 , 1 , 2 , 1 , 1 , 2 , 1 , 2 , 1 , 1],
          [0 , 0 , 2 , 0 , 2 , 0 , 0 , 2 , 0 , 2 , 0 , 0],
          [0 , 0 , 1 , 0 , 1 , 0 , 0 , 1 , 0 , 1 , 0 , 0],
          [1 , 0 , 0 , 0 , 0 ,'B', 0 , 0 , 0 , 0 , 0 , 1],
          [1 , 0 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 0 , 1],
          [1 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1],
          [1 , 1 , 2 , 1 , 2 , 1 , 2 , 1 , 2 , 1 , 1 , 1],
          [1 , 0 , 2 , 0 , 2 , 0 , 2 , 0 , 2 , 0 , 0 , 1],
          [1 , 0 , 2 , 0 , 2 , 0 , 2 , 0 , 2 , 0 , 0 , 1],
          [0 , 0 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 1 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 0],
          [3 , 1 ,'C', 0 , 0 ,'X', 0 , 0 , 0 ,'D', 1 , 3],
          [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1]]
level3 = [[1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [3 , 0 , 0 , 0 , 0 ,'E', 0 , 0 , 0 , 0 , 0 , 0],
          [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1],
          [0 , 0 , 3 , 0 , 0 ,'B', 0 , 0 , 0 , 0 , 3 , 1],
          [2 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1],
          [2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [2 , 0 ,'F', 0 , 0 , 0 , 0 , 3 , 0 ,'Z', 0 , 0],
          [1 , 0 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,'A', 0 , 0],
          [0 , 0 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [1 , 0 , 0 ,'D', 3 , 0 , 0 , 0 , 3 , 0 , 0 , 0],
          [0 , 0 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 1 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1],
          [1 , 1 , 0 , 3 , 0 , 0 , 0 , 0 , 3 , 0 , 1 , 1],
          [0 , 0 , 1 , 1 , 1 , 2 , 1 , 1 , 1 , 1 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 2 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 2 , 0 , 0 , 0 , 0 , 0 , 0],
          ['X', 0 , 0 , 0 , 0 , 2 , 0 , 0 , 0 , 0 , 3 ,'C'],
          [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1]]
level4 = [[1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
          [1 , 2 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 2 , 1],
          [0 , 2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 0],
          [0 , 2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 0],
          [0 , 2 , 0 , 0 , 0 ,'X', 0 , 0 , 0 , 0 , 2 , 0],
          [0 , 2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 0],
          [1 , 2 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 2 , 1],
          [0 , 2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 0],
          [0 , 2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 0],
          [0 , 2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 0],
          [0 , 2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 0],
          [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1]]
          
level1enA = [0,4,True,[2,2,0,0,0,0,0,0,1,1]]
level1enB = [0,4,True,[0,0,2,2,1,1,1,1,0,0,2,0]]
level1enC = [60,3,True,[3]]
level1enD = [0,1,False,[1]]
level1Dict = {'A':level1enA,'B':level1enB,'C':level1enC,'D':level1enD}
level2enA = [0,4,True,[1,0]]
level2enB = [0,4,True,[0,1]]
level2enC = [20, 2, True,[3]]
level2enD = [21, 2, True, [3]]
level2enE = [4, 1, False, [4]]
level2enF = [6, 1, False, [4]]
level2Dict = {'A':level2enA,'B':level2enB,'C':level2enC,'D':level2enD,'E':level2enE,'F':level2enF}
level3enA = [0,1,False,[2]]
level3enB = [3,1,False,[1,1,1,1,1,1,1,1,1,1,1]]
level3enC = [0,10,True,[2,4,3,3]]
level3enD = [0,3,False,[5,1,2,1]]
level3enE = [20,3,False,[5,2,2]]
level3enF = [30,5,True,[1,2]]
level4Dict = {}
level3Dict = {'A':level3enA,'B':level3enB,'C':level3enC,'D':level3enD,'E':level3enE,'F':level3enF}
levelAr = [level1, level2,level3,level4]
enGenAr = [level1Dict,level2Dict,level3Dict,level4Dict]

class Game:
    """controls all the gameplay action, and holds instances of most classes"""
    def __init__(self, levelAr, initDiff, initLives):
        width = 400
        height = 650
        self.width = width # Width for game
        self.height = height
        screenwidth = width + 150 # Width for game plus the display
        self.p1_height = 16 # Size of player rectangle
        self.p1_width = 10
        p1_SHeight = 30 # Size for player surface
        p1_SWidth = 30
        self.curLevel = 1 # Creating a game sets the level down to one
        self.scoreInt = 0 # Start score at 0
        self.scoreTot = self.scoreInt
        self.livesInt = initLives 
        self.livesCur = self.livesInt # At start of game the player's lives reset to initial value
        self.diffInt = initDiff # This will be passed from Menu class
        self.diffCur = initDiff # Difficulty increases slightly halfway through and significantly at loop end
        self.time = 200 - 5*self.diffCur
        # Player class attributes
        self.gravity = 1
        self.jumpstrength = 12
        self.walkspeed = 4
        self.swordtime = 10
        # Define the master display surface
        self.surface1 = display.set_mode((screenwidth, height))
        
        self.initLevel(self.curLevel)
        self.swords = [] # List to hold the instance of a Sword class
        self.rectangleUpdate = [] # A list containing rectangles where a change occured graphically
        self.fontDisp = font.Font(os.path.join('data','DejaVuSerif.ttf'), 16)
        self.sidebar = image.load(os.path.join('data','sidebar.png')).convert()
        
    def initLevel(self, curLevel):
        """Initialises a level for use by the Game class. To be called after a death or when going to next level
        initLevel(int) -> None"""
        self.LDown = 0 # All the following buttons should not be pressed initially
        self.RDown = 0
        self.UDown = 0
        self.DDown = 0
        # Lists to hold Rects or Surfaces that the main function will check through
        self.enList = []
        self.enSurfList = []
        self.shotList = []
        self.state = 'Begin' # State of game for controlling main loop stuff. Can be 'Play', 'Win', Lose' or 'Begin'
        self.background = image.load(os.path.join('data','BG'+str(curLevel)+'.jpg')).convert()
        enGenAr1 = copy.deepcopy(enGenAr) # Copy enemy generator list defined at beginning so no hard changes occur
        self.level = Level(levelAr[curLevel-1], enGenAr1[curLevel-1], self.time, self.width, self.height) # Creating the level class
        self.level.drawLevel()
        self.Fsurface = image.load(os.path.join('data','FG'+str(curLevel)+'.jpg')).convert() #Uses jpg because png files were too large for no better quality
        # Create the initial surfaces
        for i in self.level.blockRect:
            self.level.blockSurf.append(self.Fsurface.subsurface(i))
        self.b2surf = transform.scale(image.load(os.path.join('data','ladder.png')).convert(), (self.level.deltaX, self.level.deltaY))
        self.b2surf.set_colorkey((255,255,255))
        self.P1 = Player(self.gravity, self.jumpstrength, self.walkspeed, self.swordtime, self.level.getInitX(), self.level.getInitY(), self.p1_width, self.p1_height)
        self.p1surf = image.load(os.path.join('data','P1.png')).convert()
        self.p1surf.set_colorkey((255,255,255))
        self.levelEndSurf = image.load(os.path.join('data','levelEnd.png')).convert()
        self.levelEndSurf.set_colorkey((255,255,255))
        self.shotSurf = image.load(os.path.join('data','shot.png')).convert()
        self.shotSurf.set_colorkey((255,255,255))
        self.ballSurf = image.load(os.path.join('data','ball.png')).convert()
        self.ballSurf.set_colorkey((255,255,255))
        if curLevel == 4:
            self.enList.append(Enemy(self.width/2,0,6))
            self.enSurfList.append(image.load(os.path.join('data','boss100.png'))) # image format 1st num = action, 2nd num = varient, 3rd num = animationS
            self.enList[0]._action = 7
            self.enSurfList[0].set_colorkey((255,255,255))
        # Initialise sounds
        mixer.music.load(os.path.join('data','mscLev'+str(curLevel)+'.mp3'))
        mixer.music.play(-1)
        self.sndJump = mixer.Sound(os.path.join('data','sndJump.wav'))
        self.sndPigJump = mixer.Sound(os.path.join('data','sndPigJump.wav'))
        self.sndBallShot = mixer.Sound(os.path.join('data','sndBallShot.wav'))
        self.sndBeeShot = mixer.Sound(os.path.join('data','sndBeeShot.wav'))
        self.sndHope = mixer.Sound(os.path.join('data','sndHope.wav'))
        self.sndSpawn = mixer.Sound(os.path.join('data','sndSpawn.wav'))
        self.sndEnDie = mixer.Sound(os.path.join('data','sndEnDie.wav')) 
        self.sndSword = mixer.Sound(os.path.join('data','sndSword.wav'))
        self.flipDisp = True
        
    def updateSideBar(self, secFrac):
        """Update the side bar to display game information
        (int) -> [Rect, .... , Rect]"""
        self.surface1.blit(self.sidebar, (self.width, 0))
        updateList = []
        if secFrac % 10 == 1:
            self.scoreText = self.fontDisp.render(str(self.scoreTot), True, (0,0,0))
            self.timeText = self.fontDisp.render(str(self.level._time), True, (0,0,0))
            self.livesText = self.fontDisp.render(str(self.livesCur), True, (0,0,0))
            self.hopesText = self.fontDisp.render(str(len(self.level.hopes)), True, (0,0,0))
            updateList = [Rect(460, 300, 90, 30), Rect(500, 150, 50, 30), Rect(500, 450, 50, 30), Rect(500, 550, 50, 30)]
        self.surface1.blit(self.scoreText, (460, 300))
        self.surface1.blit(self.timeText, (500, 150))
        self.surface1.blit(self.livesText, (500, 450))
        self.surface1.blit(self.hopesText, (500, 550))
        return updateList # Return a list to add to the main function's rectangle updates
    def eventA(self,curEve):
        """Check for keyboard events, pass input to player class, then return 1 for continue play, 0 to exit main loop
        eventA(Event) -> int"""
        if curEve.type == QUIT:
            return 0
        if curEve.type == KEYDOWN:
            if curEve.key == K_LEFT:
                self.LDown = 1
                return 1
            elif curEve.key == K_RIGHT:
                self.RDown = 1
                return 1
            elif curEve.key == K_UP:
                self.UDown = 1
                return 1
            elif curEve.key == K_DOWN:
                self.DDown = 1
                return 1
            elif curEve.key == K_z:
                if self.P1.jump((self.LDown,self.RDown)) == 1:
                    self.sndJump.play()
                return 1
            elif curEve.key == K_ESCAPE:
                return 0
            elif curEve.key == K_x:
                if self.P1.attack(self) == 1:
                    self.sndSword.play()
                return 1
            else:
                return 1
        elif curEve.type == KEYUP:
            if curEve.key == K_LEFT:
                self.LDown = 0
            elif curEve.key == K_RIGHT:
                self.RDown = 0
            elif curEve.key == K_UP:
                self.UDown = 0
            elif curEve.key == K_DOWN:
                self.DDown = 0
            return 1
        else:
            return 1
    def main(self):
        """The loop to go through each game clock cycle"""
        exe = 1 # If exe is not 1 then main loop will break
        secFrac = 0 # Integer 1/50 seconds
        hopeloop = 0 
        spawningList = [] # List containing enemy generator values that will spawn enemy next second
        while exe == 1:
            # Initialisers
            rectangleUpdate = [] # A list containing rectangles where a change occured graphically
            ######################################
            #
            #   When the game action is happening
            #
            ######################################
            if self.state == 'Play':
                

                # Inputs:
                curEve = event.poll()
                exe = self.eventA(curEve)
                if self.LDown == 1:
                    self.P1.moveleft()
                elif self.RDown == 1:
                    self.P1.moveright()
                
                self.P1._vspeed += self.P1._gravity # Increase the falling speed of player with gravity. Resets to 0 later if on ground
                # Short jump movements:
                if self.P1._vspeed == -4 and self.P1._hspeed == 0:
                    if self.LDown == 1:
                        self.P1._hspeed = - self.P1._walkspeed / 2
                    elif self.RDown == 1:
                        self.P1._hspeed = self.P1._walkspeed / 2 
                # Collisions between blocks and player:
                for i in self.level.block:
                    for j in i:
                        if j != 0:
                            # Stop player falling through the floor
                            if self.P1._vspeed > 0:
                                self.P1._canmove = 0
                                if j._type == 1 or j._type == 2:
                                    if j.collidepoint(self.P1[0]+1,self.P1[1]+self.P1[3]+self.P1._vspeed)\
                                       or j.collidepoint(self.P1[0]+self.P1[2]-1,self.P1[1]+self.P1[3]+self.P1._vspeed):
                                        self.P1._canmove = 1
                                        self.P1._hspeed = 0
                                        self.P1._vspeed = 0
                                        while self.P1.colliderect(j) == False:
                                            self.P1.move_ip(0, 1)
                            # Allow vertical movement on a ladder
                            if j._type == 2 and j.colliderect(self.P1):
                                if j.collidepoint(self.P1[0]+self.P1[2]/2,self.P1[1]+self.P1[3]/2):
                                    self.P1._canmove = 0
                                if self.UDown == 1:
                                    self.P1.move_ip(0, -5)
                                elif self.DDown == 1:
                                    self.P1.move_ip(0, 5)
                            # Stop player moving into a block from any direction:
                            if j._type == 1:
                                if self.LDown == 1 or self.P1._hspeed < 0:
                                    if j.collidepoint(self.P1[0], self.P1[1]+self.P1[3]/2):
                                        self.P1._hspeed = 0
                                        while self.P1.colliderect(j) == True:
                                            self.P1.move_ip(1, 0)
                                if self.RDown == 1 or self.P1._hspeed > 0:
                                    if j.collidepoint(self.P1[0]+self.P1[2], self.P1[1]+self.P1[3]/2):
                                        self.P1._hspeed = 0
                                        while self.P1.colliderect(j) == True:
                                            self.P1.move_ip(-1, 0)
                                if self.DDown == 1:
                                    if j.collidepoint(self.P1[0]+1,self.P1[1]+self.P1[3]/2+5)\
                                       or j.collidepoint(self.P1[0]+self.P1[2]-1,self.P1[1]+self.P1[3]/2+5):
                                        
                                        self.P1._canmove = 1
                                        self.P1._hspeed = 0
                                        self.P1._vspeed = 0
                                        self.P1.move_ip(0, -5)
                           
                                if self.P1._vspeed < 0:
                                    if j.collidepoint (self.P1[0]+5,self.P1[1]+self.P1._vspeed)\
                                       or j.collidepoint(self.P1[0]+self.P1[2]-5,self.P1[1]+self.P1[3]+self.P1._vspeed):
                                        self.P1._canmove = 0
                                        self.P1._vspeed = 1
                            #Collisions between blocks and enemy type 1 (since it is effected by gravity
                            if j._type == 1 or j._type ==2:
                                for k in self.enList:

                                    if k._type == 1:
                                        if k._action != 6 and k._action != 7:
                                            while j.collidepoint(k[0]+k[2]/2, k[1]+k[3]):
                                                k.moveup(1)
                # Collision between Hope and player
                for i in self.level.hopes:
                    if i.colliderect(self.P1):
                        self.scoreTot += 100
                        self.sndHope.play()
                        rectangleUpdate.append(i)
                        self.level.hopes.remove(i)
                # Other movements
                self.P1.move_ip(self.P1._hspeed, self.P1._vspeed)
                # Remove swords and reduce swordframes
                if self.P1._swordframe > 0:
                    self.P1._swordframe -= 1
                try:
                    self.swords[0]._swordframe -= 1
                    if self.swords[0]._swordframe == 0:
                        self.swords = []
                except:
                    ''
                # Stop player from moving off edge of screen
                while self.P1[0]+self.P1[2] > self.width:
                    self.P1.move_ip(-1, 0)
                while self.P1[0] < 0:
                    self.P1.move_ip(1, 0)
                # If player won. This is different for boss levels
                if self.curLevel != 4:
                    if self.P1.colliderect(self.level.WinRect) and len(self.level.hopes) == 0:
                        self.state = 'Win'
                        secFrac = 0
                        self.enList=[]
                        self.enSurfList=[]
                        spawningList = []
                        mixer.music.stop()
                        mixer.music.load(os.path.join('data','mscWin.mp3'))
                        mixer.music.play()
                    
                    
                #Enemy movement handling
                indexI = 0
                for i in self.enList:
                    # BUBBLE ENEMIES - After time choose an action and move directly. 
                    if i._type == 1:
                        i._count += 1
                        i.movedown(3)
                        if i._count == 66 - 3 * self.diffCur: 
                            i._action = random.randint(0, 7) #0 and 1 is stop, 2 and 3 is left, 4 and 5 is right, 6 is down, 7 is up
                            i._count = 0
                        if i._action == 0 or i._action == 1:
                            ''
                        elif i._action == 2 or i._action == 3:
                            i.moveleft(1 + self.diffCur/2) 
                        elif i._action == 4 or i._action == 5:
                            i.moveright(1 + self.diffCur/2) 
                        elif i._action == 6:
                            ''
                        elif i._action == 7:
                            i.moveup(6)
                        # Wrap at edge of screen
                        if i[0] > self.width-2:
                            i[0] = 0
                        elif i[0]+i[2] < 2:
                            i[0] = self.width - i[2]
                        # Stop from falling below or above the gameplay area
                        if i[1] > self.height - 100 and i._action ==6:
                            i._action = 0
                        if i[1] < 100 and i._action == 7:
                            i._action = 0
                        if i[1] > self.height:
                            self.enList.pop(indexI)
                            self.enSurfList.pop(indexI)
                        else:
                            self.enSurfList[indexI] = image.load(os.path.join('data', 'en1'+str(i._action)+'0.png')).convert()
                            self.enSurfList[indexI].set_colorkey((0,0,255))
                    # PIG ENEMIES - Run left and right if there is a block at the right position
                    if i._type == 2: # actions: 0 is left, 1 is right, 2 is jump left, 3 is jump right
                        if i._action == 0:
                            i.moveleft(1+self.diffCur/3) 
                            if Rect(i[0]-i[2]/2, i[1]+i[3]+2, 3, 3).collidelist(self.level.blockRect) == -1 or i[0] < 1:
                                i._action = 1
                            if self.P1.colliderect(Rect(0, i[1]-1, self.width, i[3]+2)):
                                i.moveleft(3)
                                # If a jumping pig and player in range, then jump
                                if i._var == 1 and self.P1.colliderect(Rect(i[0]-50, i[1]-1, 50, i[3]+2)):
                                    i._vspeed = -8
                                    i._hspeed = -4
                                    i.moveup(2)
                                    i._action = 2
                                    self.sndPigJump.play()
                            
                        elif i._action == 1:
                            i.moveright(1+self.diffCur/3) 
                            if Rect(i[0]+i[2]*3/2, i[1]+i[3]+2, 3, 3).collidelist(self.level.blockRect) == -1 or i[0] > self.width - i[2]-1:
                                i._action = 0
                            if self.P1.colliderect(Rect(0, i[1]-1, self.width, i[3]+2)):
                                i.moveright(3)
                                if i._var == 1 and self.P1.colliderect(Rect(i[0]+i[2], i[1]-1, 50, i[3]+2)):
                                    i._vspeed = -8
                                    i._hspeed = 4
                                    i.moveup(2)
                                    i._action = 3
                                    self.sndPigJump.play()
                            
                        if i._var == 1:
                            if i[1] < i._yint:
                                i._vspeed += 1
                            else:
                                i._vspeed = 0
                                i._hspeed = 0
                                if i._action == 2:
                                    i._action = 0
                                elif i._action == 3:
                                    i._action = 1
                            i.movedown(i._vspeed)
                            i.moveright(i._hspeed)
                        if secFrac % 5 == 0:
                            self.enSurfList[indexI] = image.load(os.path.join('data', 'en2'+str(i._action)+str(secFrac/25)+'.png')).convert() # May need to be secFrac - 1 ?
                            self.enSurfList[indexI].set_colorkey((255,255,255))
                    # HOMING ENEMIES - Follow player
                    if i._type == 3:
                        playerpos = (self.P1[0]+self.P1[2]/2, self.P1[1]+self.P1[3]/2) # The centre of player
                        if i._var == 0:
                            
                            i.movetowards(playerpos, self.diffCur)
                        # If a 2nd varient, move position to move slightly over
                        else:
                            if i._count == 0:
                                i._action += 1
                                i._count = 10
                                displacement = 10*(20 - i._action)
                                displacementMov = random.choice([-displacement, displacement])
                                i._1 = (playerpos[0]+displacementMov, playerpos[1]+displacementMov) # Position to move to for 10 frames
                            i._count -= 1
                            i.movetowards(i._1, 1+self.diffCur) 
                        # Avoid the sword if possible
                        if len(self.swords) == 1:
                            i.movetowards((-playerpos[0],-playerpos[1]), 3 + self.diffCur) 
                        if secFrac % 25 == 0:
                            self.enSurfList[indexI] = image.load(os.path.join('data', 'en30'+str(secFrac/25)+'.png')).convert()
                            self.enSurfList[indexI].set_colorkey((255,255,255))
                    # HORNET ENEMIES - After a time choose a direction to move (up or down)
                    if i._type == 4:
                        i._count += 1
                        if i._count == 20 + 5 * (10 - self.diffCur):
                            i._action = random.randint(0, 1) # Direction to move (up or down)
                            number = random.randint(0, 2)
                            i._1 = 30 * number # Pixels above player to fire a shot
                            i._count = 0
                            i._shot = False
                        if i._action == 0:
                            i.moveup(5 + self.diffCur)
                        elif i._action == 1:
                            i.movedown(5 + self.diffCur)
                        # Stop it from moving above or below the game area:
                        if i[1] < 30:
                            i._action = 1
                        elif i[1] > self.height - 30:
                            i._action = 0
                        if i[1] > self.P1[1] - i._1 - 5 and i[1] < self.P1[1] -i._1 + 5 and i._shot == False: #if in range of firing position go to position then fire shot
                            i[1] = self.P1[1] - i._1
                            self.shotList.append(Shot(i[1], i._var))
                            self.sndBeeShot.play()
                            i._shot = True
                    # Volcano enemies - after a time, fire a shot
                    if i._type == 5:
                        i._count += 1
                        if i._count == 200 - 15 * self.diffCur:
                            self.shotList.append(Ball(i))
                            self.sndBallShot.play()
                            i._count = 0

                    # Boss character. Actions are: 0 = Move to a position, 1 = Move to a position (Fast), 2 = Shooting, 3 = Spawning enemies, 4 = Hoarding enemies,
                    # 5 = Firing Balls
                    if i._type == 6:
                        i._count += 1
                        # After a time, change action
                        if i._count == 150 - 30 * self.diffCur:
                            if i._action >= 2:
                                i._action = 0
                                posX = random.choice([0,self.width-50, self.width/2])
                                if posX == self.width/2:
                                    posY = random.choice([200, 500])
                                else:
                                    posY = random.choice([260,330,420,450,550,590])
                                i._1 = (posX, posY) # Position to fly to
                                i._count -= 40
                                if posX > i[0]:
                                    i._var = 0
                                else:
                                    i._var = 1
                            elif i._action == 0:
                                i._count = 0
                                i._action = 1
                                if posX > i[0]:
                                    i._var = 0
                                else:
                                    i._var = 1
                                    
                            else:
                                if posX == 0:
                                    i._var = 0
                                    if posY in [260,420,550]:
                                        i._action = 2
                                        i._2 = 1
                                    else:
                                        i._action = 3
                                    
                                elif posX == self.width-50:
                                    i._var = 1
                                    if posY in [260,420,550]:
                                        i._action = 2
                                        i._2 = 1
                                    else:
                                        i._action = 3
                                else:
                                    i._var = 0
                                    if posY == 200:
                                        i._action = 5
                                        i._2 = random.randint(0 , 1)
                                    else:
                                        i._action = 4
                                i._count = 0
                            for j in i._spawnList:
                                spawntype = random.choice([1,3])
                                self.enList.append(Enemy(j[0], j[1], spawntype))
                                self.enSurfList.append(image.load(os.path.join('data','en'+str(spawntype)+'00.png')).convert())
                                i._spawnList.remove(j)
                            self.enSurfList[0] = image.load(os.path.join('data','boss'+str(i._action)+str(i._var)+str(secFrac/25)+'.png')).convert()
                            self.enSurfList[0].set_colorkey((255,255,255))
                        # Perform action consequences
                        if i._action == 0:
                            i.movetowards(i._1, 1+self.diffCur)
                        elif i._action == 1:
                            i.movetowards(i._1, 1+3*self.diffCur)
                        elif i._action == 2:
                            if i._2 == 0:
                                i.movedown(3+self.diffCur)
                                if i[1] > posY + 50:
                                    i._2 = 1
                            else:
                                i.moveup(3+self.diffCur)
                                if i[1] < posY - 50:
                                    i._2 = 0
                            if i._count % 3 == 0:
                                self.shotList.append(Shot(i[1]+8, i._var))
                                self.sndBeeShot.play()
                        elif i._action == 3:
                            if i._count % (80-3*self.diffCur) == 0:
                                i._spawnList.append((i[0]+10, i[1]+6))
                                self.sndSpawn.play()
                        elif i._action == 4:
                            if i._count % (50-3*self.diffCur) == 0:
                                i._spawnList.append((random.randint(0, self.width - 50),random.choice([260,330,420,450,550,590])))
                                self.sndSpawn.play()
                        elif i._action == 5:
                            if i._2 == 0:
                                i.moveleft(6+self.diffCur)
                                if i[0] < 10:
                                    i._2 = 1
                            else:
                                i.moveright(6+self.diffCur)
                                if i[0] > self.width - 50:
                                    i._2 = 0
                            if i._count % (10-self.diffCur) == 0:
                                self.shotList.append(Ball((i[0],i[1])))
                                self.sndBallShot.play()
                            
                                
                        
                    # Enemy/Player Collisions
                    if i.colliderect(self.P1) and i._type != 4 and i._type != 6: # Wall enemies and the boss themselves cannot hurt player
                        # Player death animation
                        self.state = 'Lose'
                        hitEn = i
                        secFrac = 0
                        self.enList = [i]
                        self.enSurfList = [self.enSurfList[indexI]]
                        spawningList = []
                        self.shotList = []
                        mixer.music.stop()
                        mixer.music.load(os.path.join('data','mscLose.mp3'))
                        mixer.music.play()
                        break
                    # Enemy/Sword collisions    
                    try:
                        if i.colliderect(self.swords[0]):
                            i._hp -= 1
                            self.swords = []
                            if i._hp == 0:
                                if i._type < 6:
                                    self.scoreTot += i._type * 10
                                self.enList.pop(indexI)
                                self.enSurfList.pop(indexI)
                                self.sndEnDie.play()
                                rectangleUpdate.append(Rect(i[0]-20,i[1]-20,i[2]+40,i[3]+40)) #Approx area around enemy to be updated
                                
                                if i._type == 6:
                                    self.state = 'Win'
                                    secFrac = 0
                                    self.enList=[]
                                    self.enSurfList=[]
                                    self.sndEnDie.play(3)
                                    mixer.music.load(os.path.join('data','mscWin.mp3'))
                                    mixer.music.play(2)
                                    break
                    except:
                        ''
                    
                    indexI += 1
                # Shot-Ball/Player Collisions
                for i in self.shotList:
                    if i.colliderect(self.P1):
                        self.state = 'Lose'
                        hitEn = i
                        secFrac = 0
                        self.shotList = [i]
                        self.enList = []
                        self.enSurfList = []
                        spawningList = []
                        mixer.music.stop()
                        mixer.music.load(os.path.join('data','mscLose.mp3'))
                        mixer.music.play()
                        
                        break
                    if i[0] > 500 or i[0] < - 40 or i[1] > 650:
                        self.shotList.remove(i)
                        
                #Enemy spawning (completes this every second)
                secFrac += 1
                if secFrac == 50:
                    secFrac = 0
                    for j in 'ABCDEFGHIJ':
                        if j in self.level.enGen:
                            if self.level.enGenCount[j][0] > 0:
                                self.level.enGenCount[j][0] -= 1
                            else:
                                if self.level.enGenCount[j][1] > 0:
                                    self.level.enGenCount[j][1] -= 1
                                    if self.level.enGenCount[j][1] == 0 and self.level.enGenDict[j][3][self.level.enGenCount[j][4]] != 0:
                                        spawningList.append(j)
                                        self.sndSpawn.play()
                                else:
                                    if self.level.makeEn(j, self) == 1:
                                        spawningList.remove(j)
                    self.level._time -= 1
                    
                
            #########################################################
            #
            #       Beginning a Level in Main Loop
            #
            ##########################################################
            elif self.state == 'Begin':
                secFrac += 1
                self.surface1.blit(self.background, (0, 0))
                if secFrac < 40:
                    self.levelText = self.fontDisp.render('Level '+str(self.curLevel), True, (0, 255, 255))
                    center = (self.width - self.levelText.get_size()[0])/2
                    speed = center/40 # Divisor is secFrac to complete in
                    self.surface1.blit(self.levelText, (speed*secFrac, 200))
                elif secFrac >= 40 and secFrac < 90:
                    self.surface1.blit(self.levelText, (speed * 39, 200))
                elif secFrac >= 90 and secFrac < 130:
                    self.surface1.blit(self.levelText, (speed*(secFrac - 50), 200))
                elif secFrac == 130:
                    self.state = 'Play'
                    secFrac = 0
                    event.clear()
                    self.flipDisp = True
                self.updateSideBar(secFrac) 
                display.flip()
            #############################################################
            #
            #       On Dying in Main Loop
            #
            #############################################################
            elif self.state == 'Lose':
                secFrac += 1
                if secFrac == 100:
                    self.livesCur -= 1
                    if self.livesCur == 0:
                        gameover = Cutscene(self.surface1, 'Z')
                        gameover.main()
                        exe = 0
                    else:
                        secFrac = 0
                        self.initLevel(self.curLevel)
            #############################################################
            #
            #       Winning in main loop
            #
            #############################################################
            elif self.state == 'Win':
                secFrac += 1
                if secFrac == 100:
                    self.curLevel += 1
                    secFrac = 0
                    if self.curLevel == 2 or self.curLevel == 3 or self.curLevel == 4: 
                        self.initLevel(self.curLevel)
                        
                    elif self.curLevel == 5:
                        gocutscene = Cutscene(self.surface1,'C')
                        gocutscene.main()
                        exe = 0
                        break
                
            #############################################################
            #
            #       Updating Display
            #
            #############################################################
            if self.state == 'Win' or self.state == 'Play' or self.state == 'Lose':
                # Drawing:
                self.surface1.blit(self.background, (0,0))
                indexI =0
                for i in self.level.blockRect:
                    if i._type == 1:
                        self.surface1.blit(self.level.blockSurf[indexI], i)
                    elif i._type == 2:
                        self.surface1.blit(self.b2surf, i)
                    indexI += 1
                if self.curLevel != 4:
                    self.surface1.blit(self.levelEndSurf, self.level.WinRect)
                indexI = 0
                for i in self.enList:
                    rectangleUpdate.append(Rect(i[0]-18,i[1]-28,i[2]+36,i[3]+46)) #Approx area around enemy to be updated
                    self.surface1.blit(self.enSurfList[indexI], i)
                    indexI += 1
                self.hopeSurf = image.load(os.path.join('data','hope'+str(hopeloop/4)+'.png')).convert()
                self.hopeSurf.set_colorkey((255,255,255))
                for i in self.level.hopes:
                    self.surface1.blit(self.hopeSurf, (i[0], i[1]))
                    rectangleUpdate.append(i)
                hopeloop += 1
                if hopeloop == 16:
                    hopeloop = 0
                for i in self.shotList:
                    if i.move(self.diffCur) == 0:
                        self.surface1.blit(self.shotSurf, i)
                    else:
                        self.surface1.blit(self.ballSurf, i)
                    rectangleUpdate.append(Rect(i[0]-8,i[1]-35,i[2]+16,i[3]+50))
                if secFrac % 10 == 0 and self.state == 'Play':
                    self.spawnSurf = image.load(os.path.join('data','spawn'+str(secFrac/10)+'.png')).convert()
                    self.spawnSurf.set_colorkey((255,255,255))
                for i in spawningList:
                    position = self.level.getSpawnPos(i)
                    self.surface1.blit(self.spawnSurf, position)
                    rectangleUpdate.append(Rect(position, (30, 30)))
                if self.curLevel == 4 and len(self.enList) != 0:
                    if self.enList[0]._type == 6:
                        for i in self.enList[0]._spawnList:
                            self.surface1.blit(self.spawnSurf, i)
                            rectangleUpdate.append(Rect(i, (30, 30)))
                # Player drawing
                rectangleUpdate.append(Rect(self.P1[0]-20, self.P1[1]-40, self.P1[2]+40, self.P1[3]+80)) # Add the approximate area around the Player to be updated
                direct = self.P1._dir+1 # The direction for the image filenames
                if self.state == 'Play':
                    if self.P1._swordframe != 0:
                        self.p1surf = image.load(os.path.join('data','P'+str(direct)+'A'+ str((self.P1._swordframe+1)/2) + '.png')).convert()
                    else:
                        self.p1surf = image.load(os.path.join('data','P'+str(direct)+'.png')).convert()
                elif self.state == 'Lose': # Load losing animation
                    if secFrac >= 40 and secFrac < 90:
                        animationS = secFrac - 40
                    elif secFrac >= 90:
                        animationS = 49
                    else:
                        animationS = secFrac
                    self.p1surf = image.load(os.path.join('data','P'+str(direct)+'L'+str(animationS/10)+'.png')).convert()
                elif self.state == 'Win': # Load winning animation
                    animationS = secFrac
                    if secFrac >= 50:
                        animationS = 49
                    self.p1surf = image.load(os.path.join('data','PW'+str(animationS/10)+'.png')).convert()
                self.p1surf.set_colorkey((255,255,255))
                self.surface1.blit(self.p1surf,(self.P1.left - 10, self.P1.top - 14))#Rect is 10 x 16
                # Information drawing
                rectangleUpdate += self.updateSideBar(secFrac)
                # Display Updates
                if self.flipDisp == True:
                    display.flip()
                    self.flipDisp = False
                    if self.curLevel == 4 and self.state == 'Play':
                        bossintro = Cutscene(self.surface1, 'B')
                        bossintro.main()
                        self.surface1.blit(self.background,(0,0))
                        indexI = 0
                        for i in self.level.blockRect:
                            if i._type == 1:
                                self.surface1.blit(self.level.blockSurf[indexI], i)
                            elif i._type == 2:
                                self.surface1.blit(self.b2surf, i)
                            indexI += 1
                        display.flip()
                else:
                    display.update(rectangleUpdate)
            time.delay(20) # time.delay(20) for 50 frames per second

class Player(Rect):
    """A Rect representing the player character. Handles input procedures"""
    def __init__(self, gravity, jumpstrength, walkspeed, swordtime, xint, yint, width, height):
        Rect.__init__(self, xint, yint, width, height)
        self._gravity = gravity
        self._jumpstrength = jumpstrength
        self._walkspeed = walkspeed
        self._swordtime = swordtime
        self._x = xint
        self._y = yint
        self._canmove = 1
        self._dir = 1
        self._swordframe = 0
        self._vspeed = 0
        self._hspeed = 0

    def moveleft(self):
        """Move left if possible"""
        if self._canmove == 1 and self._swordframe == 0:
            self.move_ip(-self._walkspeed, 0)
            self._x -= self._walkspeed
            self._dir = 0
        elif self._canmove == 0 and self._swordframe ==0:
            self._dir = 0

    def moveright(self):
        """Move right if possible"""
        if self._canmove == 1 and self._swordframe == 0:
            self.move_ip(self._walkspeed, 0)
            self._x += self._walkspeed
            self._dir = 1
        elif self._canmove == 0 and self._swordframe ==0:
            self._dir = 1

    def jump(self, key):
        """Jump if possible. Input is a tuple of boolean ints giving information on whether to do a straight or long jump.
        Returns 1 if jump successful
        ((int,int)) -> int"""
        if self._canmove == 1 and self._swordframe == 0:
            if key[0] == 1 or key[1] == 1:
                if self._dir==1:
                    self._hspeed = self._walkspeed
                else:
                    self._hspeed = -self._walkspeed
            self._vspeed = -self._jumpstrength
            self._canmove = 0
            return 1
        else:
            return 0

    def attack(self, master):
        """Swing the Sword. Input is the master (containg a swords list).
        Return 1 if sword Rect created
        attack(Game) -> int"""
        if self._swordframe == 0:
            self._swordframe = self._swordtime
            if self._dir == 0:
                master.swords.append(Sword(self[0]-21, self[1]+5, self._swordtime*2/3))
            else:
                master.swords.append(Sword(self[0]-2, self[1]+5, self._swordtime*2/3))
            return 1
        else:
            return 0
            
class Sword(Rect):
    """Rect representing sword with a custom counter"""
    def __init__(self, xint, yint, swordtime):
        Rect.__init__(self,xint,yint, 39, 9)
        self._swordframe = swordtime

        
class Enemy(Rect):
    """Rect representing enemy. Contains functions for movement but decision making in main loop"""
    def __init__(self, xint, yint, typeA):
        # Here all enemies are same size except the boss
        if typeA != 6:
            Rect.__init__(self, xint, yint, 24, 24)
        else:
            Rect.__init__(self, xint, yint, 30, 30)
        self._type = typeA # Integer to represent 
        self._count = 0
        self._action = 0 # Actions for each enemy represented by integers ranging from 0 to a variable end
        self._hp = 1
        self._var = random.randint(0, 1) # Varient of the type
        self._vspeed = 0
        self._hspeed = 0
        self._yint = yint
        self._1 = 0 # Variable for general purposes
        if self._type == 4: # For type 4, var means on left or right side of screen
            if xint < 250:
                self._var = 0
            else:
                self._var = 1
            self._shot = False
        if self._type == 5: # Type 5 have 3 hp instead of 1
            self._hp = 3
        if self._type == 6: # Type 6 (boss) has 12 HP
            self._hp = 12
            self._2 = 0
            self._spawnList = [] # Similar to the levels spawn dictionaries only speacialised for the boss
    def moveleft(self, speed):
        """Move enemy left a given pixel length
        moveleft(int) -> None"""
        self.move_ip(-speed, 0)
    def moveright(self, speed):
        """Move enemy right a given pixel length
        moveright(int) -> None"""
        self.move_ip(speed, 0)
    def movedown(self, speed):
        """Move enemy down a given pixel length
        movedown(int) -> None"""
        self.move_ip(0, speed)
    def moveup(self, speed):
        """Move enemy up a given pixel length
        moveup(int) -> None"""
        self.move_ip(0, -speed)
    def movetowards(self, position, speed):
        """Move enemy towards a given number of pixels towards a given position
        movetowards(Rect or Tuple, int) -> None"""
        # position can be tuple or rect
        diffX = position[0] - self[0] + self[2]/2
        diffY = position[1] - self[1] + self[3]/2
        if diffX != 0 and diffY != 0:
            angle = math.atan(float(diffY)/float(diffX))
            movX = speed*math.cos(angle)
            movY = speed*math.sin(angle)
            if diffX > 0:
                self.move_ip(movX, movY)
            else:
                self.move_ip(-movX, -movY)
        elif diffX == 0 and diffY == 0:
            ''
        elif diffX == 0:
            self.move_ip(0, diffY/math.fabs(diffY)*speed)
        else:
            self.move_ip(diffX/math.fabs(diffX)*speed, 0)
       
class Shot(Rect):
    """Rect representing horizontally travelling bullets"""
    def __init__(self, ypos, varient):
        self._var = varient
        self._yPos = ypos
        if varient == 0:
            xpos = -30
        else:
            xpos = 400
        Rect.__init__(self, xpos, ypos, 30, 10)
    def move(self, diffCur):
        """Move Shot based on difficulty
        move(int) -> None"""
        if self._var == 1:
            self.move_ip(-5 - diffCur, 0)
        else:
            self.move_ip(5 + diffCur, 0)
        return 0 # The returning of 0 identifies this as a Shot rather than a Ball
    
class Ball(Rect):
    """Rect representing gravity effected bullets
    Ball(Rect or Tuple)"""
    def __init__(self, initpos):
        Rect.__init__(self, initpos[0], initpos[1], 24, 24)
        self._hspeed = random.randint(-8, 8)
        self._vspeed = random.randint(-16, -8)
        self._hsDown = 3
    def move(self, __):
        """Move Ball
        Ball.move() -> None"""
        self._vspeed += 1
        self._hsDown -= 1
        if self._hsDown == 0:
            self._hsDown = 3
            if self._hspeed > 0:
                self._hspeed -= 1
            elif self._hspeed < 0:
                self._hspeed += 1
            else:
                ''
        self.move_ip(self._hspeed, self._vspeed)
        return 1 # The returning of 1 identifies this as a Ball rather than a Shot

class Level:
    """Class to control level properties such as enemy generation
    Level([[int/str,....],....], [{[int, int, bool, [int,...],.....}....], int, int, int)"""
    def __init__(self, layout, enGenDict, tint, width, height):
        self._layout = layout
        self.enGenDict = enGenDict
        self.enGenCount = copy.deepcopy(enGenDict)
        for i in self.enGenCount:
            self.enGenCount[i].append(0)
        self._time = tint
        self.width = width
        self.height = height
        self.tilesX = len(layout[0])
        self.deltaX = self.width/self.tilesX
        self.tilesY = len(layout)
        self.deltaY = self.height/self.tilesY
        self.block = [] #contains array of all blocks
        self.blockRect = [] #contains list of all blocks that are rect objects
        self.blockSurf = [] #contains the surfaces for all blocks
        self.enemy = [] # Not used
        self.enGen = '' # Contains letters of currently active enemy generators
        self.enGenPos = [] # Contains positions of the corresponding generators in self.enGen
        self.hopes = [] # Contains list of hopes
        
    def drawLevel(self):
        """Parse the given layout (in __init__) and create the level Rects"""
        indexI = 0
        indexJ = 0
        for i in self._layout:
            templist = []
            for j in i:
                if j==0:
                    templist.append(0)
                elif j < 3 and j > 0:
                    tempblock = Block(indexJ*self.deltaX,indexI*self.deltaY,self.deltaX,self.deltaY,j)
                    templist.append(tempblock)
                    self.blockRect.append(tempblock)
                elif j == 3:
                     self.hopes.append(Hope(indexJ*self.deltaX+self.deltaX/2 - 15, indexI*self.deltaY + self.deltaY - 30))
                elif j in 'ABCDEFGHIJ':
                    self.enGen = self.enGen + j
                    self.enGenPos.append([indexJ*self.deltaX,indexI*self.deltaY])
                elif j == 'X':
                    self.P1XPos = indexJ
                    self.P1YPos = indexI
                elif j == 'Z':
                    self.WinRect = (indexJ*self.deltaX+self.deltaX/2 - 15, indexI*self.deltaY + self.deltaY - 30, 30, 30)
                indexJ += 1
            indexJ = 0
            indexI += 1
            self.block.append(templist)
        

    def getInitX(self):
        """ Assume drawLevel() is already called and there was an X in levelArray"""
        return (self.P1XPos + 0.5)* self.deltaX
    def getInitY(self):
        """Return the Y position for the player to start
        getInitY() -> int"""
        return (self.P1YPos + 0.5) * self.deltaY
    def getSpawnPos(self, letterstring):
        """Get position of a given enemy generator
        getSpawnPos(str) -> (int, int)"""
        index1 = self.enGen.index(letterstring)
        return self.enGenPos[index1]
    def makeEn(self, enArr, master):
        """Create the enemy from spawn point 'enArr' and place its Rect on 'master'
        Returns 0 if no enemy was create, 1 otherwise
        makeEn(str, Game) -> int"""
        removing = False
        self.enGenCount[enArr][1] = self.enGenDict[enArr][1]
        #Fourth term of enGen List countains which enemy to spawn
        spawntype = self.enGenDict[enArr][3][self.enGenCount[enArr][4]]
        self.enGenCount[enArr][4] += 1
        if self.enGenCount[enArr][4] == len(self.enGenCount[enArr][3]):
            if self.enGenCount[enArr][2] == True:
                self.enGenCount[enArr][4] = 0
            else:
                # Remove this spawn point at end of function
                removing = True
                
                
        if spawntype == 0:
            return 0
        enGenIndex = self.enGen.index(enArr)
        XInt = self.enGenPos[enGenIndex][0]
        YInt = self.enGenPos[enGenIndex][1]
        master.enList.append(Enemy(XInt, YInt, spawntype)) # Create the enemy
        if spawntype != 4 or XInt < 250:
            master.enSurfList.append(image.load(os.path.join('data','en'+str(spawntype)+'00.png')).convert()) # Filename format: en### ; 1st = type ; 2nd = action ; 3rd = frame
        else: # For a type4 enemy spawned on the right side of the screen:
            master.enSurfList.append(image.load(os.path.join('data','en'+str(spawntype)+'01.png')).convert())
        
        master.enSurfList[len(master.enSurfList)-1].set_colorkey((255,255,255))
        if removing == True: # Remove spawn point if it is no longer needed
            positionat = self.enGen.find(enArr)
            tempList = self.enGen.split(enArr)
            self.enGen = ''.join(tempList)
            self.enGenDict.pop(enArr)
            self.enGenCount.pop(enArr)
            self.enGenPos.pop(positionat)
        return 1
        
        
        
class Hope(Rect):
    """Rect representing a Hope to collect
    Hope(int, int)"""
    def __init__(self,xint,yint):
        hopewidth = 30
        hopeheight = 30
        Rect.__init__(self,xint,yint, hopewidth, hopeheight)
        

class Block(Rect):
    """Rect representing a Block. Has a type variable
    Block(int, int, int, int, int)"""
    def __init__(self,xint,yint,width,height,typeA):
        Rect.__init__(self, xint, yint, width, height)
        self._type = typeA
        self._x = xint
        self._y = yint
#############################################################
#                                                           #
#            MAIN   MENU    SECTION                         #
#                                                           #
#############################################################
class Menu():
    def __init__(self):
        self.surface1 = display.set_mode((550, 650))
        self.cursor = image.load(os.path.join('data','cursor.png'))
        self.cursor.set_colorkey((255,255,255))
        self._curPos = 0
        self.cursXpos = 125
        self._screen = 1
        self.background = image.load(os.path.join('data','MenuBG'+str(self._screen)+'.png')).convert()
        self.logo = image.load(os.path.join('data','Logo.png')).convert()
        self.logo.set_colorkey((255,255,255))
        self.logoS = image.load(os.path.join('data','LogoS0.png')).convert()
        self.logoS.set_colorkey((255,255,255))
        # Option variables:
        self.opDiff = 2
        self.opLives = 3
        self.initPos()
    def initPos(self):
        self.PS = Rect(550/2, 0, 30, 30)
        self.PSsurf = image.load(os.path.join('data','P1.png')).convert()
        self.PSsurf.set_colorkey((255,255,255))
        self.PSbub = image.load(os.path.join('data','bub1.png')).convert()
        self.PSbub.set_colorkey((0,0,255))
        self.enList = []
        self.enListS = []
        for i in range(100):
            self.enList.append(Rect(0-random.randint(24,524),random.randint(525,620),24,24))
            tempSurf = image.load(os.path.join('data','en210.png')).convert()
            tempSurf.set_colorkey((255,255,255))
            self.enListS.append(tempSurf)
        self._PSvspeed = 0
        self._PShspeed = 0
        mixer.music.load(os.path.join('data','mscMenu.mp3'))
        mixer.music.play(-1)
        self.jumpsound = mixer.Sound(os.path.join('data','sndJump.wav'))
    def main(self):
        exe = 1
        count = 0
        sec = 0
        while exe == 1:
            count += 1
            if count == 50:
                sec += 1 # After 50 frames, count another second
                count = 0
            if count % 5 == 0:
                self.logoS = image.load(os.path.join('data','LogoS'+str(count/5)+'.png')).convert()
                self.logoS.set_colorkey((255,255,255))
            # Inputs
            event1 = event.poll()
            if event1.type == KEYDOWN:
                if event1.key == K_DOWN:
                    if self._curPos == 3:
                        self._curPos = 0
                    else:
                        self._curPos += 1
                elif event1.key == K_UP:
                    if self._curPos == 0:
                        self._curPos = 3
                    else:
                        self._curPos -= 1
                elif event1.key == K_z:
                    if self._screen == 1:
                        if self._curPos == 0:
                            # Begin game
                            mixer.music.load(os.path.join('data','mscCutA.mp3'))
                            mixer.music.play(-1)
                            mycutscene1 = Cutscene(self.surface1, 'A')
                            mycutscene1.main()
                            mygame1 = Game(levelAr, self.opDiff, self.opLives)
                            mygame1.main()
                            count = 0
                            sec = 0
                            self.initPos()
                            mixer.music.load(os.path.join('data','mscMenu.mp3'))
                            mixer.music.play(-1)
                        elif self._curPos == 1:
                            # Go to options
                            self._screen = 2
                        elif self._curPos == 2:
                            # instructions
                            self._screen = 3
                        else:
                            exe = 0
                    elif self._screen == 2:
                        # Set the difficulty
                        self.opDiff = self._curPos + 1
                        self._screen = 1
                        count = 0
                        sec = 0
                        self.initPos()
                    else:
                        # Return to main screen
                        self._screen = 1
                        count = 0
                        sec = 0
                        self.initPos()
                    self.background = image.load(os.path.join('data','MenuBG'+str(self._screen)+'.png')).convert()
                elif event1.key == K_x:
                    if self._screen == 1:
                        self._curPos = 3
                    else:
                        self._screen = 1
                        count = 0
                        sec = 0
                        self.initPos()
                    self.background = image.load(os.path.join('data','MenuBG'+str(self._screen)+'.png')).convert()
                elif event1.key == K_ESCAPE:
                    exe = 0
            elif event1.type == QUIT:
                exe = 0
            # Animations:
            if self.PS[1] < 590:
                self._PSvspeed += 1
                
            else:
                self._PSvspeed = 0
            if sec >= 2 and sec < 5:
                if count == 25:
                    self.PSsurf = image.load(os.path.join('data','P1.png')).convert()
                    self.PSsurf.set_colorkey((255,255,255))
                elif count == 1:
                    self.PSsurf = image.load(os.path.join('data','P2.png')).convert()
                    self.PSsurf.set_colorkey((255,255,255))
            if sec == 5:
                if count == 3:
                    self._PShspeed = 0
                elif count > 3 and count < 6:
                    self._PShspeed -= 1
            if self.PS[0] < self.cursXpos and sec < 17:
                self.PS.move_ip(-self._PShspeed, 0)
                self._PShspeed = 0
                self.PSsurf = image.load(os.path.join('data','P2.png')).convert()
                self.PSsurf.set_colorkey((255,255,255))
            if sec >= 7 and sec < 12 and self.PS[1] >= 590:
                self._PSvspeed = -8
                self.jumpsound.play()
            if sec == 13:
                self.PSsurf = image.load(os.path.join('data','P1.png')).convert()
                self.PSsurf.set_colorkey((255,255,255))
            if sec >= 13 and sec < 15:
                if count == 25:
                    self.PSbub = image.load(os.path.join('data','bub1.png')).convert()
                    self.PSbub.set_colorkey((0,0,255))
                elif count == 1:
                    self.PSbub = image.load(os.path.join('data','bub2.png')).convert()
                    self.PSbub.set_colorkey((0,0,255))
            if sec == 17 and count >= 3 and count < 10:
                self._PShspeed -= 1
            if sec >= 17 and self.PS[0] + self.PS[2] < 0:
                self._PShspeed = 0
            if sec == 18 and count >=4 and count < 30 and count%2 == 0:
                self._PShspeed += 1
            if sec == 18:
                if count == 25:
                    self._PShspeed = 0
                elif count == 48:
                    self.PSsurf = image.load(os.path.join('data','P2.png')).convert()
                    self.PSsurf.set_colorkey((255,255,255))
            if sec == 19 and count >=3 and count < 30 and count%2 == 0:
                self._PShspeed += 1
            if sec >= 19 and sec <= 23:
                for i in self.enList:
                    i.move_ip(6, 0)
            if sec == 25:
                self.initPos()
                sec = 0
            self.PS.move_ip(self._PShspeed, self._PSvspeed)        
            # Drawing
            self.surface1.blit(self.background, (0,0))
            if self._screen != 3:
                self.surface1.blit(self.cursor, (self.cursXpos, 400+self._curPos*50))
                if self._screen == 1:
                    self.surface1.blit(self.logo, (90,60))
                    self.surface1.blit(self.logoS, (90,60))
                    self.surface1.blit(self.PSsurf, self.PS)
                    if sec >= 13 and sec < 15:
                        self.surface1.blit(self.PSbub, (125,550))
                    if sec >=19 and sec <=23:
                        indexI = 0
                        for i in self.enList:
                            self.surface1.blit(self.enListS[indexI],i)
                            indexI += 1
            display.flip()
            time.delay(20)

class Cutscene():
    """Draws on top of Game or Main. Freezes underneath action. May take up full screen if there are images to support it"""
    def __init__(self, masterdisplay, cutletter):
        self.disp = masterdisplay
        self.cutletter = cutletter
        try:
            self.bg = image.load(os.path.join('data','cut'+str(self.cutletter)+'0.png')).convert()
            self.bg.set_alpha(60)
            self.loaded = True
        except:
            self.loaded = False
        # Create the self.linelist list which contains all the seperate lines to display
        fileobj = open(os.path.join('data','text'+str(self.cutletter)+'.txt'), 'r')
        string1 = fileobj.read()
        self.pagelist = string1.split('<P>')
        self.linelist = []
        for i in self.pagelist:
            self.linelist.append(i.split('\n'))
        self.sceneTot = len(self.linelist)
        self.font1 = font.Font(os.path.join('data','DejaVuSerif.ttf'), 15)
        self.textSurfList = []
        for i in self.linelist[0]:
            self.textSurfList.append(self.font1.render(i, False, (0, 0, 0)))
        self.textBox = Surface((375, 200))
        self.textBox.fill((255,255,255))
        self.textBox.set_alpha(30) 
    def main(self):
        exe = 1
        scene = 0
        while exe == 1:
            
            # Inputs
            eve1 = event.poll()
            if eve1.type == KEYDOWN:
                if eve1.key == K_z:
                    self.textSurfList = []
                    scene += 1
                    if scene == self.sceneTot:
                        
                        exe = 0
                    else:
                        if self.loaded:
                            try:
                                self.bg = image.load(os.path.join('data','cut'+str(self.cutletter)+str(scene)+'.png')).convert()
                                self.bg.set_alpha(60)
                            except:
                                ''
                        for i in self.linelist[scene]:
                            self.textSurfList.append(self.font1.render(i, True, (0, 0, 0)))
                if eve1.key == K_ESCAPE:
                     exe = 0
                    
            # Drawing
            if self.loaded:
                self.disp.blit(self.bg, (0,0))
            self.disp.blit(self.textBox, (30, 425))
            indexI = 0
            for i in self.textSurfList:
                self.disp.blit(i, (35, 430 + 20*indexI))
                indexI += 1
            display.flip()
            time.delay(40)

#init pygame here
init()
mymenu1 = Menu()
mymenu1.main()

quit()
