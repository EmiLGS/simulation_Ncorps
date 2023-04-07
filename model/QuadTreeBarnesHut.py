import cmath
import numpy as np
import random as random
from model.Body import Body
from model.GlobVar import GlobVar

class Node():
    def __init__(self,x0,y0,width, bodies):
        """
         Initialize the mass model. This is called by __init__ and should not be called directly. Instead you should use
         
         @param x0 - x position of the center of mass
         @param y0 - y position of the center of mass ( in microns )
         @param width - width of the mass ( in metres )
         @param bodies - list of bodies that make up the mass
        """
        self.x0 = x0
        self.y0 = y0
        self.w = width
        self.bodies = bodies
        self.children = []
        self.massCenter = None
        self.mass = None

    #si c'est une feuille(carré) on a besoin des points qu'elle contient 
    def getBodies(self):
        """
         Returns the bodies associated with this message. This is a copy of the : attr : ` bodies ` attribute.
         
         
         @return a list of : class : ` Body ` objects or None if there are no bodies associated with this
        """
        return self.bodies

    def division(self):
        """
         Divide the body into four nodes and return the result. This is useful for debugging and to ensure that the nodes don't collide
        """
        # This method is used to create a new node with the same shape as the node.
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
        """
         Returns a list of bodies in the rectangle defined by x y w. This is useful for debugging and to determine which bodies are part of the rectangle
         
         @param x - x coordinate of the rectangle
         @param y - y coordinate of the rectangle ( top left corner )
         @param w - width of the rectangle ( width ). It must be greater than 0
         
         @return list of : class : ` Body `
        """
        bds = []
        # Add a body to the list of bds.
        for body in self.bodies:
            # Add a body to the list of bds if the position is within the bounds of the body.
            if ((x <= body.pos[0]) and (y <= body.pos[1]) and (x + w > body.pos[0]) and (y + w > body.pos[1])):
                bds.append(body)
        return bds
    
    def isLeaf(self):
        """
         Returns true if this node is a leaf. A leaf is a node with no children. This is used to determine if a node can be removed from the tree without losing information.
         
         
         @return C { True } if this node is a leaf C { False } otherwise ( not an error )
        """
        return self.children == []
    
    def contains(self,body):
        """
         Checks if body is contained in this rectangle. This is used to determine if a rectangular area is inside the body's bounding box
         
         @param body - Body to check for containment in this rectangle
         
         @return True if body is inside this rectangle False if not or if the body is outside the rectangle's
        """
        return self.x0 <= body.pos[0] < self.x0+self.w and self.y0 <= body.pos[1] < self.y0+self.w

    def insert(self,body):
        """
         Insert a body into the tree. This is a recursive function so you can insert bodies into subtrees and their children
         
         @param body - Body to be inserted
        """
        # Inserts the body of the tree.
        if not self.isLeaf():
            # Inserts the body to the children of this node.
            for child in self.children:
                # Inserts the body into the child if it does not already exist.
                if child.contains(body):
                    child.insert(body)
        else:
            self.bodies.append(body)
            # division if there is more than one body
            if len(self.bodies)>1:
                self.division()
    
    def removeEmptyLeaves(self):
        """
         Remove leaves that have no bodies. This is useful for debugging and to ensure that a tree does not end up empty
        """
        newChildren = []
        # Add a leaf to the list of children.
        for child in self.children:
            # Add a leaf to the list of children.
            if not child.isLeaf() or len(child.bodies) != 0:
                newChildren.append(child)
                child.removeEmptyLeaves()
        self.children = newChildren
    
    def computeMass(self):
        """
         Compute and return the mass of the node and its descendents. This is used to compute the center of mass of the body in the tree.
         
         
         @return tuple ( mass center ) where mass is the mass of the node and center is the center of mass
        """
        # Compute mass and massCenter of the leaf.
        if self.isLeaf():
            body = self.bodies[0]
            self.mass = body.mass
            self.massCenter = body.pos
        else:
            m,cm = 0,0
            # Computes the mass of all children of the graph.
            for child in self.children:
                mChild, cmChild = child.computeMass()
                m += mChild
                cm += mChild*cmChild
            cm /= m
            self.mass = m
            self.massCenter = cm
        return self.mass, self.massCenter
    
    def computeForce(self,body, precision):
        """
         Compute the force that would be applied to a body if it were to collide with the body.
         
         @param body - The body to compute the force for. It is assumed that the physics system has been built and is in the coordinate system of the body
         @param precision
        """
        #If we only have one body we calculate the force accordingly
        # Calculate the force of the leaf.
        if self.isLeaf():
            # Returns the number of bodies in the body.
            if self.bodies[0] == body:
                return 0
            else:
                otherBody = self.bodies[0]
        #If we have more we have to check if we can approximate all those bodies as a single one
        else:
            r = np.sqrt((self.massCenter[0] - body.pos[0]) ** 2 + (self.massCenter[1] - body.pos[1]) ** 2)
            D = self.w
            # compute the force of the body
            if r != 0 and D/r < precision:
                otherBody = Body(self.massCenter[0],self.massCenter[1],self.mass)
            #else we just calculate the force in all the children independently
            else:
                force = 0
                # Compute the force of the body of the body.
                for child in self.children:
                    force += child.computeForce(body,precision)
                return force

        a = otherBody.pos[0] - body.pos[0]
        b = otherBody.pos[1] - body.pos[1]
        d = np.sqrt(a**2 + b**2)

        Vdir = np.array([a,b])
        QuadTree.nbInteract += 1
        force = ((GlobVar.G * otherBody.mass * body.mass)/d**3)*Vdir
        # print("Forc de", body, "par", otherBody,"=",force)
        return force

    def __str__(self):
        """
         Returns a string representation of the node. Used for debugging. It is the same as __str__ but with more information.
         
         
         @return A string representation of the node in human readable form ( x y w body nenfants|child
        """
        res = ""
        res += "x = " + str(self.x0)
        res += "\ny = " + str(self.y0)
        res += "\nwidth = " + str(self.w)
        # Returns a string representation of this node.
        if self.isLeaf():
            res += "\nbody : " + "[" + (", ").join(list(map(str,self.bodies))) + "]"
        else:
            res += "\nenfants :\n"
            # Returns a string representation of the tree
            for child in self.children:
                res += "\n"
                # prints the child as a string
                for lign in str(child).split("\n"):
                    res += "  |  " + lign + "\n"
        return res

