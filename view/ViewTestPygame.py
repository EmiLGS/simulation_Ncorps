
import time
import pygame, sys
import csv

from time import sleep
from decimal import Decimal
from tkinter import filedialog
from controller.BodySimulationController import BodySimulationController
from model.ThreeBodiesSimulation import ThreeBodiesSimulation
from model.TwoBodiesSimulation import TwoBodiesSimulation
from model.MoreBodiesSimulation import  MoreBodiesSimulation
from model.ImportBodiesSimulation import *

class ViewTestPygame():
    def __init__(self):
        pygame.init()

        # Fonts
        pygame.font.init()
        self.poppins_font_15 = pygame.font.Font("assets/font/Poppins-regular.ttf", 15)
        self.poppins_font_30 = pygame.font.Font("assets/font/Poppins-regular.ttf", 30)
        self.poppins_font_35 = pygame.font.Font("assets/font/Poppins-regular.ttf", 35)
        self.poppins_font_80 = pygame.font.Font("assets/font/Poppins-regular.ttf", 80)
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
        #(380,98)
        self.button_dim = (456,118)
        self.box_idle = pygame.transform.scale(pygame.image.load("./assets/picture/button.jpg"),(self.button_dim[0],self.button_dim[1]))
        self.box_pressed = pygame.transform.scale(pygame.image.load("./assets/picture/button_down.jpg"),(self.button_dim[0], self.button_dim[1]))

        n = 11
        self.icon_play = pygame.transform.scale(pygame.image.load("./assets/picture/bouton-jouer.png"),(512//n,512//n))
        self.icon_notice = pygame.transform.scale(pygame.image.load("./assets/picture/livre.png"),(512//n,512//n))
        self.icon_exit = pygame.transform.scale(pygame.image.load("./assets/picture/se-deconnecter2.png"),(512//n,512//n))

    def menu(self):

        while self.run_menu:
            # Get mouse position
            mouseX, mouseY = pygame.mouse.get_pos()

            # Display the text
            self.window_surface.blit(self.background,(0,0))

            # Collision areas
            button_posX = (self.width/2)-(self.button_dim[0]/2)
            button_posY = 225
            decalage_Y = 150
            rect_jouer = pygame.Rect(button_posX, button_posY, self.button_dim[0], self.button_dim[1])
            rect_notice = pygame.Rect(button_posX, button_posY + decalage_Y, self.button_dim[0], self.button_dim[1])
            rect_quitter = pygame.Rect(button_posX, button_posY + decalage_Y*2, self.button_dim[0], self.button_dim[1])

            self.display_text(self.window_surface, 'N-Corps', (450,50), self.poppins_font_80, '#007AB5')
           
            # Animation when mouse hover button
            # Play button 
            if not rect_jouer.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.box_idle, (button_posX, button_posY))   
            else:
                self.window_surface.blit(self.box_pressed, (button_posX, button_posY))
                
            # Notice button
            if not rect_notice.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.box_idle, (button_posX, button_posY + decalage_Y))
            else:
                self.window_surface.blit(self.box_pressed, (button_posX, button_posY + decalage_Y))
                
            # Quit Button
            if not rect_quitter.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.box_idle, (button_posX, button_posY + decalage_Y*2))
            else:
                self.window_surface.blit(self.box_pressed, (button_posX, button_posY + decalage_Y*2))
            
            # Draw icons
            self.window_surface.blit(self.icon_play, (button_posX + 45, button_posY + 35))
            self.window_surface.blit(self.icon_notice, (button_posX + 45, button_posY + decalage_Y + 35))
            self.window_surface.blit(self.icon_exit, (button_posX + 45, button_posY + decalage_Y*2 + 35))

            # Draw Buttons texts
            self.display_text(self.window_surface, 'Jouer', (600, button_posY + 35), self.poppins_font_35, '#007AB5')
            self.display_text(self.window_surface, 'Notice', (600, button_posY + decalage_Y + 35), self.poppins_font_35, '#007AB5')
            self.display_text(self.window_surface, 'Quitter', (595, button_posY + decalage_Y*2 + 35), self.poppins_font_35, '#007AB5')

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
        text = ("Enoncé : \n" + 
                "Le problème à N corps est un problème de mécanique newtonienne où plusieurs corps se déplacent dans l'espace en étant soumis à leur propre inertie et l'attraction des autres corps.\n" +
                "Paramètres : \n" +
                "- Nombres d'objets \n" +
                "- Masses minimums et maximums \n")
        
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

    def simulation(self, file=None, nbBodies = 50, mass = (5.9722*10**24) ):
        # Use simControllerulation specific.
        sim = None
        if file == None:
            sim = MoreBodiesSimulation(nbBodies, mass,self.width, self.height)
        else:
            sim = ImportBodiesSimulation(file, len(file))

        while self.run_simulation:

            # Get mouse position
            mouseX, mouseY = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_simulation = False
                    pygame.quit()
                
                # Evenements lors du clique
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si clique sur bouton Retour
                    if self.rect_return.collidepoint((mouseX,mouseY)):
                        # Lancer l'ecran
                        self.run_configurator = True
                        self.run_simulation = False
                        self.configuration()

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
        color_active = pygame.Color(180, 180, 180)
        color_passive = pygame.Color(230, 230, 230)
        color1 = color_passive
        color2 = color_passive

        # Input Value
        input_number = '50'
        input_mass = '5.9722*10**24'

        self.button_posX = (self.width/2)-(self.button_dim[0]/2)

        # Launch simulation
        self.rect_jouer = pygame.Rect(self.width//3.5, 700, 1000, 100)

        # rectangle Input
        self.rect_input = pygame.Rect(400,200,300,40)
        self.rect_input_outline = pygame.Rect(395,195,310,50)
        self.rect_mass = pygame.Rect(400,400,300,40)
        self.rect_mass_outline = pygame.Rect(395,395,310,50)
        self.rect_import = pygame.Rect(self.button_posX,525,456,118)

        file = None

        while self.run_configurator:
            self.window_surface.blit(self.background, (0, 0))
            
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
                            #! RAJOUTER UNE FONCTION DE TEST DES VALEURS (INTERVALLES, COHéRENCE ETC)
                            if(file == None):
                                self.simulation(nbBodies = int(input_number), mass = self.bodyMass(input_mass))
                            else:
                                self.simulation(file, nbBodies = int(input_number), mass = self.bodyMass(input_mass))
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
                    if self.rect_import.collidepoint((mouseX, mouseY)):
                        self.window_surface.blit(self.box_pressed, (self.button_posX,525))
                        file = filedialog.askopenfilename(initialdir="D:/Université/L3/S6/Projet 2/simulation_ncorps_yega/data", title ="selectionner", filetypes=(("Fichier CSV","*.csv"),("Fichier PDF","*.pdf")))
                        file = self.getBodyFromCSV(file)
                        for i in range(len(file)):
                            print(file[i][0])
                        
                if event.type == pygame.KEYDOWN:
                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:
                        # get text input from 0 to -1 i.e. end.
                        if(active_nb):
                            input_number = input_number[:-1]
                        else:
                            input_mass = input_mass[:-1]

                    # Unicode standard is used for string
                    # formation
                    else:
                        if(active_nb):       
                            input_number += event.unicode
                        else:
                            input_mass += event.unicode

            # Draw import butotn
            self.window_surface.blit(self.box_idle, ((self.button_posX,525)))

            # Draw icon return
            self.window_surface.blit(self.icon_return, ((1200-self.taille_return_icon-25, 800-self.taille_return_icon-25)))

            # Draw play
            self.window_surface.blit(self.icon_play, ( self.width//1.8, 700 ))
            self.display_text(self.window_surface, "Lancer la simulation", (self.width//3.3,700), self.poppins_font_30, '#007AB5')

            # Display text on inputs
            self.display_text(self.window_surface,"Nombre de corps ? (2 - 100)", (400,150),self.poppins_font_30,'#007AB5')
            self.display_text(self.window_surface,"Masse des corps ? (x * (10**11 - 10**24) )", (400,350),self.poppins_font_30,'#007AB5')
            self.display_text(self.window_surface, "Import", (self.button_posX + 225, 560), self.poppins_font_35, '#007AB5')

            # Draw the rectangle
            pygame.draw.rect( self.window_surface,"#007AB5", self.rect_input_outline)
            pygame.draw.rect( self.window_surface, color1, self.rect_input)
            pygame.draw.rect( self.window_surface, "#007AB5", self.rect_mass_outline)
            pygame.draw.rect( self.window_surface, color2, self.rect_mass)

            # Apply text surface
            self.display_text(self.window_surface, input_number, (self.rect_input.x, self.rect_input.y), self.poppins_font_30, 'black')
            self.display_text(self.window_surface, input_mass, (self.rect_mass.x, self.rect_mass.y), self.poppins_font_30, 'black')
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
    
    def getBodyFromCSV(self, file):
        tab = []
        row_count = 0
        with open(file, 'r') as f:
            # Créer un objet csv à partir du fichier
            obj = csv.reader(f)
            row_count = sum(1 for row in obj)
            tab = [0] * (row_count-1)

        with open(file, 'r') as f:
            # Créer un objet csv à partir du fichier
            obj = csv.reader(f)
            i = -1
            for ligne in obj:
                if(i != -1):
                    tab[i] = ligne
                i += 1
        return tab
    
    # FUnction to return the correct float of the input mass field
    def bodyMass(self,mass_val):
        res = ''
        res2 = ''
        i = 0
        j = -1
        while (mass_val[i]) in ['1','2','3','4','5','6','7','8','9','.']:
            res += mass_val[i]
            i+=1
        while mass_val[j] != '*':
            res2 = mass_val[j] + res2
            j -= 1
        return float(res) * 10 ** int(res2)
