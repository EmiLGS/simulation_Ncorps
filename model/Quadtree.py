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
    def __init__(self,x0,y0,width, points):
        self.x0 = x0
        self.y0 = y0
        self.w = width
        self.points = points
        self.children = [] 

    #si c'est une feuille(carré) on a besoin des points qu'elle contient 
    def get_points(self):
        return self.points

def division(node, m):
    if(len(node.points)>m):
        w2 = float(node.w /2)
    
        node_Point = PointsIn(node.x0, node.y0, w2, node.points)
        n1 = Node(node.x0, node.y0, w2,node_Point)
        division(n1,m)

        node_Point2 = PointsIn(node.x0, node.y0+w2, w2, node.points)
        n2 = Node(node.x0, node.y0+w2, w2, node_Point2)
        division(n2,m)

        node_Point3 = PointsIn(node.x0+w2, node.y0 ,w2, node.points)
        n3 = Node(node.x0, node.y0, w2, node_Point3)
        division(n3,m)

        node_Point4 = PointsIn(node.x0+w2, node.y0+w2, w2, node.points)
        n4 = Node(node.x0+w2, node.y0+w2, w2, node_Point4)
        division(n4,m) 

        node.children = [n1,n2,n3,n4]

def PointsIn(x,y,w,points):
    pts = []
    for p in points:
        if ((x <= p.x) and (y <= p.y) and (x + w >= p.x) and (y + w >= p.y)):
            pts.append(p.x)
    return pts

class QuadTree():
    def __init__(self, m):
        self.m = m
        self.points = [Point(random.randint(0,800),random.randint(0,800)) for i in range(20)]
        self.node0 = Node(0,0,800,self.points)

    def addPoint(self,x,y):
        self.points.append(Point(x,y))
    
    def div(self):
        division(self.node0,self.m)
    
    def afficher(self):
        #quelques testes 
        print("nombre de points : ", len(self.points) == 20)
        print(self.points[0].y)
        # self.div()
        # print("node : ", self.node0.children[0].get_points()[0].x,",", self.node0.children[0].get_points()[0].y)



q = QuadTree(1)
q.afficher()