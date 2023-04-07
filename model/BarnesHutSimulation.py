from controller.Utilities import Utilities
from model.Body import Body
from random import randint
from model.QuadTreeBarnesHut import QuadTree
import numpy as np

class BarnesHutSimulation():

    #If you specify bodies and a bodyCount, it will be taken into account if bodyCount is higher than the number of bodies in bodies
    #If so, the constructor will add random bodies to your initial bodies list to match bodyCount
    def __init__(self,bodyCount=0, mass_min=6,mass_max=12, width=None, height=None, precision=1, bodies=[]):
        """
         Initializes the quadtree with randomly generated masses. It is recommended to use this constructor when you want to create a quadtree with a large number of bodies.
         
         @param bodyCount - The number of bodies to generate. Default is 0.
         @param mass_min - The minimum mass of the bodies. Default is 6.
         @param mass_max - The maximum mass of the bodies. Default is 12.
         @param width - The width of the window. Default is None.
         @param height - The height of the window. Default is None.
         @param precision - The number of decimal places to use for floating point numbers. Default is 1.
         @param bodies - A list of Body objects that will be used to generate the quadtree
        """
        self.precision = precision
        self.quadTreeWidth = max(width,height)
        self.bodies = bodies
        self.bodyCount = bodyCount if bodyCount > len(bodies) else len(bodies)

        # Add a random body to the body list.
        for _ in range(bodyCount-len(bodies)):
            random_exp = randint(mass_min, mass_max)
            random_float = float(randint(1,9))
            random_mass = float(random_float*10**random_exp)
            self.bodies.append(Body(randint(20,width-20),randint(20,height-20), random_mass))
        # print(*bodies)
        self.nbInteract = 0

    def advance(self):
        """
         Advance the physics simulation by computing the quadtree and updating the speed of the bodies. This is done in two steps
        """
        
        minX, minY, maxX, maxY = np.inf,np.inf,-np.inf,-np.inf
        # Find the minimum and maximum position of all bodies in the list.
        for body in self.bodies:
            # Find the maximum position of the body
            if body.pos[0] > maxX:
                maxX = body.pos[0]
            # Get the maximum position of the body
            if body.pos[1] > maxY:
                maxY = body.pos[1]
            # Find the minimum position of the body
            if body.pos[0] < minX:
                minX = body.pos[0]
            # Find the minimum position of the body
            if body.pos[1] < minY:
                minY = body.pos[1]

        quadWidth = max(maxY - minY, maxX - minX)

        quadtree = QuadTree(quadWidth,-minX,-minY, self.bodies)

        # print("\n")

        quadtree.computeMasses()

        # Computes the force of all the quadtree bodies.
        for body in self.bodies:
            body.acc = 0
            force = quadtree.computeForce(body,self.precision)  
            body.addForce(force)
            
        #Update the speed of both bodies and get their position accordingly
        # Compute new position of all bodies in the list of bodies.
        for body in self.bodies:
            body.computeNewPos()
        
        self.nbInteract = QuadTree.nbInteract

