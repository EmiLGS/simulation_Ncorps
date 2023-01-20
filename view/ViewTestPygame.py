import time
import pygame, sys
from model.TwoBodiesSimulation import TwoBodiesSimulation
from controller.BodySimulationController import BodySimulationController

class ViewTestPygame:
    def __init__(self):
        pygame.init()

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)

        pygame.display.set_caption('Quick Start')
        self.window_surface = pygame.display.set_mode((1200, 800))

        self.background = pygame.Surface((1200, 800))
        self.background.fill(pygame.Color('#BBBBBB'))

        self.run_menu = True
        self.run_simulation = False

        self.box_idle = pygame.transform.scale(pygame.image.load("view/red_button11.png"),(380,98))
        self.box_pressed = pygame.transform.scale(pygame.image.load("view/red_button12.png"),(380, 98))

    def menu(self):

        # Différentes écritures
        Jouer = self.my_font.render('Jouer', True, "white")
        Level= self.my_font.render('Notice', True, "white")
        Quitter = self.my_font.render('Quitter', True, "white")

        while self.run_menu:
            # Récuperer positions de la souris
            mouseX, mouseY = pygame.mouse.get_pos()

            # Afficher les écritures
            self.window_surface.blit(self.background,(0,0))

            # Zones d'interactions si souris passe sur les boutons
            rect_jouer = pygame.Rect(350, 275, 380, 98)
            rect_level = pygame.Rect(350, 390, 380, 98)
            rect_quitter = pygame.Rect(350, 510, 380, 98)

            # Animations quand souris passe sur les boutons
            # Bouton Jouer
            if not rect_jouer.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.box_idle, (350, 275))
                self.window_surface.blit(Jouer, (460, 300))
            else:
                self.window_surface.blit(self.box_idle, (350, 285))
                self.window_surface.blit(Jouer, (460, 310))

             #Bouton Level
            if not rect_level.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.box_idle, (350, 390))
                self.window_surface.blit(Level, (460, 420))
            else:
                self.window_surface.blit(self.box_idle, (350, 400))
                self.window_surface.blit(Level, (460, 430))

            # Bouton Quitter
            if not rect_quitter.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.box_idle, (350, 510))
                self.window_surface.blit(Quitter, (425, 540))
            else:
                self.window_surface.blit(self.box_idle, (350, 520))
                self.window_surface.blit(Quitter, (425, 550))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # Evenements lors du clique
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si clique sur bouton Jouer
                    if rect_jouer.collidepoint((mouseX,mouseY)):

                        # Lancer la transition
                        self.run_menu = False
                        self.run_simulation = True
                        self.simulation()

                    # Si clique sur bouton Quitter
                    if rect_quitter.collidepoint((mouseX,mouseY)):
                        sys.exit()

    def simulation(self):
        # Use simControllerulation specific.
        simController = BodySimulationController(TwoBodiesSimulation())
        body1 = simController.getFirstBody()
        body2 = simController.getSecondBody()
        while self.run_simulation:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_simulation = False

            self.window_surface.blit(self.background, (0, 0))

            x1 = body1.pos[0]
            y1 = body1.pos[1]
            vx1 = body1.spd[0]
            vy1 = body1.spd[1]
            ax1 = body1.acc[0]
            ay1 = body1.acc[1]

            # Print the speed of bodies 
            speed1 = self.my_font.render( simController.createFirstBodyString(), False, (0, 0, 0))
            speed2 = self.my_font.render( simController.createSecondBodyString(), False, (0, 0, 0))
            self.window_surface.blit(speed1, [x1,y1-30])
            self.window_surface.blit(speed1, [body2.pos[0],body2.pos[1]-30])
            pygame.draw.polygon(self.window_surface, (0, 0, 0), ((x1+5, y1), (x1+5000*ax1, y1+5000*ay1), (x1-5,y1)))
            
            pygame.draw.circle(self.window_surface,pygame.Color('#FF0000'), [ x1, y1 ], 10)
            pygame.draw.circle(self.window_surface,pygame.Color('#0000FF'), [ body2.pos[0], body2.pos[1] ], 10)
            
            simController.simulation.advance()
            pygame.display.update()

# Pygame check event and updating screen.
