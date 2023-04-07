import random
import matplotlib
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import pylab
import numpy as np
class PrecisionChart():
    def __init__(self,data):
        """
         Initialize the object with data. This is called by __init__ and should not be called directly.
         
         @param data - The data to store in the object's
        """
        self.data = data

    # Create a render of the chart and return it
    def printChart(self):
        """
         Print chart of Precision. This is a function to be used in conjunction with plot (). It returns a tuple ( chart_title chart_text ) where chart_title is the title of the chart and chart_text is a string that describes the chart.
         
         @return ( chart_title chart_text ) chart_title is a string describing the chart and chart_text is a descriptive
        """
        n=0
        # matplotlib.use("Agg")
        fig, ax = plt.subplots()
        ax.legend(loc='lower right')
        ax.set_title("Precision Chart")
        # fig = pylab.figure( figsize=[4.5, 4.5] )
        fig.patch.set_facecolor('#E6E6E6')
        # ax = fig.gca()
        ax.set(xlabel='frame',ylabel='error')
        referenceInitialState = self.data[-1][-1].get("Precision")
        # Le graphe ne peut pas le graphe ne peut pas dessiné par cause de non existence dessiné par cause de non existence d état initial stable
        if referenceInitialState == None:
            return None, "Le graphe ne peut pas être dessiné par cause de non existence d'état initial stable"
        referenceInitialState = referenceInitialState[0]
        referenceSimulation = None
        lenFrames = 0
        # This method is used to find the reference simulation and the reference simulation.
        for i in range(len(self.data)):
            # This method is used to find the reference simulation and the reference initial state.
            for j in range(len(self.data[i])):
                data = self.data[i][j]
                # This method is called by the simulation simulation.
                if data.get("Precision") != None and data.get("Precision")[0] == referenceInitialState and data.get("Algorithme") == "classic":
                    # This function is used to determine the number of frames in the reference simulation.
                    if referenceSimulation == None or lenFrames < len(data.get("Precision")[1][0]):
                        referenceSimulation = data
                        lenFrames = len(data.get("Precision")[1][0])
        # Le graphe ne peut pas le graphe ne peut pas dessiné par cause de non existence de simulation de reference
        if referenceSimulation == None:
            return None, "Le graphe ne peut pas être dessiné par cause de non existence de simulation de reference (algo naif)"
        
        # Plot the data of the reference simulation.
        for i in range(len(self.data)):
            # Plot the data for each algorithme algorithme and the number of frames in the reference simulation.
            for j in range(len(self.data[i])):
                data = self.data[i][j]
                # If the precision is not set to referenceInitialState then the data is not the initial state.
                if data.get("Precision") == None or data.get("Precision")[0] != referenceInitialState: continue
                n += 1
                # Plot the data for the algorithme and precision.
                for k,v in data.items():
                    # Set the algorithm to the algorithme.
                    if k == "Algorithme":
                        algo = v
                    # plot the frames of the reference simulation
                    if k == "Precision":
                        v = v[1]
                        frames = v[1][:lenFrames]
                        ax.plot(frames, self.bodiesToErrorFromRef(v[0],referenceSimulation.get("Precision")[1][0]),label=algo+str(n))

        
        ax.legend()
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        return raw_data,canvas,self.getAverageErrorAt20(data.get("Precision")[2], referenceSimulation.get("Precision")[2])

    def getAverageErrorAt20(self, bodies, reference):
        """
         Calculate the average error between two sets of 2D points. It is assumed that the bodies are in the same frame
         
         @param bodies - list of ( x y ) tuples
         @param reference - list of ( x y ) tuples to compare
         
         @return float or None if no
        """
        # Returns the bodies of the current body.
        if bodies == None: return None
        res = 0
        length = min(len(bodies), len(reference))
        # The distance between bodies and bodies.
        for i in range(length):
            res += np.sqrt((bodies[i][0]-reference[i][0])**2 + (bodies[i][1]-reference[i][1])**2)
        return res/length
        

    def bodiesToErrorFromRef(self, bodies, reference):
        """
         Calculate error from reference. This is a helper function to calculate the error of a list of bodies based on a reference
         
         @param bodies - list of bodies to calculate error
         @param reference - list of reference bodies to calculate error from
         
         @return list of error in percent ( 0 - 100 ) for each body in the list. It is a list of floats
        """
        res = []
        # appends the precision of the bodies and reference to the result array
        for i in range(min(len(bodies),len(reference))):
            precision = np.sqrt((bodies[i][0]-reference[i][0])**2 + (bodies[i][1]-reference[i][1])**2)/np.sqrt(reference[i][0]**2 + reference[i][1]**2)*100
            res.append(precision)
        return res
    
        #return [np.abs(bodies[i]-reference[i])/reference[i]*100 for i in range(len(bodies))]