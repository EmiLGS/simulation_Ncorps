import cmath
import numpy as np
import random as random
from model.Body import Body
from model.GlobVar import GlobVar

class Node():
    def __init__(self,x0,y0,width, bodies):
        self.x0 = x0
        self.y0 = y0
        self.w = width
        self.bodies = bodies
        self.children = []
        self.massCenter = None
        self.mass = None

    #si c'est une feuille(carré) on a besoin des points qu'elle contient 
    def getBodies(self):
        return self.bodies

    def division(self):
        if(len(self.bodies)>1):
            w2 = self.w /2

            node_Point = self.pointsIn(self.x0, self.y0, w2)
            n1 = Node(self.x0, self.y0, w2, node_Point)
            n1.division()

            node_Point2 = self.pointsIn(self.x0, self.y0+w2, w2)
            n2 = Node(self.x0, self.y0+w2, w2, node_Point2)
            n2.division()

            node_Point3 = self.pointsIn(self.x0+w2, self.y0 ,w2)
            n3 = Node(self.x0+w2, self.y0, w2, node_Point3)
            n3.division()

            node_Point4 = self.pointsIn(self.x0+w2, self.y0+w2, w2)
            n4 = Node(self.x0+w2, self.y0+w2, w2, node_Point4)
            n4.division()

            self.children = [n1,n2,n3,n4]
            self.bodies = []

    def pointsIn(self,x,y,w):
        bds = []
        for body in self.bodies:
            if ((x <= body.pos[0]) and (y <= body.pos[1]) and (x + w > body.pos[0]) and (y + w > body.pos[1])):
                bds.append(body)
        return bds
    
    def isLeaf(self):
        return self.children == []
    
    def contains(self,body):
        return self.x0 <= body.pos[0] < self.x0+self.w and self.y0 <= body.pos[1] < self.y0+self.w

    def insert(self,body):
        if not self.isLeaf():
            for child in self.children:
                if child.contains(body):
                    child.insert(body)
        else:
            self.bodies.append(body)
            if len(self.bodies)>1:
                self.division()
    
    def removeEmptyLeaves(self):
        newChildren = []
        for child in self.children:
            if not child.isLeaf() or len(child.bodies) != 0:
                newChildren.append(child)
                child.removeEmptyLeaves()
        self.children = newChildren
    
    def computeMass(self):
        if self.isLeaf():
            body = self.bodies[0]
            self.mass = body.mass
            self.massCenter = body.pos
        else:
            m,cm = 0,0
            for child in self.children:
                mChild, cmChild = child.computeMass()
                m += mChild
                cm += mChild*cmChild
            cm /= m
            self.mass = m
            self.massCenter = cm
        return self.mass, self.massCenter
    
    def computeForce(self,body, precision):
        #If we only have one body we calculate the force accordingly
        if self.isLeaf():
            if self.bodies[0] == body:
                return 0
            else:
                otherBody = self.bodies[0]
        #If we have more we have to check if we can approximate all those bodies as a single one
        else:
            r = np.sqrt((self.massCenter[0] - body.pos[0]) ** 2 + (self.massCenter[1] - body.pos[1]) ** 2)
            D = self.w
            if r != 0 and D/r < precision:
                otherBody = Body(self.massCenter[0],self.massCenter[1],self.mass)
            #else we just calculate the force in all the children independently
            else:
                force = 0
                for child in self.children:
                    force += child.computeForce(body,precision)
                return force

        a = otherBody.pos[0] - body.pos[0]
        b = otherBody.pos[1] - body.pos[1]
        d = np.sqrt(a**2 + b**2)

        Vdir = np.array([a,b])
        force = ((GlobVar.G * otherBody.mass * body.mass)/d**3)*Vdir
        # print("Forc de", body, "par", otherBody,"=",force)
        return force

    def __str__(self):
        res = ""
        res += "x = " + str(self.x0)
        res += "\ny = " + str(self.y0)
        res += "\nwidth = " + str(self.w)
        if self.isLeaf():
            res += "\nbody : " + "[" + (", ").join(list(map(str,self.bodies))) + "]"
        else:
            res += "\nenfants :\n"
            for child in self.children:
                res += "\n"
                for lign in str(child).split("\n"):
                    res += "  |  " + lign + "\n"
        return res

class QuadTree():
    def __init__(self, width, bodies=[]):
        self.bodies = []
        self.node0 = Node(0,0,width,[])
        for body in bodies:
            self.quadInsert(body)
        self.node0.removeEmptyLeaves()
        print(self)

    def addBody(self,x,y):
        self.bodies.append(Body(x,y))

    def quadInsert(self,body):
        self.bodies.append(body)
        self.node0.insert(body)

    def removeEmptyLeaves(self):
        self.node0.removeEmptyLeaves()

    def computeMasses(self):
        self.node0.computeMass()
    
    def computeForce(self, body, precision):
        return self.node0.computeForce(body, precision)
    
    def __str__(self):
        return str(self.node0)

    def afficher(self):
        #quelques tests
        print("nombre de points : ", len(self.bodies) == 20)
        print(self.bodies[0].pos[0])
        # self.div()
        # print("node : ", self.node0.children[0].get_points()[0].x,",", self.node0.children[0].get_points()[0].y)