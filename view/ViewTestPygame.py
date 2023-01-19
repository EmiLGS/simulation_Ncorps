import time
import pygame
from model.TwoBodiesSimulation import TwoBodiesSimulation
from controller.BodySimulationController import BodySimulationController


class ViewTestPygame:
    pygame.init()

    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 30)


    pygame.display.set_caption('Quick Start')
    window_surface = pygame.display.set_mode((1200, 800))

    background = pygame.Surface((1200, 800))
    background.fill(pygame.Color('#BBBBBB'))

    is_running = True

    # Use simControllerulation specific.
    simController = BodySimulationController(TwoBodiesSimulation())
    body1 = simController.getFirstBody()
    body2 = simController.getSecondBody()
    # Create a clickable button to add Bodies

    # Pygame check event and updating screen.
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        window_surface.blit(background, (0, 0))

        x1 = body1.pos[0]
        y1 = body1.pos[1]
        vx1 = body1.spd[0]
        vy1 = body1.spd[1]
        ax1 = body1.acc[0]
        ay1 = body1.acc[1]

        # Print the speed of bodies 
        speed1 = my_font.render( simController.createFirstBodyString(), False, (0, 0, 0))
        speed2 = my_font.render( simController.createSecondBodyString(), False, (0, 0, 0))
        window_surface.blit(speed1, [x1,y1-30])
        window_surface.blit(speed1, [body2.pos[0],body2.pos[1]-30])
        pygame.draw.polygon(window_surface, (0, 0, 0), ((x1+5, y1), (x1+5000*ax1, y1+5000*ay1), (x1-5,y1)))
        
        pygame.draw.circle(window_surface,pygame.Color('#FF0000'), [ x1, y1 ], 10)
        pygame.draw.circle(window_surface,pygame.Color('#0000FF'), [ body2.pos[0], body2.pos[1] ], 10)
        
        simController.simulation.advance()
        pygame.display.update()