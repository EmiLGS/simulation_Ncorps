import numpy as np

class Body():
    def __init__(self,x,y):
        self.pos = np.array([x+0.1,y+0.1])
        self.spd = np.array([0.0,0.0])
        self.acc = np.array([0.0,0.0])
        self.mass = 10

    def addForce(self,force):
        self.acc = force

    def computeNewPos(self):

        #Add acceleration to speed
        self.spd += self.acc

        #Add speed to position
        self.pos += self.spd