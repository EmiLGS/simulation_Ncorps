import numpy as np
from model.Body import Body
from model.GlobVar import GlobVar

class ThreeBodiesSimulation():

    def __init__(self,body1=None,body2=None,body3=None):
        self.body1 = body1 if body1 else Body(400,400)
        self.body2 = body2 if body2 else Body(200,200)
        self.body3 = body3 if body3 else Body(600,500)
        self.bodies = [body1,body2,body3]


    def advance(self):

        self.computeAllForces(self.body1,[self.body2,self.body3])
        self.computeAllForces(self.body2,[self.body1,self.body3])
        self.computeAllForces(self.body3,[self.body1,self.body2])

        #Update the speed of both bodies and get their position accordingly
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
            body.addForce(((GlobVar.G*body.mass*targetBody.mass)/(d**3))*Vdir)
