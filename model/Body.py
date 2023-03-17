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
        print(self.acc)
        self.spd += self.acc

        #Add speed to position
        self.pos += self.spd

    def __str__(self):
        return "Body : x = " + str(self.pos[0]) + ", y = " + str(self.pos[1])