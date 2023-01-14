import numpy as np
from Body import Body

class TwoBodiesSimulation():

    g = 9.81

    def __init__(self,body1=None,body2=None):
        self.body1 = body1 if body1 else Body(300,300)
        self.body2 = body2 if body2 else Body(600,200)
        self.body1.spd = np.array([0.0,1.1])
        self.body2.spd = np.array([0.0,-1.1])

    def advance(self):

        #Get distance between 2 bodies
        a = self.body2.pos[0] - self.body1.pos[0]
        b = self.body2.pos[1] - self.body1.pos[1]
        d = np.sqrt(a**2 + b**2)

        V12 = np.array([a,b])
        force = ((self.g*self.body1.mass*self.body2.mass)/(d**3))*V12

        #Apply force to both bodies
        self.body1.addForce(force)
        self.body2.addForce(-force)

        #Update the speed of both bodies and get their position accordinglyswww
        self.body1.computeNewPos()
        self.body2.computeNewPos()




        
        # #Get force and force direction between 2 bodies
        # F = self.g*self.body1.mass*self.body2.mass / d**2

        # x3 = self.body1.x + 10
        # y3 = self.body1.y

        # P12 = np.sqrt((self.body1.x - self.body2.x)**2 + (self.body1.y - self.body2.y)**2)
        # P13 = np.sqrt((self.body1.x - x3)**2 + (self.body1.y - y3)**2)
        # P23 = np.sqrt((self.body2.x - x3)**2 + (self.body2.y - y3)**2)

        # body1Fdir = np.arccos((P12**2 + P13**2 - P23**2)/(2*P12*P13))

        # body2Fdir = body1Fdir+np.pi