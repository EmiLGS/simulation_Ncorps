from model.Body import Body
from random import randint
from model.QuadTreeBarnesHut import QuadTree
import numpy as np

class BarnesHutSimulation():

    #If you specify bodies and a bodyCount, it will be taken into account if bodyCount is higher than the number of bodies in bodies
    #If so, the constructor will add random bodies to your initial bodies list to match bodyCount
    def __init__(self,bodyCount=0, mass=(5.9722*10**11), width=None, height=None, precision=1, bodies=[]):
        self.precision = precision
        self.quadTreeWidth = max(width,height)
        self.bodies = bodies
        self.bodyCount = bodyCount if bodyCount > len(bodies) else len(bodies)
        for _ in range(bodyCount-len(bodies)):
            self.bodies.append(Body(randint(20,width-20),randint(20,height-20),mass))
        print(*bodies)

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

        print("\n")

        quadtree.computeMasses()

        for body in self.bodies:
            body.acc = 0
            force = quadtree.computeForce(body,self.precision)  
            body.addForce(force)
            
        #Update the speed of both bodies and get their position accordingly
        for body in self.bodies:
            body.computeNewPos()
