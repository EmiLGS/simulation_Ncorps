from model.Body import Body
from random import randint
from model.QuadTree import QuadTree

class BarnesHutSimulation():

    def __init__(self,bodyCount=3, mass=(5.9722*10**24), width=None, height=None, precision=1):
        self.precision = precision
        self.quadTreeWidth = max(width,height)
        self.bodies = [Body(randint(20,width-20),randint(20,height-20),mass) for _ in range(bodyCount)]
    
    def advance(self):

        print(", ".join(list(map(str, self.bodies))))
        quadtree = QuadTree(self.quadTreeWidth,self.bodies)

        quadtree.computeMasses()

        for body in self.bodies:
            body.acc = quadtree.computeForce(body,self.precision)  
            
        #Update the speed of both bodies and get their position accordingly
        for body in self.bodies:
            body.computeNewPos()

