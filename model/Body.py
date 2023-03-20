import numpy as np

class Body():
    def __init__(self, mass, x, y):
        self.pos = np.array([float(x)+0.1,float(y)+0.1])
        self.spd = np.array([0.0,0.0])
        self.acc = np.array([0.0,0.0])
        # MASSE TERRE = 5.9722*10**24
        # MASSE MINIMAL = 10**11
        self.mass = mass
        

    def addForce(self,force):
        self.acc += force/self.mass

    def computeNewPos(self):
        accMag = np.sqrt(self.acc[0]**2 + self.acc[1]**2)
        accMax = 0.1
        self.acc = self.acc if accMag < accMax else self.acc/accMag * np.array([accMax,accMax])
        #Add acceleration to speed
        self.spd += self.acc

        #Add speed to position
        self.pos += self.spd
        
    #!! Disgusting function ...
    def getBodyColor(self,size):
        if size >= 1 and size < 4:
            return '#000000'
        elif size >= 4 and size < 7:
            return '#999999'
        elif size == 7:
            return '#FFFF00'
        elif size > 7 and size < 10:
            return '#FF9900'
        elif size == 10:
            return '#FF0000'