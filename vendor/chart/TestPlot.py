import matplotlib
import matplotlib.backends.backend_agg as agg
import pylab
class TestPlot():
    def __init__(self,data):
        self.data = data
        
    # Create a render of the chart and return it
    def printChart(self):
        matplotlib.use("Agg")
        fig = pylab.figure( figsize=[4, 4], dpi=100)
        ax = fig.gca()
        ax.plot(self.data);
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        return raw_data,canvas
