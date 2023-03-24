import numpy as np

class Body():
    def __init__(self, x, y, mass=10**11):
        self.pos = np.array([float(x),float(y)])
        self.spd = np.array([0.0,0.0])
        self.acc = np.array([0.0,0.0])
        # MASSE TERRE = 5.9722*10**24
        # MASSE MINIMALE = 10**11
        self.mass = mass
        

    def addForce(self,force):
        self.acc += force/float(self.mass)

    def computeNewPos(self):
        #TODO check if accMax is good enough or if there is a way to improve it
        # accMag = np.sqrt(self.acc[0]**2 + self.acc[1]**2)
        # accMax = np.inf
        # self.acc = self.acc if accMag < accMax else self.acc/accMag * np.array([accMax,accMax])
        #Add acceleration to speed
        self.spd += self.acc

        #Add speed to position
        self.pos += self.spd

    def __str__(self):
        return "Body : x =  " + str(self.pos[0]) + ", y = " + str(self.pos[1])
    
    #!! Disgusting function ...
    def getBodyColor(self,size):
        if size >= 1 and size < 4:
            return '#000000'
        elif size >= 4 and size < 7:
            return '#999999'
        elif size == 7:
            return '#FFD02D'
        elif size > 7 and size < 10:
            return '#FF9900'
        elif size == 10:
            return '#FF0000'
