from time import sleep
import pygame
from model.ThreeBodiesSimulation import ThreeBodiesSimulation
from model.TwoBodiesSimulation import TwoBodiesSimulation
import numpy as np

class ViewTestPygame:
    pygame.init()

    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 30)


    pygame.display.set_caption('Quick Start')
    window_surface = pygame.display.set_mode((800, 800))

    background = pygame.Surface((800, 800))
    background.fill(pygame.Color('#BBBBBB'))

    is_running = True

    # sim = ThreeBodiesSimulation()
    sim = TwoBodiesSimulation()

    while is_running:
        sleep(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        window_surface.blit(background, (0, 0))

        # x1 = sim.body1.pos[0]
        # y1 = sim.body1.pos[1]
        # vx1 = sim.body1.spd[0]
        # vy1 = sim.body1.spd[1]
        # ax1 = sim.body1.acc[0]
        # ay1 = sim.body1.acc[1]

        # speed1 = my_font.render(str(np.sqrt(sim.body1.spd[0]**2 + sim.body1.spd[1]**2)), False, (0, 0, 0))
        # speed2 = my_font.render(str(np.sqrt(sim.body2.spd[0]**2 + sim.body2.spd[1]**2)), False, (0, 0, 0))
        # window_surface.blit(speed1, [x1,y1-30])
        # window_surface.blit(speed1, [sim.body2.pos[0],sim.body2.pos[1]-30])
        # pygame.draw.polygon(window_surface, (0, 0, 0), ((x1+5, y1), (x1+5000*ax1, y1+5000*ay1), (x1-5,y1)))
        
        pygame.draw.circle(window_surface,pygame.Color('#FF0000'),[sim.body1.pos[0],sim.body1.pos[1]],50)
        pygame.draw.circle(window_surface,pygame.Color('#0000FF'),[sim.body2.pos[0],sim.body2.pos[1]],10)
        # pygame.draw.circle(window_surface,pygame.Color('#00FF00'),[sim.body3.pos[0],sim.body3.pos[1]],10)

        sim.advance()

        pygame.display.update()