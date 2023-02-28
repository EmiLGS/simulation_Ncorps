from model.Body import Body
from random import randint
from model.QuadTree import QuadTree

class BarnesHutSimulation():

    #If you specify bodies and a bodyCount, it will be taken into account if bodyCount is higher than the number of bodies in bodies
    #If so, the constructor will add random bodies to your initial bodies list to match bodyCount
    def __init__(self,bodyCount=3, mass=(5.9722*10**24), width=None, height=None, precision=1, bodies=[]):
        self.precision = precision
        self.quadTreeWidth = max(width,height)
        self.bodies = bodies
        self.bodyCount = bodyCount if bodyCount > len(bodies) else len(bodies)
        for _ in range(bodyCount-len(bodies)):
            self.bodies.append(Body(randint(20,width-20),randint(20,height-20),mass))

    def advance(self):
        #TODO compute quadtree size with maximum and minimum of all bodies positions
        quadtree = QuadTree(self.quadTreeWidth,self.bodies)

        quadtree.computeMasses()

        for body in self.bodies:
            body.acc = quadtree.computeForce(body,self.precision)  
            
        #Update the speed of both bodies and get their position accordingly
        for body in self.bodies:
            body.computeNewPos()

