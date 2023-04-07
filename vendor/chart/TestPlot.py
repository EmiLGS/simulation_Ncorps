import matplotlib
import matplotlib.backends.backend_agg as agg
import pylab
class TestPlot():
    def __init__(self,data):
        """
         Initialize the object with data. This is called by __init__ and should not be called directly.
         
         @param data - The data to store in the object's
        """
        self.data = data
        
    # Create a render of the chart and return it
    def printChart(self):
        """
         Print the chart and return the raw data and canvas. This is useful for debugging and to get a more readable representation of the chart
         
         @return tuple of raw data and the canvas
        """
        matplotlib.use("Agg")
        fig = pylab.figure( figsize=[4, 4], dpi=100)
        ax = fig.gca()
        ax.plot(self.data)
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        return raw_data,canvas
