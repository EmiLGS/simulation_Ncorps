
import time
import pygame, sys

from time import sleep
from controller.BodySimulationController import BodySimulationController
from model.ThreeBodiesSimulation import ThreeBodiesSimulation
from model.TwoBodiesSimulation import TwoBodiesSimulation
from model.MoreBodiesSimulation import  MoreBodiesSimulation
import numpy as np

class ViewTestPygame():
    def __init__(self):
        pygame.init()

        # Fonts
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.poppins_font_30 = pygame.font.Font("view/Poppins-regular.ttf", 30)
        pygame.font.get_fonts()

        # Windows parameters
        self.width = 1200
        self.height = 800

        pygame.display.set_caption('Ncorps')
        self.window_surface = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface((1200, 800))
        self.background.fill(pygame.Color('#E6E6E6'))

        # Screens loops
        self.run_menu = True
        self.run_simulation = False
        self.run_notice = False

        # Icons
        self.taille_return_icon = 512//11
        self.rect_return = pygame.Rect(1200-self.taille_return_icon-25, 800-self.taille_return_icon-25, self.taille_return_icon, self.taille_return_icon)
        self.icon_return = pygame.transform.scale(pygame.image.load("./Images/return.png"),(self.taille_return_icon,self.taille_return_icon))

        self.button_dim = (380,98)
        self.box_idle = pygame.transform.scale(pygame.image.load("./Images/button.jpg"),(self.button_dim[0],self.button_dim[1]))
        self.box_pressed = pygame.transform.scale(pygame.image.load("./Images/button_down.jpg"),(self.button_dim[0], self.button_dim[1]))

        # sim = ThreeBodiesSimulation()
        # sim = TwoBodiesSimulation()
        

    def menu(self):

        # Fonts for text buttons
        Jouer = self.poppins_font_30.render('Jouer', True, "#007AB5")
        Level= self.poppins_font_30.render('Notice', True, "#007AB5")
        Quitter = self.poppins_font_30.render('Quitter', True, "#007AB5")

        while self.run_menu:
            # Get mouse position
            mouseX, mouseY = pygame.mouse.get_pos()

            # Display the text
            self.window_surface.blit(self.background,(0,0))

            # Collision areas
            self.button_posX = (self.width/2)-(self.button_dim[0]/2)
            rect_jouer = pygame.Rect(self.button_posX, 275, self.button_dim[0], 98)
            rect_notice = pygame.Rect(self.button_posX, 390, self.button_dim[0], 98)
            rect_quitter = pygame.Rect(self.button_posX, 510, self.button_dim[0], 98)

            # Icon buttons
            n = 11
            self.icon_play = pygame.transform.scale(pygame.image.load("./Images/bouton-jouer.png"),(512//n,512//n))
            self.icon_notice = pygame.transform.scale(pygame.image.load("./Images/livre.png"),(512//n,512//n))
            self.icon_exit = pygame.transform.scale(pygame.image.load("./Images/se-deconnecter2.png"),(512//n,512//n))
           
            # Animation when mouse hover button
            # Play button 
            if not rect_jouer.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.box_idle, (self.button_posX, 275))
                self.window_surface.blit(Jouer, (600, 300))
                self.window_surface.blit(self.icon_play, (self.button_posX + 35, 275 + 25))
            else:
                self.window_surface.blit(self.box_pressed, (self.button_posX, 275))
                self.window_surface.blit(Jouer, (600, 300))
                self.window_surface.blit(self.icon_play, (self.button_posX + 35, 275 + 25))

            # Notice button
            if not rect_notice.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.box_idle, (self.button_posX, 390))
                self.window_surface.blit(Level, (600, 420))
                self.window_surface.blit(self.icon_notice, (self.button_posX + 35, 390 + 25))
            else:
                self.window_surface.blit(self.box_pressed, (self.button_posX, 390))
                self.window_surface.blit(Level, (600, 420))
                self.window_surface.blit(self.icon_notice, (self.button_posX + 35, 390 + 25))

            # Quit Button
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
                # Exit
                if event.type == pygame.QUIT:
                    self.run_notice = False
                    pygame.quit()

                # Event when click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Click on Play
                    if rect_jouer.collidepoint((mouseX,mouseY)):
                        # Run the screen
                        self.run_menu = False
                        self.run_simulation = True
                        self.simulation()
                    
                    # Click on Notice
                    if rect_notice.collidepoint((mouseX,mouseY)):
                        # Run the screen
                        self.run_menu = False
                        self.run_notice = True
                        self.Notice()

                    # Click on Quit
                    if rect_quitter.collidepoint((mouseX,mouseY)):
                        sys.exit()

    def Notice(self):
        text = ("Enoncé : \n" + 
                "Le problème à N corps est un problème de mécanique newtonienne où plusieurs corps se déplacent dans l'espace en étant soumis à leur propre inertie et l'attraction des autres corps.\n" +
                "Paramètres : \n" +
                "- Nombres d'objets \n"
                "- Masses minimums et maximums")

        # Display text
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
            # Get mouse position
            mouseX, mouseY = pygame.mouse.get_pos()

            for event in pygame.event.get():
                # Exit
                if event.type == pygame.QUIT:
                    self.run_notice = False
                    pygame.quit()
                
                # Events when click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Click on Play
                    if self.rect_return.collidepoint((mouseX,mouseY)):
                        # Run the screen
                        self.run_menu = True
                        self.run_notice = False
                        self.menu()

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
        # pygame.draw.polygon(window_surface, (0, 0, 0), ((x1+5, y1), (x1+ax1, y1+ay1), (x1-5,y1)))
        
        

            self.window_surface.blit(self.background, (0, 0))
            display_text(self.window_surface, text, (50,50), self.poppins_font_30, 'black')
            self.window_surface.blit(self.icon_return, ((1200-self.taille_return_icon-25, 800-self.taille_return_icon-25)))
            pygame.display.flip()

    def simulation(self):
        # Use simControllerulation specific.
        sim = MoreBodiesSimulation(50, self.width, self.height)

        while self.run_simulation:

            # Get mouse position
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

            for body in sim.bodies:
                pygame.draw.circle(self.window_surface,(0,0,0),(body.pos[0],body.pos[1]),5)
            sim.advance()

            self.window_surface.blit(self.icon_return, ((1200-self.taille_return_icon-25, 800-self.taille_return_icon-25)))
            pygame.display.update()

# Pygame check event and updating screen.
