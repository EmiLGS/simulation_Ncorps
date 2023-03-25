import numpy as np
from model.Body import Body
from random import randint
from controller.Utilities import Utilities
            
from model.GlobVar import GlobVar

class MoreBodiesSimulation():

    #If you specify bodies and a bodyCount, it will be taken into account if bodyCount is higher than the number of bodies in bodies
    #If so, the constructor will add random bodies to your initial bodies list to match bodyCount
    def __init__(self,bodyCount=3, mass_min=(5.9722*10**6), mass_max=(5.9722*10**12), width=None, height=None,bodies=[]):
        self.bodyCount = bodyCount if len(bodies) < bodyCount else len(bodies)
        self.bodies = bodies

        mass_min = Utilities().bodyMassExp(mass_min)
        mass_max = Utilities().bodyMassExp(mass_max)

        for _ in range(bodyCount-len(bodies)):
            random_exp = randint(mass_min, mass_max)
            random_float = float(randint(1,9))
            random_mass = float(random_float*10**random_exp)
            self.bodies.append(Body(randint(20,width-20),randint(20,height-20), random_mass))

    
    def advance(self):

        for body in self.bodies:
            self.computeAllForces(body)

        #Update the speed of both bodies and get their position accordingly
        for body in self.bodies:
            body.computeNewPos()
    
    def computeAllForces(self,body):
        body.acc = 0
        for otherBody in self.bodies:
            if otherBody != body:
                a = otherBody.pos[0] - body.pos[0]
                b = otherBody.pos[1] - body.pos[1]
                d = np.sqrt(a**2 + b**2)

                Vdir = np.array([a,b])
                body.addForce(((GlobVar.G*body.mass*otherBody.mass)/(d**3))*Vdir)
                # print("Force de", body, "par", otherBody, "=", ((GlobVar.G*body.mass*otherBody.mass)/(d**3))*Vdir)
