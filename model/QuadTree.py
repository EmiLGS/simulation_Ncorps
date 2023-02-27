import cmath
import numpy as np
import random as random
from Body import Body
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
    def get_points(self):
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
            print(len(self.bodies))
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
        return self.mass, self.massCenter

    def __str__(self):
        res = ""
        res += "x = " + str(self.x0)
        res += "\ny = " + str(self.y0)
        res += "\nwidth = " + str(self.w)
        res += "\nenfants :\n"
        for child in self.children:
            res += "\n"
            for lign in str(child).split("\n"):
                res += "  |  " + lign + "\n"
        return res

class QuadTree():
    def __init__(self, bodies=[]):
        self.bodies = []
        self.node0 = Node(0,0,800,[])
        for body in bodies:
            self.quadInsert(body)
        self.node0.removeEmptyLeaves()

    def addBody(self,x,y):
        self.bodies.append(Body(x,y))

    def quadInsert(self,body):
        self.bodies.append(body)
        self.node0.insert(body)

    def removeEmptyLeaves(self):
        self.node0.removeEmptyLeaves()

    def comuteMasses(self):
        self.node0.computeForce()
    
    def computeForce(self):
        if self.isLeaf():
            pass

    def afficher(self):
        #quelques tests
        print("nombre de points : ", len(self.bodies) == 20)
        print(self.bodies[0].pos[0])
        # self.div()
        # print("node : ", self.node0.children[0].get_points()[0].x,",", self.node0.children[0].get_points()[0].y)



q = QuadTree(1, [Body(10,10),Body(70,70),Body(105,2)])
q.afficher()
print(q.node0)