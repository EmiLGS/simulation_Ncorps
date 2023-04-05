import random
import matplotlib
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import pylab
import numpy as np
class PrecisionChart():
    def __init__(self,data):
        self.data = data

    # Create a render of the chart and return it
    def printChart(self):
        # matplotlib.use("Agg")
        fig, ax = plt.subplots()
        ax.legend(loc='lower right')
        ax.set_title("Precision Chart")
        # fig = pylab.figure( figsize=[4.5, 4.5] )
        fig.patch.set_facecolor('#E6E6E6')
        # ax = fig.gca()
        ax.set(xlabel='frame',ylabel='error')
        referenceInitialState = self.data[-1][-1].get("Precision")
        if referenceInitialState == None:
            return None, "Le graphe ne peut pas être dessiné par cause de non existence d'état initial stable"
        referenceInitialState = referenceInitialState[0]
        referenceSimulation = None
        lenFrames = 0
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                data = self.data[i][j]
                if data.get("Precision") != None and data.get("Precision")[0] == referenceInitialState and data.get("Algorithme") == "classic":
                    if referenceSimulation == None or lenFrames < len(data.get("Precision")[1][0]):
                        referenceSimulation = data
                        lenFrames = len(data.get("Precision")[1][0])
        if referenceSimulation == None:
            return None, "Le graphe ne peut pas être dessiné par cause de non existence de simulation de reference (algo naif)"
        
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                data = self.data[i][j]
                if data.get("Precision") == None or data.get("Precision")[0] != referenceInitialState: continue
                for k,v in data.items():
                    if k == "Numero Simulation":
                        n = v
                    if k == "Algorithme":
                        algo = v
                    if k == "Precision":
                        v = v[1]
                        frames = v[1][:lenFrames]
                        ax.plot(v[1], self.bodiesToError(v[0],referenceSimulation.get("Precision")[1][0]),label=algo+n)
        ax.legend()
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        return raw_data,canvas

    def bodiesToError(self, bodies,reference):
        res = []
        for i in range(min(len(bodies),len(reference))):
            precX = np.abs(bodies[i][0]-reference[i][0])/reference[i][0]*100
            precY = np.abs(bodies[i][1]-reference[i][1])/reference[i][1]*100
            res.append((precX+precY)/2)
        return res
    
        #return [np.abs(bodies[i]-reference[i])/reference[i]*100 for i in range(len(bodies))]