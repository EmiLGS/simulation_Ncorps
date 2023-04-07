import numpy as np

class Body():
    def __init__(self, x, y, mass=10**11):
        """
         Initialize the object with x y and mass. This is called by __init__ and should not be called directly
         
         @param x - x coordinate of the object
         @param y - y coordinate of the object ( default 10 ** 11 )
         @param mass - mass of the object ( default 10 ** 11
        """
        self.pos = np.array([float(x),float(y)])
        self.spd = np.array([0.0,0.0])
        self.acc = np.array([0.0,0.0])
        # MASSE TERRE = 5.9722*10**24
        # MASSE MINIMALE = 10**11
        self.mass = mass
        

    def addForce(self,force):
        """
         Add a force to the accelerometer. This is a convenience method for the use of : meth : ` ~montreal_forced_modulation `
         
         @param force - The force to add
        """
        self.acc += force/float(self.mass)

    def computeNewPos(self):
        """
         Compute new position and acceleration based on current position and acceleration. Acceleration is reduced to max acceleration
        """
        #TODO check if accMax is good enough or if there is a way to improve it
        #! Temporarily removing it seems to work a bit. Don't use masses too big or everything goes boom
        # accMag = np.sqrt(self.acc[0]**2 + self.acc[1]**2)
        # accMax = np.inf
        # self.acc = self.acc if accMag < accMax else self.acc/accMag * np.array([accMax,accMax])
        #Add acceleration to speed
        self.spd += self.acc

        #Add speed to position
        self.pos += self.spd

    def __str__(self):
        """
         Returns a string representation of the body. This is used for debugging purposes and should not be used for anything else.
         
         
         @return A string representation of the body in a format suitable for debugging purposes. Example : " Body : x = 10 y = 10
        """
        return "Body : x =  " + str(self.pos[0]) + ", y = " + str(self.pos[1])
    
    #!! Disgusting function ...
    def getBodyColor(self,size):
        """
         Returns the color to use for the body. It is based on the size of the body and the number of rows / colums that will be used to fill the body
         
         @param size - The size of the body
         
         @return The color to use for the body in the form #RRGGBB where # is the number of
        """
        # Returns the color of the size in the format 0x00FF0000.
        if size >= 1 and size < 4:
            return '#000000'
        elif size >= 4 and size < 7:
            return '#999999'
        elif size == 7:
            return '#FFD02D'
        elif size > 7 and size < 10:
            return '#FF9900'
        elif size == 10:
            return '#FF0000'
