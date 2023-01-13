import numpy as np

class Body():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.mass = 1
    
body1 = Body(0,0)
body2 = Body(10,10)
g = 9.81

for i in range(10):
    a = body2.y - body1.y
    b = body2.x - body1.x

    d = np.sqrt(a**2 + b**2)

    F = g*body1.mass*body2.mass / d**2
    directionDeLaForcePourBody1 = np.arctan(a/b)
    body1.ax = F*np.cos(directionDeLaForcePourBody1)
    body1.ay = F*np.sin(directionDeLaForcePourBody1)

    body1.vx += body1.ax
    body1.vy += body1.ay

    body1.x += body1.vx
    body1.y += body1.vy

    
    directionDeLaForcePourBody2 = directionDeLaForcePourBody1 + np.pi
    body2.ax = F*np.cos(directionDeLaForcePourBody2)
    body2.ay = F*np.sin(directionDeLaForcePourBody2)

    body2.vx += body2.ax
    body2.vy += body2.ay

    body2.x += body2.vx
    body2.y += body2.vy



    print(body1.x,body1.y,body2.x,body2.y)




