import numpy as np
from model.Body import Body
from model.GlobVar import GlobVar

class ThreeBodiesSimulation():

    def __init__(self,body1=None,body2=None,body3=None):
        """
         Initialize a Body object. You can pass one or three Body objects to this method. If none are provided a 400 Bad Request will be used.
         
         @param body1 - Body object to be used for the first body.
         @param body2 - Body object to be used for the second body.
         @param body3 - Body object to be used for the third body
        """
        self.body1 = body1 if body1 else Body(400,400)
        self.body2 = body2 if body2 else Body(200,200)
        self.body3 = body3 if body3 else Body(600,500)
        self.bodies = [body1,body2,body3]


    def advance(self):
        """
        Advance the speed of both bodies by one time step. This is called by the game loop every frame
        """
        
        self.computeAllForces(self.body1,[self.body2,self.body3])
        self.computeAllForces(self.body2,[self.body1,self.body3])
        self.computeAllForces(self.body3,[self.body1,self.body2])

        #Update the speed of both bodies and get their position accordingly
        self.body1.computeNewPos()
        self.body2.computeNewPos()
        self.body3.computeNewPos()
    
    def computeAllForces(self,body,targetBodies):
        """
         Compute forces between body and targetBodies. This is used to compute the mass and acc of a physics body
         
         @param body - The physics body to compute forces for
         @param targetBodies - The list of target physics bodies
        """
        body.acc = 0
        # Add force to each target body.
        for targetBody in targetBodies:
            a = targetBody.pos[0] - body.pos[0]
            b = targetBody.pos[1] - body.pos[1]
            d = np.sqrt(a**2 + b**2)

            Vdir = np.array([a,b])
            body.addForce(((GlobVar.G*body.mass*targetBody.mass)/(d**3))*Vdir)
