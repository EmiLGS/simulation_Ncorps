import random
import matplotlib
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import pylab
class FramePerTimeChart():
    def __init__(self,data):
        """
         Initialize the object with data. This is called by __init__ and should not be called directly.
         
         @param data - The data to store in the object's
        """
        self.data = data

    # Create a render of the chart and return it
    def printChart(self):
        """
         Prints the time chart of the simulation. It is used to visualize the performance of the simulations
         
         
         @return True if the chart
        """
        # matplotlib.use("Agg")
        fig, ax = plt.subplots()
        ax.legend(loc='lower right')
        ax.set_title("Time chart")
        # fig = pylab.figure( figsize=[4.5, 4.5] )
        fig.patch.set_facecolor('#E6E6E6')
        # ax = fig.gca()
        ax.set(xlabel='second',ylabel='frame')
        # Plot the data in the data set.
        for i in range(len(self.data)):
            # Plot the data for each data item in the data array i.
            for j in range(len(self.data[i])):
                data = self.data[i][j]
                # Plot the data for the given data.
                for k,v in data.items():
                    # Numero Simulation n is Numero Simulation
                    if k == "Numero Simulation":
                        n = v
                    # Set the algorithm to the algorithme
                    if k == "Algorithme":
                        algo = v
                    # plot the temps calcul plot.
                    if k == "Temps calcul":
                        ax.plot(v[0],v[1],label=algo+n)
        ax.legend()
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        return raw_data,canvas
