import cmath
import numpy as np
import random as random

class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    #     self.z = complex(x,y)
    
    # def R(self,points):
    #     for i in points: 
    #         r = np.sqrt((self.x-i.x)**2 + (self.y-i.y))
    #     return r

    # def theta(self,r):
    #     return -1/r
class Node():
    def __init__(self,x0,y0,width, maxPoints, points):
        self.x0 = x0
        self.y0 = y0
        self.w = width
        self.m = maxPoints
        self.points = points
        self.children = []

    #si c'est une feuille(carré) on a besoin des points qu'elle contient 
    def get_points(self):
        return self.points

    def division(self):
        if(len(self.points)>self.m):
            w2 = self.w /2

            node_Point = self.pointsIn(self.x0, self.y0, w2)
            n1 = Node(self.x0, self.y0, w2, self.m, node_Point)
            n1.division()

            node_Point2 = self.pointsIn(self.x0, self.y0+w2, w2)
            n2 = Node(self.x0, self.y0+w2, w2, self.m, node_Point2)
            n2.division()

            node_Point3 = self.pointsIn(self.x0+w2, self.y0 ,w2)
            n3 = Node(self.x0, self.y0, w2, self.m, node_Point3)
            n3.division()

            node_Point4 = self.pointsIn(self.x0+w2, self.y0+w2, w2)
            n4 = Node(self.x0+w2, self.y0+w2, w2, self.m, node_Point4)
            n4.division()

            self.children = [n1,n2,n3,n4]
            self.points = []

    def pointsIn(self,x,y,w):
        pts = []
        for p in self.points:
            if ((x <= p.x) and (y <= p.y) and (x + w >= p.x) and (y + w >= p.y)):
                pts.append(p)
        return pts
    
    def isLeaf(self):
        return self.children == []
    
    def contains(self,point):
        return self.x0 <= point.x < self.x0+self.w and self.y0 <= point.y < self.y0+self.w


    def insert(self,point):
        if not self.isLeaf():
            for child in self.children:
                if child.contains(point):
                    child.insert(point)
        else:
            self.points.append(point)
            if len(self.points)>self.m:
                self.division()


class QuadTree():
    def __init__(self, m):
        self.m = m
        self.points = [Point(random.randint(0,800),random.randint(0,800)) for i in range(20)]
        self.node0 = Node(0,0,800,m,self.points)
        self.div()  

    def addPoint(self,x,y):
        self.points.append(Point(x,y))

    def quadInsert(self,point):
        self.points.append(point)
        self.node0.insert(point)
    
    def div(self):
        Node.division(self.node0)
    
    def afficher(self):
        #quelques tests
        print("nombre de points : ", len(self.points) == 20)
        print(self.points[0].y)
        self.quadInsert(Point(10,10))
        print(self.points[-1].x,self.points[-1].y)
        # self.div()
        # print("node : ", self.node0.children[0].get_points()[0].x,",", self.node0.children[0].get_points()[0].y)



q = QuadTree(1)
q.afficher()