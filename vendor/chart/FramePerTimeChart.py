import random
import matplotlib
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import pylab
class FramePerTimeChart():
    def __init__(self,data):
        self.data = data

    # Create a render of the chart and return it
    def printChart(self):
        # matplotlib.use("Agg")
        fig, ax = plt.subplots()
        ax.legend(loc='lower right')
        ax.set_title("Time chart")
        # fig = pylab.figure( figsize=[4.5, 4.5] )
        fig.patch.set_facecolor('#E6E6E6')
        # ax = fig.gca()
        ax.set(xlabel='second',ylabel='frame')
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                data = self.data[i][j]
                for k,v in data.items():
                    if k == "Numero Simulation":
                        n = v
                    if k == "Algorithme":
                        algo = v
                    if k == "Temps calcul":
                        # print(algo+n)
                        ax.plot(v[0],v[1],label=algo+n)
        ax.legend()
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        return raw_data,canvas