class QuadTree():
    nbInteract = 0

    def __init__(self, width, xShift, yShift, bodies=[]):
        """
         Initializes a quad tree. This is the top level node that is used to represent the quad tree.
         
         @param width - width of the quad tree in pixels. It is the number of quads that will be created in the tree.
         @param xShift - x - coordinate of the node's left edge.
         @param yShift - y - coordinate of the node's top edge.
         @param bodies - list of : class : ` Body ` objects
        """
        self.xShift = xShift
        self.yShift = yShift
        self.bodies = []
        self.realBodiesToFakeBodies = {}
        self.node0 = Node(0,0,width,[])
        # Inserts quads in the quads.
        for body in bodies:
            self.quadInsert(body)
        self.node0.removeEmptyLeaves()
        # print(self)

    def quadInsert(self,realBody):
        """
         Insert a real body into the quad. This is used to simulate an infinitely large body that is going to be moved to the bottom of the physics world
         
         @param realBody - The real body to
        """
        self.realBodiesToFakeBodies[realBody] = Body(realBody.pos[0]+self.xShift, realBody.pos[1]+self.yShift, realBody.mass)
        self.bodies.append(self.realBodiesToFakeBodies[realBody])
        self.node0.insert(self.realBodiesToFakeBodies[realBody])

    def removeEmptyLeaves(self):
        """
         Remove empty leaves from the tree. This is useful for debugging and to ensure that the tree is in a consistent state
        """
        self.node0.removeEmptyLeaves()

    def computeMasses(self):
        """
         Compute masses of the node. This is called by mass_computation. py and should be overridden
        """
        self.node0.computeMass()
    
    def computeForce(self, body, precision):
        """
         Compute the force for the body. This is a wrapper around QuadTree. computeForce that clears the Interact flag before returning to the root node
         
         @param body - Body to compute the force for
         @param precision - Precision of the force ( 0 - 9 )
         
         @return A list of floats representing the force in each direction ( m / s^2 / s^3
        """
        QuadTree.nbInteract = 0
        return self.node0.computeForce(self.realBodiesToFakeBodies[body], precision)
    
    def __str__(self):
        """
         Returns a string representation of the node. This is useful for debugging purposes. The string representation can be parsed by : py : func : ` astropy. graph. Graph. from_string ` or
         
         
         @return The string representation of the
        """
        return str(self.node0)

    def afficher(self):
        """
         Affichage d'un bonne. @function { public } afficher @param { void }
        """
        #quelques tests
        print("nombre de points : ", len(self.bodies) == 20)
        print(self.bodies[0].pos[0])
        self.div()
        print("node : ", self.node0.children[0].get_points()[0].x,",", self.node0.children[0].get_points()[0].y)