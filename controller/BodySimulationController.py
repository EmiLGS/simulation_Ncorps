import numpy as np

class BodySimulationController() :
    
    def __init__(self,simulation):
        self.simulation = simulation
    
    def getFirstBody(self):
        return self.simulation.getFirstBody()
    
    def getSecondBody(self):
        return self.simulation.getSecondBody()
    
    # Create a string of the first body
    def createFirstBodyString(self):
        return str(np.sqrt(self.simulation.body1.spd[0]**2 + self.simulation.body1.spd[1]**2))
    
    # Create a string of the Second body
    def createSecondBodyString(self):
        return str(np.sqrt(self.simulation.body2.spd[0]**2 + self.simulation.body2.spd[1]**2))