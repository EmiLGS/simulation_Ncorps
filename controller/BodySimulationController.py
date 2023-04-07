import numpy as np

class BodySimulationController() :
    
    def __init__(self,simulation):
        """
         Initializes the object with data. This is called by __init__ and should not be called directly.
         
         @param simulation - The simulation to use for this object's
        """
        self.simulation = simulation
    
    def getFirstBody(self):
        """
         Returns the first body. This is a convenience method for simulating the first body of the body - set of the simulation.
         
         
         @return the first body or None if there are no bodies in the set of body - set of the simulation
        """
        return self.simulation.getFirstBody()
    
    def getSecondBody(self):
        """
         Get the body of the second body. This is the body that is used to calculate the mass of the particle.
         
         
         @return the body of the second body in km / s or None if there is no body in the particle
        """
        return self.simulation.getSecondBody()
    
    # Create a string of the first body
    def createFirstBodyString(self):
        """
         Creates string representation of first body. Used for debugging. It is the square root of the sum of the squared distances between the first and second body.
         
         
         @return string representation of first body in string form e. g. " 1. 2m " or " 1
        """
        return str(np.sqrt(self.simulation.body1.spd[0]**2 + self.simulation.body1.spd[1]**2))
    
    # Create a string of the Second body
    def createSecondBodyString(self):
        """
         Creates string representation of second body. Used for debugging. It is the square root of the sum of the squared distances between the first and second body.
         
         
         @return string representation of second body in string form e. g. " 2. 5x2 " or " 2
        """
        return str(np.sqrt(self.simulation.body2.spd[0]**2 + self.simulation.body2.spd[1]**2))
    