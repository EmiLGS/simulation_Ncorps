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
        # fig = pylab.figure( figsize=[4.5, 4.5] )
        fig.patch.set_facecolor('#E6E6E6')
        # ax = fig.gca()
        ax.set(xlabel='second',ylabel='frame')
        i = 1
        for k in self.data.keys():
            data = self.data[k]
            for k2 in data.keys():
                print("Il y a" + str(i) + "courbe")
                if k2 == "Temps_calcul":
                    ax.plot(data[k2][0],data[k2][1])
            i += 1

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        return raw_data,canvas
