
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
        self.poppins_font_30 = pygame.font.Font("assets/font/Poppins-regular.ttf", 30)
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
        self.run_configurator = True

        # Icons
        self.taille_return_icon = 512//11
        self.rect_return = pygame.Rect(1200-self.taille_return_icon-25, 800-self.taille_return_icon-25, self.taille_return_icon, self.taille_return_icon)
        self.icon_return = pygame.transform.scale(pygame.image.load("./assets/picture/return.png"),(self.taille_return_icon,self.taille_return_icon))

        self.button_dim = (380,98)
        self.box_idle = pygame.transform.scale(pygame.image.load("./assets/picture/button.jpg"),(self.button_dim[0],self.button_dim[1]))
        self.box_pressed = pygame.transform.scale(pygame.image.load("./assets/picture/button_down.jpg"),(self.button_dim[0], self.button_dim[1]))

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
            self.icon_play = pygame.transform.scale(pygame.image.load("./assets/picture/bouton-jouer.png"),(512//n,512//n))
            self.icon_notice = pygame.transform.scale(pygame.image.load("./assets/picture/livre.png"),(512//n,512//n))
            self.icon_exit = pygame.transform.scale(pygame.image.load("./assets/picture/se-deconnecter2.png"),(512//n,512//n))
           
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
                        self.run_configurator = True
                        self.configuration()
                    
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
        text = "Notice d'utilisation de la simulation à NCorps\n 1. Paramétrage :\n - Nombre de boules :"
        
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

            self.window_surface.blit(self.background, (0, 0))
            self.display_text(self.window_surface, text, (50,50), self.poppins_font_30, 'black')
            self.window_surface.blit(self.icon_return, ((1200-self.taille_return_icon-25, 800-self.taille_return_icon-25)))
            pygame.display.flip()

    def simulation(self, nbBodies = 50, mass = 10**11):
        # Use simControllerulation specific.
        sim = MoreBodiesSimulation(nbBodies, self.width, self.height)

        while self.run_simulation:

            # Get mouse position
            mouseX, mouseY = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_simulation = False
                    pygame.quit()
                
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

    def configuration(self):
        active_nb = False
        active_mass = False
        can_run = False
        color_active = pygame.Color( 180, 180, 180 )
        color_passive = pygame.Color( 230, 230, 230 )
        color1 = color_passive
        color2 = color_passive

        # Input Value
        input_number = ''
        input_mass = ''

        # Launch simulation
        n = 11
        play_txt = "Jouer la simulation"
        self.icon_play = pygame.transform.scale(pygame.image.load("./assets/picture/bouton-jouer.png"),(512//n,512//n))
        self.rect_jouer = pygame.Rect(self.width//3.5, 700, 1000, 100)

        # rectangle Input
        self.rect_input = pygame.Rect(400,200,300,30)
        self.rect_input_outline = pygame.Rect(395,195,310,40)
        self.rect_mass = pygame.Rect(400,400,300,30)
        self.rect_mass_outline = pygame.Rect(395,395,310,40)

        # Font of input string
        font = pygame.font.Font(None, 30)
        text_surface1 = font.render(input_number, True, (0, 0, 0))
        text_surface2 = font.render(input_mass, True, (0, 0, 0))

        while self.run_configurator:
            self.window_surface.blit(self.background, (0, 0))
            self.button_posX = (self.width/2)-(self.button_dim[0]/2)
            # Get mouse position
            mouseX, mouseY = pygame.mouse.get_pos()

            # Check if parameters have been given
            if(input_number != '' and input_mass != ''):
                can_run = True
            else:
                can_run = False

            # Check state input
            if(active_nb):
                color1 = color_active
            else:
                color1 = color_passive
            
            if(active_mass):
                color2 = color_active
            else:
                color2 = color_passive
            
            # EVENT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_configurator = False
                    pygame.quit()
                # CLICK EVENT
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect_return.collidepoint((mouseX,mouseY)):
                        self.run_menu = True
                        self.run_configurator = False
                        self.menu()
                    # start simulation button
                    if self.rect_jouer.collidepoint((mouseX,mouseY)):
                        if(can_run):
                            self.run_simulation = True
                            self.run_configurator = False
                            self.simulation(nbBodies=int(input_number),mass=input_mass)
                    #collide nb corps input
                    if self.rect_input.collidepoint((mouseX,mouseY)):
                        if(active_mass == True):
                            active_mass = not active_mass
                        active_nb = not active_nb      
                    #Collide mass input
                    if self.rect_mass.collidepoint((mouseX,mouseY)):
                        if(active_nb == True):
                            active_nb = not active_nb
                        active_mass = not active_mass
                if event.type == pygame.KEYDOWN:
                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:
                        # get text input from 0 to -1 i.e. end.
                        if(active_nb):
                            input_number = input_number[:-1]
                            text_surface1 = font.render(input_number, True, (0, 0, 0))
                        else:
                            input_mass = input_mass[:-1]
                            text_surface2 = font.render(input_mass, True, (0, 0, 0))
                    # Unicode standard is used for string
                    # formation
                    else:
                        if(active_nb):       
                            input_number += event.unicode
                            text_surface1 = font.render(input_number, True, (0, 0, 0))
                        else:
                            input_mass += event.unicode
                            text_surface2 = font.render(input_mass, True, (0, 0, 0))

            # Draw icon return
            self.window_surface.blit(self.icon_return, ((1200-self.taille_return_icon-25, 800-self.taille_return_icon-25)))

            # Draw play
            self.window_surface.blit(self.icon_play, ( self.width//1.8, 700 ))
            self.display_text(self.window_surface, play_txt, (self.width//3.2,700), self.poppins_font_30, 'black')

            # Display text on inputs
            self.display_text(self.window_surface,"Nombre de corps ?", (400,150),self.poppins_font_30,'black')
            self.display_text(self.window_surface,"Masse des corps ?", (400,350),self.poppins_font_30,'black')
            
            # Draw the rectangle
            pygame.draw.rect( self.window_surface,"black", self.rect_input_outline )
            pygame.draw.rect( self.window_surface, color1, self.rect_input )
            pygame.draw.rect( self.window_surface, "black", self.rect_mass_outline )
            pygame.draw.rect( self.window_surface, color2, self.rect_mass )
            
            # Apply text surface
            self.window_surface.blit(text_surface1, ( self.rect_input.x, self.rect_input.y ) )
            self.window_surface.blit(text_surface2, ( self.rect_mass.x, self.rect_mass.y ) )
            # Update the screen
            pygame.display.update()

        # Display text
    def display_text(self, surface, text, pos, font, color):
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
