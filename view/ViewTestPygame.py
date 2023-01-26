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
        self.poppins_font_30 = pygame.font.Font("view/assets/Poppins-regular.ttf", 30)
        pygame.font.get_fonts()

        # Parametre de la fenetre
        self.width = 1200
        self.height = 800

        pygame.display.set_caption('Ncorps')
        self.window_surface = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface((1200, 800))
        self.background.fill(pygame.Color('#E6E6E6'))

        # Boucles pour les ecrans
        self.run_menu = True
        self.run_simulation = False
        self.run_notice = False
        self.run_configurator = False

        self.taille_return_icon = 512//11
        self.rect_return = pygame.Rect(1200-self.taille_return_icon-25, 800-self.taille_return_icon-25, self.taille_return_icon, self.taille_return_icon)
        self.icon_return = pygame.transform.scale(pygame.image.load("view/assets/return.png"),(self.taille_return_icon,self.taille_return_icon))

        # Charger les images
        self.button_dim = (380,98)
        self.box_idle = pygame.transform.scale(pygame.image.load("view/assets/button.jpg"),(self.button_dim[0],self.button_dim[1]))
        self.box_pressed = pygame.transform.scale(pygame.image.load("view/assets/button_down.jpg"),(self.button_dim[0], self.button_dim[1]))

    def menu(self):

        # Différentes écritures
        Jouer = self.poppins_font_30.render('Simuler', True, "#007AB5")
        Level = self.poppins_font_30.render('Notice', True, "#007AB5")
        Quitter = self.poppins_font_30.render('Quitter', True, "#007AB5")

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

            # Icones boutons
            n = 11
            self.icon_play = pygame.transform.scale(pygame.image.load("view/assets/bouton-jouer.png"),(512//n,512//n))
            self.icon_notice = pygame.transform.scale(pygame.image.load("view/assets/livre.png"),(512//n,512//n))
            self.icon_exit = pygame.transform.scale(pygame.image.load("view/assets/se-deconnecter2.png"),(512//n,512//n))
           
            # Animations quand souris passe sur les boutons
            # Bouton Lancer simulation
            if not rect_jouer.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.box_idle, (self.button_posX, 275))
                self.window_surface.blit(Jouer, (600, 300))
                self.window_surface.blit(self.icon_play, (self.button_posX + 35, 275 + 25))
            else:
                self.window_surface.blit(self.box_pressed, (self.button_posX, 275))
                self.window_surface.blit(Jouer, (600, 300))
                self.window_surface.blit(self.icon_play, (self.button_posX + 35, 275 + 25))

            # Bouton Notice
            if not rect_notice.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.box_idle, (self.button_posX, 390))
                self.window_surface.blit(Level, (600, 420))
                self.window_surface.blit(self.icon_notice, (self.button_posX + 35, 390 + 25))
            else:
                self.window_surface.blit(self.box_pressed, (self.button_posX, 390))
                self.window_surface.blit(Level, (600, 420))
                self.window_surface.blit(self.icon_notice, (self.button_posX + 35, 390 + 25))

            # Bouton Quitter
            if not rect_quitter.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.box_idle, (self.button_posX, 510))
                self.window_surface.blit(Quitter, (585, 540))
                self.window_surface.blit(self.icon_exit, (self.button_posX + 35, 510 + 25))
            else:
                self.window_surface.blit(self.box_pressed, (self.button_posX, 510))
                self.window_surface.blit(Quitter, (585, 540))
                self.window_surface.blit(self.icon_exit, (self.button_posX + 35, 510 + 25))

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
                        self.run_configurator = True
                        self.configurator()
                    
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
            mouseX, mouseY = pygame.mouse.get_pos()

            # Quitter
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_notice = False
                    pygame.quit()
                
                # Evenements lors du clique
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si clique sur bouton Jouer
                    if self.rect_return.collidepoint((mouseX,mouseY)):
                        # Lancer l'ecran
                        self.run_menu = True
                        self.run_notice = False
                        self.menu()

            self.window_surface.blit(self.background, (0, 0))
            display_text(self.window_surface, text, (50,50), self.poppins_font_30, 'black')
            self.window_surface.blit(self.icon_return, ((1200-self.taille_return_icon-25, 800-self.taille_return_icon-25)))
            pygame.display.flip()

    def simulation(self):
        # Use simControllerulation specific.
        simController = BodySimulationController(TwoBodiesSimulation())
        body1 = simController.getFirstBody()
        body2 = simController.getSecondBody()
        while self.run_simulation:
            mouseX, mouseY = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_simulation = False
                
                # Evenements lors du clique
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si clique sur bouton Jouer
                    if self.rect_return.collidepoint((mouseX,mouseY)):
                        # Lancer l'ecran
                        self.run_menu = True
                        self.run_simulation = False
                        self.menu()

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

            self.window_surface.blit(self.icon_return, ((1200-self.taille_return_icon-25, 800-self.taille_return_icon-25)))
            pygame.display.update()

    def configurator(self):
        while self.run_configurator:
            # Récuperer positions de la souris
            mouseX, mouseY = pygame.mouse.get_pos()

            self.window_surface.blit(self.background,(0,0))
            
            # Play icon
            self.rect_play = pygame.Rect(120, 150, self.button_dim[0], 98)
            # Zones d'interactions si souris passe sur les boutons
            self.icon_play = pygame.transform.scale(pygame.image.load("view/assets/bouton-jouer.png"),(512//11,512//11))
            rect_return = pygame.Rect(120, 150, self.button_dim[0], 98)
            
            # If play or leave button pushed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_configurator = False
                    pygame.quit()
                
                # Click changement
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If play button pressed
                    if self.rect_return.collidepoint((mouseX,mouseY)):
                        # change view
                        self.run_configurator = False
                        self.run_menu = True
                        self.menu()

                    # If play button clicked in configurator
                    if self.rect_play.collidepoint((mouseX,mouseY)):
                        # change view
                        self.run_configurator = False
                        self.run_simulation = True
                        self.simulation()
                
                pygame.display.flip()

