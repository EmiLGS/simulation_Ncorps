import matplotlib.backends.backend_agg as agg
import pygame
from pygame.locals import *
from vendor.chart.TestPlot import TestPlot

class TestChart():
    def __init__(self,data):
        self.timeChart = TestPlot(data)

    def view(self):
        pygame.init()
        # Get Chart data
        printChart = self.timeChart.printChart()
        raw_data = printChart[0]
        canvas = printChart[1]

        # Start Pygame basic
        window = pygame.display.set_mode((400, 400), DOUBLEBUF)
        screen = pygame.display.get_surface()

        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(surf, (0,0))
        pygame.display.flip()

        crashed = False
        while not crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True