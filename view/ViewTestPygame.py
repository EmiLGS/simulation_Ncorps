
import time
import pygame, sys
import csv

from time import sleep
from decimal import Decimal
from tkinter import filedialog
from controller.BodySimulationController import BodySimulationController
from controller.VerifyController import VerifyController
from model.ThreeBodiesSimulation import ThreeBodiesSimulation
from model.TwoBodiesSimulation import TwoBodiesSimulation
from model.MoreBodiesSimulation import  MoreBodiesSimulation
from model.ImportBodiesSimulation import *
from vendor.chart.FramePerTimeChart import FramePerTimeChart

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

        # Controller
        print(VerifyController((self.width, self.height)).verifyNb(1))


        pygame.display.set_caption('Ncorps')
        self.window_surface = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface((1200, 800))
        self.background.fill(pygame.Color('#E6E6E6'))

        # Screens loops
        self.run_menu = True
        self.run_simulation = False
        self.run_notice = False
        self.run_configurator = False 
        self.run_statistic = False

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
        # NEXT
        self.icon_next = pygame.transform.scale(pygame.image.load("./assets/picture/next.png"),(512//n,512//n))
        self.rect_next = pygame.Rect(self.taille_return_icon, 800-self.taille_return_icon-25, self.taille_return_icon, self.taille_return_icon)
        
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
           
            # Animation when mouse hover a button
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
            

            # Draw title
            self.display_text(self.window_surface, 'N-Corps', (450,50), self.poppins_font_80, '#007AB5')

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
                    sys.exit()

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
                "Configuration : \n" +
                "- Nombres de corps \n" +
                "- Masses minimums et maximums \n" +
                "- Import : vous pouvez importer directement des corps avec des caractéristiques précises par le biais d'un tableau excel. Pour ce faire il vous suffit de télécharger le modèle de fichier excel fournit sur le menu de configuration, le remplir avec vos informations puis le fournir en cliquant sur le bouton import.")

        while self.run_notice:
            # Get mouse position
            mouseX, mouseY = pygame.mouse.get_pos()

            for event in pygame.event.get():
                # Exit
                if event.type == pygame.QUIT:
                    self.run_notice = False
                    pygame.quit()
                    sys.exit()
                
                # Events when click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Click on Play
                    if self.rect_return.collidepoint((mouseX,mouseY)):
                        # Run the screen
                        self.run_menu = True
                        self.run_notice = False
                        self.menu()

            # Draw background
            self.window_surface.blit(self.background, (0, 0))

            # Draw text
            self.display_text(self.window_surface, text, (50,50), self.poppins_font_30, 'black')

            # Draw icon return
            self.window_surface.blit(self.icon_return, ((1200-self.taille_return_icon-25, 800-self.taille_return_icon-25)))
            pygame.display.flip()

    def simulation(self, file=None, nbBodies = 50, mass = (5.9722*10**24) ):
        # Use a specific simulation
        sim = None
        if file == None:
            sim = MoreBodiesSimulation(nbBodies, mass,self.width, self.height)
        else:
            sim = ImportBodiesSimulation(file, len(file))

        cmpt = 0
        data = [[],[]]
        initTime = time.time()
        while self.run_simulation:
            # Get mouse position
            cmpt += 1
            # if cmpt % 20 == 0 :
                # print(cmpt, time.time() - initTime)
            data[0].append( round(time.time() - initTime, 3) )
            data[1].append(cmpt)
            mouseX, mouseY = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_simulation = False
                    pygame.quit()
                    sys.exit()
                
                # Evenements lors du clique
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si clique sur bouton Retour
                    if cmpt > 200 :
                        if self.rect_return.collidepoint((mouseX,mouseY)):
                            finishTime = time.time() - initTime
                            print(f"Il y a eu {cmpt} Frame en {round(finishTime,3)} seconde(s)")
                            self.run_statistic = True
                            self.run_simulation = False
                            self.statistic(data)

                    if self.rect_next.collidepoint((mouseX,mouseY)):
                        # Lancer l'ecran
                        self.run_configurator = True
                        self.run_simulation = False
                        self.configuration()

            # Draw background
            self.window_surface.blit(self.background, (0, 0))

            # Draw bodies
            for body in sim.bodies:
                pygame.draw.circle(self.window_surface,(0,0,0),(body.pos[0],body.pos[1]), self.convertMassForDisplay(body.mass))
            sim.advance()

            self.window_surface.blit(self.icon_return, ((self.taille_return_icon, 800-self.taille_return_icon-25)))
            if cmpt > 200 :
                self.window_surface.blit(self.icon_next, ((1200-self.taille_return_icon-25, 800-self.taille_return_icon-25)))
            pygame.display.update()
    
    def statistic(self,data):
        # Define here Chart from vendor\Chart
        # FramePerTimeChart
        FPT = FramePerTimeChart(data[0],data[1])
        printFPT = FPT.printChart()
        FPTraw_data = printFPT[0]
        FPTcanvas = printFPT[1]
        # END FramePerTimeChart
        # END CHART
        while self.run_statistic:
            # Get mouse position
            mouseX, mouseY = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_statistic = False
                    pygame.quit()

                # Evenements lors du clique
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si clique sur bouton Retour
                    if self.rect_next.collidepoint((mouseX,mouseY)):
                        self.run_menu = True
                        self.run_statistic = False
                        self.menu()
            self.window_surface.blit(self.background, (0, 0))
            self.window_surface.blit(self.icon_return, ((self.taille_return_icon, 800-self.taille_return_icon-25)))
            # PRINT FPT
            FPTsize = FPTcanvas.get_width_height()
            FPTsurf = pygame.image.fromstring(FPTraw_data, FPTsize, "RGB")
            self.window_surface.blit(FPTsurf, (20,20))
            # Display title
            self.display_text(self.window_surface, 'Statistic', (self.width//2 - 150, -20), self.poppins_font_80, '#007AB5')
            # END PRINT FPT
            pygame.display.update()

    def configuration(self):
        # Variables
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

        # Rectangles for collisions
        rect_jouer = pygame.Rect(self.width//3.5, 700, 1000, 100)
        rect_input = pygame.Rect(400,200,300,40)
        rect_input_outline = pygame.Rect(395,195,310,50)
        rect_mass = pygame.Rect(400,400,300,40)
        rect_mass_outline = pygame.Rect(395,395,310,50)
        rect_import = pygame.Rect(self.button_posX,525,456,118)

        file = None

        while self.run_configurator:
            # Get mouse position
            mouseX, mouseY = pygame.mouse.get_pos()

            controller = VerifyController((800,1200))

            if(controller.verifyInput(input_number, input_mass) == False or controller.verifyNb(input_number) == False):
                can_run = False
            else:
                can_run = True

            # Check state input
            if(active_nb):
                color1 = color_active
            else:
                color1 = color_passive
            
            if(active_mass):
                color2 = color_active
            else:
                color2 = color_passive

            if not rect_import.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.box_idle, (self.button_posX,525))   
            else:
                self.window_surface.blit(self.box_pressed, (self.button_posX,525))
            
            # EVENT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_configurator = False
                    pygame.quit()
                    sys.exit()
                # CLICK EVENT
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Return
                    if self.rect_return.collidepoint((mouseX,mouseY)):
                        self.run_menu = True
                        self.run_configurator = False
                        self.menu()

                    # Start simulation
                    if rect_jouer.collidepoint((mouseX,mouseY)):
                        if(can_run):
                            self.run_simulation = True
                            self.run_configurator = False

                            if(file == None):
                                self.simulation(nbBodies = int(input_number), mass = self.bodyMass(input_mass))
                            else:
                                self.simulation(file, nbBodies = int(input_number), mass = self.bodyMass(input_mass))

                    # Type text input nb
                    if rect_input.collidepoint((mouseX,mouseY)):
                        if(active_mass == True):
                            active_mass = not active_mass
                        active_nb = not active_nb 

                    # Type text input mass
                    if rect_mass.collidepoint((mouseX,mouseY)):
                        if(active_nb == True):
                            active_nb = not active_nb
                        active_mass = not active_mass

                    # Import file
                    if rect_import.collidepoint((mouseX, mouseY)):
                        file = filedialog.askopenfilename(initialdir="D:/Université/L3/S6/Projet 2/simulation_ncorps_yega/data", title ="selectionner", filetypes=(("Fichier CSV","*.csv"),("Fichier PDF","*.pdf")))
                        file = self.getBodyFromCSV(file)
                        
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
                        if event.unicode.isdigit():
                            if(active_nb):       
                                input_number += event.unicode
                            else:
                                input_mass += event.unicode

            # Draw background
            self.window_surface.blit(self.background, (0, 0))

            # Draw import butotn
            self.window_surface.blit(self.box_idle, ((self.button_posX,525)))

            # Draw icon return
            self.window_surface.blit(self.icon_return, ((1200-self.taille_return_icon-25, 800-self.taille_return_icon-25)))

            # Draw play
            self.window_surface.blit(self.icon_play, ( self.width//1.8, 700 ))            

            # Display text on inputs
            self.display_text(self.window_surface, "Lancer la simulation", (self.width//3.3,700), self.poppins_font_30, '#007AB5')
            self.display_text(self.window_surface,"Nombre de corps ? (2 - 100)", (400,150),self.poppins_font_30,'#007AB5')
            self.display_text(self.window_surface,"Masse des corps ? (x * (10**11 - 10**24) )", (400,350),self.poppins_font_30,'#007AB5')
            self.display_text(self.window_surface, "Import", (self.button_posX + 225, 560), self.poppins_font_35, '#007AB5')

            # Draw the rectangles
            pygame.draw.rect(self.window_surface,"#007AB5", rect_input_outline)
            pygame.draw.rect(self.window_surface, color1, rect_input)
            pygame.draw.rect(self.window_surface, "#007AB5", rect_mass_outline)
            pygame.draw.rect(self.window_surface, color2, rect_mass)

            # Apply text surface
            self.display_text(self.window_surface, input_number, (rect_input.x, rect_input.y), self.poppins_font_30, 'black')
            self.display_text(self.window_surface, input_mass, (rect_mass.x, rect_mass.y), self.poppins_font_30, 'black')

            # Update the screen
            pygame.display.update()

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

    def convertMassForDisplay(self, mass):
        mass = mass / (10**24)
        mass = round(mass)
        return(mass)

    # Fnctioun to return the correct float of the input mass field
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
