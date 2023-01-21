import numpy as np
from model.Body import Body

class ThreeBodiesSimulation():

    G = 6.67*10**-11

    def __init__(self,body1=None,body2=None,body3=None):
        print(ThreeBodiesSimulation.G)
        self.body1 = body1 if body1 else Body(400,400)
        self.body2 = body2 if body2 else Body(200,200)
        self.body3 = body3 if body3 else Body(600,500)
        self.body1.mass = -10**9
        self.body2.mass = -10**9
        self.body3.mass = -10**9
        vitin = np.sqrt(self.G*self.body1.mass/200)
        self.body2.spd = np.array([0.0,vitin])
        self.body3.spd = np.array([0.0,-vitin])

    def advance(self):

        self.computeAllForces(self.body1,[self.body2,self.body3])
        self.computeAllForces(self.body2,[self.body1,self.body3])
        self.computeAllForces(self.body3,[self.body1,self.body2])

        #Update the speed of both bodies and get their position accordinglyswww
        self.body1.computeNewPos()
        self.body2.computeNewPos()
        self.body3.computeNewPos()
    
    def computeAllForces(self,body,targetBodies):
        body.acc = 0
        for targetBody in targetBodies:
            a = targetBody.pos[0] - body.pos[0]
            b = targetBody.pos[1] - body.pos[1]
            d = np.sqrt(a**2 + b**2)

            Vdir = np.array([a,b])
            body.addForce(((self.G*body.mass*targetBody.mass)/(d**3))*Vdir)
