import numpy as np
from model.Body import Body
from model.GlobVar import GlobVar

class TwoBodiesSimulation():

    def __init__(self,body1=None,body2=None):
        """
         Initialize the object with two bodies. This is the method to be called by the constructor. It sets the mass and position of the bodies
         
         @param body1 - The first body to be used in the calculation. If not specified a 400x400 body will be created.
         @param body2 - The second body to be used in the calculation. If not specified a 200x400 body will be created
        """
        self.body1 = body1 if body1 else Body(400,400)
        self.body2 = body2 if body2 else Body(200,400)
        self.bodies = [body1,body2]
        self.body1.mass = 10*10**11
        self.body2.mass = 1
        dist = np.sqrt((self.body1.pos[0] - self.body2.pos[0])**2 + (self.body1.pos[1] - self.body2.pos[1]))
        vitin = np.sqrt(GlobVar.G*self.body1.mass/(dist))
        self.body2.spd = np.array([0.0,vitin])

    def getFirstBody(self):
        """
         Returns the first body of the body chain. This is used to determine the position of the body's first element in the chain.
         
         
         @return the first body of the body chain or None if there is no body chain at the point of view
        """
        return self.body1

    def getSecondBody(self):
        """
         Get the second body of this message. This is the body that is used to send the message to the client when it is sent to the server.
         
         
         @return a L { twisted. internet. defer. Deferred } which fires with the body as its sole argument
        """
        return self.body2

    def advance(self):
        """
         Advance the position of the bodies by the force defined in GlobVar. G and the velocity of the
        """
        #Get distance between 2 bodies
        a = self.body2.pos[0] - self.body1.pos[0]
        b = self.body2.pos[1] - self.body1.pos[1]
        d = np.sqrt(a**2 + b**2)

        V12 = np.array([a,b])
        force = ((GlobVar.G*self.body1.mass*self.body2.mass)/(d**3))*V12

        self.body1.acc = np.array([0.0,0.0])
        self.body2.acc = np.array([0.0,0.0])
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