import matplotlib
import matplotlib.backends.backend_agg as agg
import pylab
class FramePerTimeChart():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    # Create a render of the chart and return it
    def printChart(self):
        matplotlib.use("Agg")
        fig = pylab.figure( figsize=[4.5, 4.5] )
        fig.patch.set_facecolor('#E6E6E6')
        ax = fig.gca()
        ax.set_xlabel('second')
        ax.set_ylabel('frame')
        ax.plot(self.x,self.y, color='red');
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        return raw_data,canvas
