import cmath
import numpy as np
import random as random
from model.Body import Body
from model.GlobVar import GlobVar

class Node():
    DISREGARD = (1,2,0,3)
    CORNER_CHILDREN = (3, 2, 0, 1)

    def __init__(self,x0,y0,width, bodies, level = 0):
        self.x0 = x0
        self.y0 = y0
        self.center = (x0 + width/2 , y0 + width/2)
        self.bodies = bodies
        self.children = []
        self.parent = []
        self.massCenter = None
        self.mass = None
        self.inner, self.outer = None, None
        self._cneighbors = 4*[None,]
        self._nneighbors = None
        self.level = level

    #si c'est une feuille(carré) on a besoin des points qu'elle contient 
    def getBodies(self):
        return self.bodies

    def division(self):
        if(len(self.bodies)>1):
            w2 = self.w /2

            node_Point = self.pointsIn(self.x0, self.y0, w2)
            n1 = Node(self.x0, self.y0, w2, node_Point, level = self.level + 1)
            n1.division()

            node_Point2 = self.pointsIn(self.x0, self.y0+w2, w2)
            n2 = Node(self.x0, self.y0+w2, w2, node_Point2, level = self.level + 1)
            n2.division()

            node_Point3 = self.pointsIn(self.x0+w2, self.y0 ,w2)
            n3 = Node(self.x0+w2, self.y0, w2, node_Point3, level = self.level + 1)
            n3.division()

            node_Point4 = self.pointsIn(self.x0+w2, self.y0+w2, w2)
            n4 = Node(self.x0+w2, self.y0+w2, w2, node_Point4, level = self.level + 1)
            n4.division()

            self.children = [n1,n2,n3,n4]
            for i in self.children:
                i.parent.append(self)
                i.parent.append(k for k in self.parent) 
                
            self.bodies = []

    def pointsIn(self,x,y,w):
        bds = []
        for body in self.bodies:
            if ((x <= body.pos[0]) and (y <= body.pos[1]) and (x + w > body.pos[0]) and (y + w > body.pos[1])):
                bds.append(body)
        return bds
    

    def thresh_division(self, thresh):
        if len(self) > thresh:
            self.division()
        if not self.isLeaf():
            for child in self.children:
                child.thresh_division(thresh)

    def isLeaf(self):
        return self.children == []

    def Parent(self):
        return self.parent[0]

    def contains(self,body):
        return self.x0 <= body.pos[0] < self.x0+self.w and self.y0 <= body.pos[1] < self.y0+self.w

    def insert(self,body):
        if not self.isLeaf():
            for child in self.children:
                if child.contains(body):
                    child.insert(body)
        else:
            self.bodies.append(body)
   

#auteur : github de Luis Barroso-Luque----------------------    
    
    def set_cneighbors(self):
        for i, child in enumerate(self._children):
            # Set sibling neighbors
            sn = (abs(1 + (i^1) - i), abs(1 + (i^2) - i))
            child._cneighbors[sn[0]] = self._children[i^1]
            child._cneighbors[sn[1]] = self._children[i^2]
            # Set other neighbors from parents neighbors
            pn = tuple(set((0,1,2,3)) - set((sn)))
            nc = lambda j, k: j^((k+1)%2+1)
            child._cneighbors[pn[0]] = (self._cneighbors[pn[0]]._get_child(nc(i, pn[1]))
                                        if self._cneighbors[pn[0]] is not None
                                        else None)
            child._cneighbors[pn[1]] = (self._cneighbors[pn[1]]._get_child(nc(i, pn[0]))
                                        if self._cneighbors[pn[1]] is not None
                                        else None)
            # Recursively set cneighbors
            if child._has_children():
                child.set_cneighbors()

    def nearest_neighbors(self):
        if self._nneighbors is not None:
            return self._nneighbors

        # Find remaining nearest neighbors of same level
        nn = [cn._cneighbors[(i+1)%4]
              for i, cn in enumerate(self._cneighbors)
              if cn is not None and cn.level == self.level]
        # Find remaining nearest neigbor at lower levels #So hacky!
        nn += [cn._cneighbors[(i+1)%4]._get_child(self.CORNER_CHILDREN[i])
               for i, cn in enumerate(self._cneighbors)
               if cn is not None and cn._cneighbors[(i+1)%4] is not None and
               (cn.level < self.level and i != self.DISREGARD[self._cindex])]

        nn = [n for n in self._cneighbors + nn if n is not None]
        self._nneighbors = nn
        return nn

    def interaction_set(self):
        nn, pn = self.nearest_neighbors, self.parent.nearest_neighbors
        int_set = []
        for n in pn:
            if n._has_children():
                int_set += [c for c in n if c not in nn]
            elif n not in nn:
                int_set.append(n)
        return int_set
#-----------------------------------------------------------------------
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
    nbInteract = 0

    def __init__(self, width=1200, bodies=[], thresh=5):
        self.bodies = bodies
        self.node0 = Node(0,0,width,[])

        self.thresh = thresh
        self._build_tree(bodies)
        self.depth = None

    def _build_tree(self,bodies):
        self.node0.insert(body for body in bodies)
        self.node0.thresh_division(self.threshold)
        self.node0.set_cneighbors()

    def __str__(self):
        return str(self.node0)

#auteur : github de Luis Barroso-Luque
#------------------------------------------------------
    def __len__(self):
        l = len(self.node0)
        for node in self.node0.traverse():
            l += len(node)
        return l

    def __iter__(self):
        for points in self.node0.get_points():
            yield points

    @property
    def depth(self):
        if self.depth is None:
            self.depth = max([node.level for node in self.node0.traverse()])
        return self.depth

    @property
    def nodes(self):
        return [node for node in self.node0.traverse()]

    def traverse_nodes(self):
        for node in self.node0.traverse():
            yield node

#------------------------------------------------------

