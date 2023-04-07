import numpy as np
from model.Body import Body
from random import randint
from controller.Utilities import Utilities
            
from model.GlobVar import GlobVar

class MoreBodiesSimulation():

    #If you specify bodies and a bodyCount, it will be taken into account if bodyCount is higher than the number of bodies in bodies
    #If so, the constructor will add random bodies to your initial bodies list to match bodyCount
    def __init__(self,bodyCount=3, mass_min=6, mass_max=12, width=None, height=None,bodies=[]):
        """         
         
         @param bodyCount - The number of bodies to create
         @param mass_min - The minimum mass of the bodies in kilograms
         @param mass_max - The maximum mass of the bodies in kilograms
         @param width - The width of the body in km / s
         @param height - The height of the body in km / s
         @param bodies - A list of Body objects that will be
        """
        self.bodyCount = bodyCount if len(bodies) < bodyCount else len(bodies)
        self.bodies = bodies

        # Add a random body to the body list.
        for _ in range(bodyCount-len(bodies)):
            random_exp = randint(mass_min, mass_max)
            random_float = float(randint(1,9))
            random_mass = float(random_float*10**random_exp)
            self.bodies.append(Body(randint(20,width-20),randint(20,height-20), random_mass))
        
        self.nbInteract = 0

    
    def advance(self):
        """
         Advance the physics simulation by computing forces and updating the speed of both bodies. This is called by the simulator
        """
        self.nbInteract = 0
        
        # compute all forces for each body
        for body in self.bodies:
            self.computeAllForces(body)

        #Update the speed of both bodies and get their position accordingly
        # Compute new position of all bodies in the list of bodies.
        for body in self.bodies:
            body.computeNewPos()
    
    def computeAllForces(self,body):
        """
         Compute forces of a body
         
         @param body - Body to compute forces
        """
        body.acc = 0
        # Add force de body to the body
        for otherBody in self.bodies:
            # This function is used to add force de to the body
            if otherBody != body:
                self.nbInteract+=1
                a = otherBody.pos[0] - body.pos[0]
                b = otherBody.pos[1] - body.pos[1]
                d = np.sqrt(a**2 + b**2)

                Vdir = np.array([a,b])
                body.addForce(((GlobVar.G*body.mass*otherBody.mass)/(d**3))*Vdir)
                # print("Force de", body, "par", otherBody, "=", ((GlobVar.G*body.mass*otherBody.mass)/(d**3))*Vdir)
