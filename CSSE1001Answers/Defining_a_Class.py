class Rectangle(object):
    def __init__(self,top_left,width,height):
        self.top_left = top_left
        self.width = width
        self.height = height

    def get_bottom_right(self):
        (x,y) = self.top_left
        x = x+self.width
        y = y+self.height
        return (x,y)

    def move(self,p):
        self.top_left = p

    def resize(self,width,height):
        self.width = width
        self.height = height

    def __str__(self):
        br = self.get_bottom_right()
        tl = self.top_left
        foo = '('+str(tl)+', '+str(br)+')'
        return foo 
    
