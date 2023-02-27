from Body import Body
from random import randint
from QuadTree import QuadTree

class BarnesHutSimulation():
    
    def __init__(self,bodyCount=3, mass=(5.9722*10**24), width=None, height=None):
        self.bodies = [Body(mass,randint(20,width-20),randint(20,height-20)) for _ in range(bodyCount)]
    
    def advance(self):

        quadtree = QuadTree(1, self.bodies)

        quadtree.computeMasses()

        for body in self.bodies:
            quadtree.computeForce(body)

        #Update the speed of both bodies and get their position accordingly
        for body in self.bodies:
            body.computeNewPos()
