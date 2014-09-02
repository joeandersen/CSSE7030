import math
epsilon = 0.000001

class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def dist_to_point(self,p):
        x1 = self._x
        y1 = self._y
        x2 = p._x
        y2 = p._y
        distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return distance

    def is_near(self,p):
        foo =  self.dist_to_point(p) < epsilon
        return foo

    def add_point(self,p):
        x1 = int(self._x)
        y1 = int(self._y)
        x2 = int(p._x)
        y2 = int(p._y)
        #print x1,y1,x2,y2
        self._x = x1+x2
        self._y = y1+y2
        #print repr(self)
        #return foo
    
            
    
        
