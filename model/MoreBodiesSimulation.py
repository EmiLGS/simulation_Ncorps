import numpy as np
from model.Body import Body
from random import randint

class MoreBodiesSimulation():

    G = 6.67*10**-11

    def __init__(self, bodyCount=None, mass=(5.9722*10**24), width=None, height=None, bodies=[]):
        self.bodies = []
        self.bodyCount = bodyCount if len(bodies) < bodyCount else len(bodies)

        self.bodies = bodies

        for _ in range(bodyCount - len(bodies)):
            self.bodies.append(Body(mass,randint(20,width-20),randint(20,height-20)))

    def advance(self):

        for body in self.bodies:
            self.computeAllForces(body)

        #Update the speed of both bodies and get their position accordinglyswww
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
                body.addForce(((self.G*body.mass*otherBody.mass)/(d**3))*Vdir)
