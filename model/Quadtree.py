import cmath
import numpy as np
import random as random


#Obsolete. Check QuadTreeFMM or QuadTreeBarnesHut depending on what you want
class Point():
    def __init__(self,x,y):
        """
         Initialize the instance with x and y. This is used to make it easier to use __init__
         
         @param x - The x value of the point
         @param y - The y value of the point ( must be same as x
        """
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
        """
         Initialize the node with the given parameters. This is the constructor for the Node class. It should not be called directly by user code.
         
         @param x0 - The x coordinate of the top left corner of the node.
         @param y0 - The y coordinate of the top left corner of the node.
         @param width - The width of the node. This is the number of cells that make up the node.
         @param points - The points of the node in the form of a list
        """
        self.x0 = x0
        self.y0 = y0
        self.w = width
        self.points = points
        self.children = [] 

    #si c'est une feuille(carré) on a besoin des points qu'elle contient 
    def get_points(self):
        """
         Get the points that make up the polygon. This is useful for debugging and to avoid having to re - create the polygon every time it is used.
         
         
         @return A list of : class : ` ~compas. geometry. Point ` objects representing the points that make up the polygon
        """
        return self.points

def division(node, m):
    """
     Divide the node into m equally sized subtrees. This is used to determine the size of the subdivision tree
     
     @param node - The node to be divided
     @param m - The number of subtrees to divide the tree
    """
    # Create a new node with the points in the node.
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
    """
     Returns a list of points in a rectangle. This is a helper function for L { Intersection }.
     
     @param x - X coordinate of the rectangle. It is assumed that the top left corner of the rectangle is ( 0 0 ).
     @param y - Y coordinate of the rectangle. It is assumed that the top left corner of the rectangle is ( 0 0 ).
     @param w - Width of the rectangle. It is assumed that the top left corner of the rectangle is ( 0 0 ).
     @param points - A list of points to check. Each point is a namedtuple with x and y attributes.
     
     @return A list of points in the rectangle defined by x y w and points. The list is sorted by x
    """
    pts = []
    # Add points to the list of points.
    for p in points:
        # Add the point to the list of points.
        if ((x <= p.x) and (y <= p.y) and (x + w >= p.x) and (y + w >= p.y)):
            pts.append(p.x)
    return pts

class QuadTree():
    def __init__(self, m):
        """
         Initialize the murrow. This is called by __init__ to initialize the murrow.
         
         @param m - The number of rows in the murrow
        """
        self.m = m
        self.points = [Point(random.randint(0,800),random.randint(0,800)) for i in range(20)]
        self.node0 = Node(0,0,800,self.points)

    def addPoint(self,x,y):
        """
         Adds a point to the plot. This is useful for debugging and to avoid having to re - calculate the values every time you add a point
         
         @param x - x coordinate of the point
         @param y - y coordinate of the point ( must be >
        """
        self.points.append(Point(x,y))
    
    def div(self):
        """
         Divide node0 by m and store result in node0. This is equivalent to a division in C
        """
        division(self.node0,self.m)
    
    def afficher(self):
        """
         Affichage d'un niveau de nodre. Cette fonction permet de afficher les
        """
        # quelques testes 
        print("nombre de points : ", len(self.points) == 20)
        print(self.points[0].y)
        self.div()
        print("node : ", self.node0.children[0].get_points()[0].x,",", self.node0.children[0].get_points()[0].y)