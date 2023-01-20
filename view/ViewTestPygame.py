import time
import pygame, sys

from controller.BodySimulationController import BodySimulationController
from model.TwoBodiesSimulation import TwoBodiesSimulation

class ViewTestPygame():
    def __init__(self):
        pygame.init()

        # Polices
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        pygame.font.get_fonts()

        # Parametre de la fenetre
        self.width = 1200
        self.height = 800

        pygame.display.set_caption('Ncorps')
        self.window_surface = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface((1200, 800))
        self.background.fill(pygame.Color('#BBBBBB'))

        # Boucles pour les ecrans
        self.run_menu = True
        self.run_simulation = False
        self.run_notice = False

        # Charger les images
        self.button_dim = (380,98)
        self.box_idle = pygame.transform.scale(pygame.image.load("view/red_button11.png"),(self.button_dim[0],self.button_dim[1]))
        self.box_pressed = pygame.transform.scale(pygame.image.load("view/red_button12.png"),(self.button_dim[0], self.button_dim[1]))

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
            self.button_posX = (self.width/2)-(self.button_dim[0]/2)
            rect_jouer = pygame.Rect(self.button_posX, 275, self.button_dim[0], 98)
            rect_notice = pygame.Rect(self.button_posX, 390, self.button_dim[0], 98)
            rect_quitter = pygame.Rect(self.button_posX, 510, self.button_dim[0], 98)

            # Animations quand souris passe sur les boutons
            # Bouton Jouer
            if not rect_jouer.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.box_idle, (self.button_posX, 275))
                self.window_surface.blit(Jouer, (550, 300))
            else:
                self.window_surface.blit(self.box_idle, (self.button_posX, 285))
                self.window_surface.blit(Jouer, (550, 310))

             #Bouton Notice
            if not rect_notice.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.box_idle, (self.button_posX, 390))
                self.window_surface.blit(Level, (550, 420))
            else:
                self.window_surface.blit(self.box_idle, (self.button_posX, 400))
                self.window_surface.blit(Level, (550, 430))

            # Bouton Quitter
            if not rect_quitter.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.box_idle, (self.button_posX, 510))
                self.window_surface.blit(Quitter, (540, 540))
            else:
                self.window_surface.blit(self.box_idle, (self.button_posX, 520))
                self.window_surface.blit(Quitter, (540, 550))

            pygame.display.flip()

            for event in pygame.event.get():
                # Quitter
                if event.type == pygame.QUIT:
                    self.run_notice = False
                    pygame.quit()

                # Evenements lors du clique
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si clique sur bouton Jouer
                    if rect_jouer.collidepoint((mouseX,mouseY)):
                        # Lancer l'ecran
                        self.run_menu = False
                        self.run_simulation = True
                        self.simulation()
                    
                    if rect_notice.collidepoint((mouseX,mouseY)):
                        # Lancer l'ecran
                        self.run_menu = False
                        self.run_notice = True
                        self.Notice()

                    # Si clique sur bouton Quitter
                    if rect_quitter.collidepoint((mouseX,mouseY)):
                        sys.exit()

    def Notice(self):
        text = "Notice d'utilisation de la simulation à NCorps\n 1. Paramétrage :\n - Nombre de boules :"

        # Fonction pour afficher zone de texte
        def display_text(surface, text, pos, font, color):
            collection = [word.split(' ') for word in text.splitlines()]
            space = font.size(' ')[0]
            x,y = pos
            for lines in collection:
                for words in lines:
                    word_surface = font.render(words, True, color)
                    word_width, word_height = word_surface.get_size()
                    if x + word_width >= self.width:
                        x = pos[0]
                        y += word_height
                    surface.blit(word_surface, (x,y))
                    x += word_width + space
                x = pos[0]
                y += word_height
        
        while self.run_notice:
            # Quitter
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_notice = False
                    pygame.quit()

            self.window_surface.blit(self.background, (0, 0))
            display_text(self.window_surface, text, (50,50), self.my_font, 'black')
            pygame.display.flip()

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
