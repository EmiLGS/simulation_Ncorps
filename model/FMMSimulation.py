import cmath
import numpy as np
import random as random
from model.Body import Body
from model.GlobVar import GlobVar
from model.QuadtreeFMM import QuadTreeFMM

from itertools import chain

#Binomial coefficient
def fac(n):
    f = 1
    for i in range(1,n+1):
        f = f*i
    return f
    
def bino(n,r):
    return fac(n) // fac(r) // fac(n-r)


#compute alpha for outer 
def alpha(bodies,j, center):
    alphaj = 0
    for i in range(1,len(bodies)):
        alphaj += bodies[i].mass * complex(bodies[i].pos[0]-center[0],bodies[i].pos[1]-center[1])**j/j
    return alphaj        

#data structure representing the multipole expansion associated with n
def Outer(n):
    M = 0
    for i in n.bodies:
        M += i.mass
    outer = [M]
    outer[1:] = [alpha(n.bodies,p,(400,600)) for p in range(1,6)]
    outer.append(complex(n.center))
    return outer


def outer_shift(outer, center):
    shift = [outer[0]]
    shift[1:] = [sum([outer[k]*center**(l - k)*bino(l-1, k-1) - (outer[0]*center**l)/l
                  for k in range(1, l)]) for l in range(1, len(outer))]

    return shift

#step 2 build outer
def Build_outer(n):
    if n.isLeaf():
        n.outer =  Outer(n)
    else:
        n.outer = 0
        for i in n.children() :
            Build_outer(i)
            n.outer = n.outer + outer_shift(i.outer , complex(i.center)-complex(n.center))
    pass

# outer sauvegarde les informations qu'il faut pour trouver le potentiel loin de n grace au particules dans n
#inner c'est l'inverse grave aux particles loin de n on calcule le potentiel de n
#   
#etapes a faire demain:
#apres on cherche les voisins du parent(n) et on recupere son fils on met tout ça dans un ensemble

def beta(l, alphas, z0):
    betal = 0
    for i in range(l):
        betal += (alphas[i] * z0**l-i *bino((l-1),(i-1))) - (alphas[0]*z0**l)/l
    return betal

def convert_outer_to_inner(alphas,z0): 
    betas = []
    for i in alphas:
        betas.append(beta(5,alphas,z0))
    betas.append(z0)
    return betas

#n1 inside n2, we try to convert inner n2 to inner n1
def inner_shift(betas, z0):
    shift = [sum([betas[j]*bino(j,i)*(-z0)**(j-i)
              for j in range(i,len(betas))])
              for i in range(len(betas))]
    return shift


def Build_inner(n):
    p = n.Parent()
    z0 = complex(*p.center) - complex(*n.center)
    n.inner = inner_shift(p.inner,z0)
    for i in n.Interaction_Set():
        z0 = complex(*i.center) - complex(*n.center)
        n.inner = n.inner + convert_outer_to_inner(i.outer, z0)

    if n.isLeaf() :
        z0 = complex(n.center)
        betas = n.inner
        for p in n.bodies:
            z = complex(*p.pos)
            p.phi -= np.real(np.polyval(betas[::-1],z-z0))

        for nn in n.nearest_neighbors:
            potentialDDS(n.bodies, nn.bodies)

        # Compute all-to-all potential from all particles in leaf cell
        po = potentialDS(n.bodies)

    else:
        for c in n.children :
            Build_inner(c)

#auteur : github de Luis Barroso-Luque
#----------------------------------------------------
class FMM():
    def __init__(particles, width, tree_thresh=None , nterms=5):
        tree = QuadTreeFMM(width, particles, tree_thresh)
        Build_outer(tree.node0)
        tree.node0.inner = np.zeros((nterms + 1), dtype=complex)
        any(Build_inner(child) for child in tree.node0)

def potentialDDS(bodies, sources):
    for i, body in enumerate(bodies):
        for source in sources:
            r = Distance(body.pos, source.pos)
            body.phi -= body.charge*np.log(r)


def potentialDS(bodies):
    phi = np.zeros((len(bodies),))

    for i, body in enumerate(bodies):
        for source in (bodies[:i] + bodies[i+1:]):
            r = Distance(body.pos, source.pos)
            body.phi -= body.charge*np.log(r)
        phi[i] = body.phi

    return phi
#----------------------------------------------------

def Distance(p1, p2):
    x1,x2 = p1[0],p2[0]
    y1,y2 = y1[0],y2[0]
    return np.sqrt((x1-x2)**2+(y1-y2)**2)