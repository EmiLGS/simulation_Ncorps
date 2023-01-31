import numpy as np

class Body():
    def __init__(self,x,y):
        self.pos = np.array([x+0.1,y+0.1])
        self.spd = np.array([0.0,0.0])
        self.acc = np.array([0.0,0.0])
        # MASSE TERRE
        self.mass =  5.9722*10**24 # 10**11

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