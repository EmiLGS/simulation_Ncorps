from controller.Utilities import Utilities
from model.Body import Body
from random import randint
from model.QuadTreeBarnesHut import QuadTree
import numpy as np

class BarnesHutSimulation():

    #If you specify bodies and a bodyCount, it will be taken into account if bodyCount is higher than the number of bodies in bodies
    #If so, the constructor will add random bodies to your initial bodies list to match bodyCount
    def __init__(self,bodyCount=0, mass_min=(5.9722*10**6),mass_max=(5.9722*10**12), width=None, height=None, precision=1, bodies=[]):
        self.precision = precision
        self.quadTreeWidth = max(width,height)
        self.bodies = bodies
        self.bodyCount = bodyCount if bodyCount > len(bodies) else len(bodies)
        mass_min = Utilities().bodyMassExp(mass_min)
        mass_max = Utilities().bodyMassExp(mass_max)

        for _ in range(bodyCount-len(bodies)):
            random_exp = randint(mass_min, mass_max)
            random_float = float(randint(1,9))
            random_mass = float(random_float*10**random_exp)
            self.bodies.append(Body(randint(20,width-20),randint(20,height-20), random_mass))
        # print(*bodies)

    def advance(self):
        
        minX, minY, maxX, maxY = np.inf,np.inf,-np.inf,-np.inf
        for body in self.bodies:
            if body.pos[0] > maxX:
                maxX = body.pos[0]
            if body.pos[1] > maxY:
                maxY = body.pos[1]
            if body.pos[0] < minX:
                minX = body.pos[0]
            if body.pos[1] < minY:
                minY = body.pos[1]

        quadWidth = max(maxY - minY, maxX - minX)

        quadtree = QuadTree(quadWidth,-minX,-minY, self.bodies)

        # print("\n")

        quadtree.computeMasses()

        for body in self.bodies:
            body.acc = 0
            force = quadtree.computeForce(body,self.precision)  
            body.addForce(force)
            
        #Update the speed of both bodies and get their position accordingly
        for body in self.bodies:
            body.computeNewPos()

