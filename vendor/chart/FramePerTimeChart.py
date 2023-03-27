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
        print(self.data)
        for i in range(len(self.data)):
            for k in self.data[i].keys():
                data = self.data[i]
                if k == "Temps calcul":
                    plt.plot(data[k])
                # print(data)
                # plt.plot([5,6,6,9.1,3])
            

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        return raw_data,canvas
