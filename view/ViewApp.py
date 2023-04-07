
import json
import time
import pygame, sys
import math

from time import sleep
from decimal import Decimal
from tkinter import filedialog
from controller.VerifyController import VerifyController
from model.MoreBodiesSimulation import  MoreBodiesSimulation
from controller.Utilities import Utilities
from controller.JsonController import JsonController
from model.Body import Body
from vendor.Checkbox import Checkbox
from vendor.chart.FramePerTimeChart import FramePerTimeChart
from vendor.chart.PrecisionChart import PrecisionChart
from model.BarnesHutSimulation import BarnesHutSimulation
import numpy as np

class ViewTestPygame():
    def __init__(self):
        pygame.init()
        self.jsonController = JsonController("./data/statistics.json")
        self.nbSim = 0
        # Fonts
        pygame.font.init()
        self.poppins_font_15 = pygame.font.Font("assets/font/Poppins-Regular.ttf", 15)
        self.poppins_font_30 = pygame.font.Font("assets/font/Poppins-Regular.ttf", 30)
        self.poppins_font_35 = pygame.font.Font("assets/font/Poppins-Regular.ttf", 35)
        self.poppins_font_80 = pygame.font.Font("assets/font/Poppins-Regular.ttf", 80)
        pygame.font.get_fonts()

        # Windows parameters
        self.width = 1200
        self.height = 800

        self.nb_simulations = 0

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

        # Data to store
        self.numSimulations = 0
        self.nbCorps = 0
        self.algo = None
        self.temps = None
        self.precision = None

        self.data = [self.numSimulations, self.nbCorps, self.algo, self.temps, self.precision]

        self.nbInteract = 0
        self.averageInteract = 0
        
        # Buttons
        self.button_dim = (456,118)
        self.box_idle = pygame.transform.scale(pygame.image.load("./assets/picture/button.jpg"),(self.button_dim[0],self.button_dim[1]))
        self.box_pressed = pygame.transform.scale(pygame.image.load("./assets/picture/button_down.jpg"),(self.button_dim[0], self.button_dim[1]))
        self.box_idle_correct = pygame.transform.scale(pygame.image.load("./assets/picture/button_correct.jpg"),(self.button_dim[0],self.button_dim[1]))
        self.box_pressed_correct = pygame.transform.scale(pygame.image.load("./assets/picture/button_down_correct.jpg"),(self.button_dim[0],self.button_dim[1]))
        self.box_idle_incorrect = pygame.transform.scale(pygame.image.load("./assets/picture/button_incorrect.jpg"),(self.button_dim[0],self.button_dim[1]))
        self.box_pressed_incorrect = pygame.transform.scale(pygame.image.load("./assets/picture/button_down_incorrect.jpg"),(self.button_dim[0],self.button_dim[1]))
  
        # Icons
        self.icons_size = 512//11
        self.icon_return = pygame.transform.scale(pygame.image.load("./assets/picture/return.png"),(self.icons_size,self.icons_size))
        self.icon_play = pygame.transform.scale(pygame.image.load("./assets/picture/bouton-jouer.png"),(self.icons_size,self.icons_size))
        self.icon_notice = pygame.transform.scale(pygame.image.load("./assets/picture/livre.png"),(self.icons_size,self.icons_size))
        self.icon_exit = pygame.transform.scale(pygame.image.load("./assets/picture/se-deconnecter2.png"),(self.icons_size,self.icons_size))
        self.icon_import = pygame.transform.scale(pygame.image.load("./assets/picture/import.png"),(self.icons_size,self.icons_size))
        self.icon_import_correct = pygame.transform.scale(pygame.image.load("./assets/picture/import_correct.png"),(self.icons_size,self.icons_size))
        self.icon_import_incorrect = pygame.transform.scale(pygame.image.load("./assets/picture/import_incorrect.png"),(self.icons_size,self.icons_size))
        self.icon_trash = pygame.transform.scale(pygame.image.load("./assets/picture/poubelle.png"),(self.icons_size,self.icons_size))
        self.icon_next = pygame.transform.scale(pygame.image.load("./assets/picture/next.png"),(self.icons_size,self.icons_size))
        self.icon_cache = pygame.transform.scale(pygame.image.load("./assets/picture/cache.png"),(self.icons_size,self.icons_size))
        
        # Rects
        self.rect_next = pygame.Rect(self.icons_size, 800-self.icons_size-25, self.icons_size, self.icons_size)
        self.rect_return = pygame.Rect(1200-self.icons_size-25, 800-self.icons_size-25, self.icons_size, self.icons_size)

    def menu(self):
        # Reinitialize json file
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
            rect_cache = pygame.Rect(self.width-60, self.height-60, self.button_dim[0], self.button_dim[1])
            
            # Draw title
            Utilities().display_text(self.window_surface, 'N-Corps', (450,50), self.poppins_font_80, '#007AB5')

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
            # Reset statistics.json cache
            if not rect_cache.collidepoint(mouseX, mouseY):
                self.window_surface.blit(self.icon_cache, (self.width-60, self.height-60))
            else:
                self.window_surface.blit(self.icon_cache, (self.width-58, self.height-58))

            # Draw icons
            self.window_surface.blit(self.icon_play, (button_posX + 45, button_posY + 35))
            self.window_surface.blit(self.icon_notice, (button_posX + 45, button_posY + decalage_Y + 35))
            self.window_surface.blit(self.icon_exit, (button_posX + 45, button_posY + decalage_Y*2 + 35))

            # Draw Buttons texts
            Utilities().display_text(self.window_surface, 'Jouer', (600, button_posY + 35), self.poppins_font_35, '#007AB5')
            Utilities().display_text(self.window_surface, 'Notice', (600, button_posY + decalage_Y + 35), self.poppins_font_35, '#007AB5')
            Utilities().display_text(self.window_surface, 'Quitter', (595, button_posY + decalage_Y*2 + 35), self.poppins_font_35, '#007AB5')

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
                    #Click on Cache
                    if rect_cache.collidepoint((mouseX,mouseY)):
                        # Reset statistics.json
                        self.jsonController.deleteJsonFile()
                    # Click on Notice
                    if rect_notice.collidepoint((mouseX,mouseY)):
                        # Run the screen
                        self.run_menu = False
                        self.run_notice = True
                        self.Notice()

                    # Click on Quit
                    if rect_quitter.collidepoint((mouseX,mouseY)):
                        sys.exit()
            
            
            pygame.display.flip()

    def Notice(self):
        text = ("Enoncé : \n" + 
                "Le problème à N corps est un problème de mécanique newtonienne où plusieurs corps se déplacent dans l'espace en étant soumis à leur propre inertie et l'attraction des autres corps.\n" +
                "Configuration : \n" +
                "- Nombres de corps \n" +
                "- Masses minimums et maximums \n" +
                "- Algorithmes : Vous pouvez sélectionner l'algorithme désiré en cochant la checkbox correspondante. \n" +
                "- Import : vous pouvez importer directement des corps avec des caractéristiques précises par le biais d'un tableau excel. Pour ce faire il vous suffit de modifier le modèle de fichier excel fournit sur le menu de configuration, le remplir avec vos informations puis le redonner en cliquant sur le bouton import.")
        
        while self.run_notice:
            # Get mouse position
            mouseX, mouseY = pygame.mouse.get_pos()

            # Draw background
            self.window_surface.blit(self.background, (0, 0))

            # Draw text
            Utilities().display_text(self.window_surface, text, (50,50), self.poppins_font_30, 'black')

            # Draw icon return
            self.window_surface.blit(self.icon_return, ((1200-self.icons_size-25, 800-self.icons_size-25)))

            for event in pygame.event.get():
                # Exit
                if event.type == pygame.QUIT:
                    self.run_notice = False
                    pygame.quit()
                    sys.exit()
                
                # Events when click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Click on return
                    if self.rect_return.collidepoint((mouseX,mouseY)):
                        # Run the screen
                        self.run_menu = True
                        self.run_notice = False
                        self.menu()

            pygame.display.flip()

    def simulation(self, file=None, nbBodies = 50, mass_min = 6, mass_max = 12, algo="classic"):
        # Use a specific simulation
        sim = None
        precList = None
        self.algo = algo
        def importBodies(file):
            bodies = []
            for _ in range(len(file)):
                body = Body(file[_][0],file[_][1],float(file[_][2]))
                if len(file[_]) > 3:
                    body.spd = np.array([float(file[_][3]),float(file[_][4])])
                bodies.append(body)

            return bodies
        
        if file == None:
            bodies = []
        else:
            #File is simply the name of the file, the second element is the bodies over each frame (similar to dataTime), the third is the list of the bodies at the 20th frame of the simulation
            precList = [file, [[],None], None]
            bodies = importBodies(file)
            nbBodies = len(bodies)
            self.nbCorps = nbBodies

        if algo == "classic":
            sim = MoreBodiesSimulation(bodyCount=nbBodies, mass_min=mass_min, mass_max=mass_max, width=self.width, height=self.height, bodies=bodies)
        elif algo == "barnesHut":
            sim = BarnesHutSimulation(bodyCount=nbBodies,mass_min=mass_min, mass_max=mass_max, width=self.width, height=self.height, bodies=bodies)
        elif algo == "FMM":
            sim = MoreBodiesSimulation(bodyCount=nbBodies, mass_min=mass_min, mass_max=mass_max, width=self.width, height=self.height, bodies=bodies)

        cmpt = 0
        dataTime = [[],[]]
        initTime = time.time()

        while self.run_simulation:
            # Get mouse position
            cmpt += 1
            dataTime[0].append(round(time.time() - initTime, 3))
            dataTime[1].append(cmpt)
            if file != None: precList[1][0].append(tuple(sim.bodies[0].pos))
            mouseX, mouseY = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_simulation = False
                    precList[1][1] = dataTime[1]
                    self.data = [self.numSimulations, self.nbCorps, self.algo, dataTime, precList]
                    self.jsonController.storeDataJson(self.data)
                    pygame.quit()
                    sys.exit()
                
                # Events when click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Click on return
                    if cmpt > 200 :
                        if self.rect_return.collidepoint((mouseX,mouseY)):

                            # Save simulation
                            self.temps = dataTime[0]
                            if file != None : precList[1][1] = dataTime[1]
                            self.data = [self.numSimulations, self.nbCorps, self.algo, dataTime, precList]
                            self.jsonController.storeDataJson(self.data)
                            
                            self.run_statistic = True
                            self.run_simulation = False
                            self.statistic()

                    if self.rect_next.collidepoint((mouseX,mouseY)):
                        # Save simulation
                        self.temps = dataTime[0]
                        if file != None : precList[1][1] = dataTime[1]
                        self.data = [self.numSimulations, self.nbCorps, self.algo, dataTime, precList]
                        self.jsonController.storeDataJson(self.data)

                        # Run screen
                        self.run_configurator = True
                        self.run_simulation = False
                        sim = None
                        self.configuration()

            # Draw background
            self.window_surface.blit(self.background, (0, 0))

            # Get base values for min and max exponential
            mass_min_r = math.floor(math.log(sim.bodies[0].mass, 10))
            mass_max_r = math.floor(math.log(sim.bodies[0].mass, 10))
            # Values for the size in pixels of the bodies
            minp = 3
            maxp = 10

            # Get min and max exp values for all bodies
            for body in sim.bodies:
                exp = math.floor(math.log(body.mass, 10))
                if(exp < mass_min_r):
                    mass_min_r = exp
                if(exp > mass_max_r):
                    mass_max_r = exp
            
            # Draw bodies
            for body in sim.bodies:
                # if mass max equal to min max set a pixel size for all
                if mass_max_r == mass_min_r :
                    pygame.draw.circle(self.window_surface,body.getBodyColor(7),(body.pos[0],body.pos[1]), 7)
                # Scale the size of the bodies
                else :
                    nombreSortie = ((maxp - minp) / (mass_max_r - mass_min_r)) * (math.floor(math.log(body.mass, 10)) - mass_min_r) + minp
                    pygame.draw.circle(self.window_surface,body.getBodyColor(int(nombreSortie)),(body.pos[0],body.pos[1]), int(nombreSortie))

            self.window_surface.blit(self.icon_return, ((self.icons_size, 800-self.icons_size-25)))

            # Store Bodies For Precision at 20 frames
            if cmpt == 20:
                if file != None and precList[2] == None: precList[2] = tuple(map(lambda x : tuple(x.pos), sim.bodies))

            # Draw next icon
            if cmpt > 200 :
                self.window_surface.blit(self.icon_next, ((1200-self.icons_size-25, 800-self.icons_size-25)))

            sim.advance()

            self.nbInteract += sim.nbInteract
            self.averageInteract= self.nbInteract/cmpt

            pygame.display.update()
    
    def statistic(self,):
        # Load data from json file
        with open("./data/statistics.json", 'r') as file:
            data = json.load(file)
        
        # Define here Chart from vendor\Chart
        # FramePerTimeChart
        
        FPT = FramePerTimeChart(data)
        printFPT = FPT.printChart()
        FPTraw_data = printFPT[0]
        FPTcanvas = printFPT[1]

        Prec = PrecisionChart(data)
        printPrec = Prec.printChart()
        print(printPrec[1])
        if printPrec[0] == None:
            drawPrecision = False
            errMessPrec = printPrec[1]
        else:
            drawPrecision = True
            PrecRawData = printPrec[0]
            PrecCanvas = printPrec[1]
            averagePrec20 = printPrec[2]
        # END FramePerTimeChart
        # END CHART

        while self.run_statistic:
            # Get mouse position
            mouseX, mouseY = pygame.mouse.get_pos()

            self.window_surface.blit(self.background, (0, 0))
            self.window_surface.blit(self.icon_return, ((self.icons_size, 800-self.icons_size-25)))

            # PRINT FPT
            FPTsize = FPTcanvas.get_width_height()
            FPTsurf = pygame.image.fromstring(FPTraw_data, FPTsize, "RGB")
            self.window_surface.blit(FPTsurf, (20,30))

            if drawPrecision:
                PrecSize = PrecCanvas.get_width_height()
                PrecSurf = pygame.image.fromstring(PrecRawData, PrecSize, "RGB")
                self.window_surface.blit(PrecSurf, (500,30))
                Utilities().display_text(self.window_surface, "L'erreur moyenne au bout de 20 frames etait de " + str(averagePrec20), (600,500), self.poppins_font_15, '#007AB5')
            else:
                Utilities().display_text(self.window_surface, errMessPrec, (750,250), self.poppins_font_15, '#007AB5')


            # Display title
            Utilities().display_text(self.window_surface, 'Statistiques', (self.width//2 - 150, -20), self.poppins_font_80, '#007AB5')
            Utilities().display_text(self.window_surface, "La simulation contenait " + str(self.nbCorps) + " corps pour un total de " + str(self.averageInteract) + "calcul de force par frame", (100, 600 ), self.poppins_font_15, '#007AB5')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_statistic = False
                    pygame.quit()
                    sys.exit()

                # Evenements lors du clique
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si clique sur bouton Retour
                    if self.rect_next.collidepoint((mouseX,mouseY)):
                        self.run_menu = True
                        self.run_statistic = False
                        self.menu()

            pygame.display.update()

    def configuration(self):
        # Variables
        active_nb = False
        active_mass_min = False
        active_mass_max = False
        error = None
        can_run = False
        color_active = pygame.Color(180, 180, 180)
        color_passive = pygame.Color(230, 230, 230)
        color_nb = color_passive
        color_mass_min = color_passive
        color_mass_max = color_passive

        # Input Value
        input_number = '50'
        input_mass_min = '5.9722*10**6'
        input_mass_max = '5.9722*10**12'

        self.button_posX = (self.width/2)-(self.button_dim[0]/2)

        # Rectangles for collisions
        rect_jouer = pygame.Rect(self.width//3.5, 700, 1000, 100)
        rect_input = pygame.Rect(400,125,300,40)
        rect_input_outline = pygame.Rect(395,120,310,50)
        rect_mass_min = pygame.Rect(400,250,300,40)
        rect_mass_min_outline = pygame.Rect(395,245,310,50)
        rect_mass_max = pygame.Rect(400,375,300,40)
        rect_mass_max_outline = pygame.Rect(395,370,310,50)
        rect_import = pygame.Rect(self.button_posX,500,556,118)
        rect_trash = pygame.Rect(self.button_posX + self.button_dim[0] + 25, 500 + 35, self.icons_size, self.icons_size)

        file = None

        # Checkbox algorithm selector*
        # Boxe for multiple check
        boxes = []
        #checkbox
        classic = Checkbox(surface=self.window_surface,x=350,y=450,caption="Algorithme quadratique", idnum=1,font_color='#007AB5',checked=True, algo="classic")
        barnersHutt = Checkbox(surface=self.window_surface,x=570,y=450,caption="Barners Hutt", idnum=2,font_color='#007AB5', algo="barnesHut")
        FMM = Checkbox(surface=self.window_surface,x=720,y=450,caption="FMM", idnum=3,font_color='#007AB5',algo="FMM")
        #Append into the boxes
        boxes.append(classic)
        boxes.append(barnersHutt)
        boxes.append(FMM)
        
        while self.run_configurator:
            # Get mouse position
            mouseX, mouseY = pygame.mouse.get_pos()

            controller = VerifyController((800,1200))
            # Draw background
            self.window_surface.blit(self.background, (0, 0))
            #checkbox update
            for checkbox in boxes:
                checkbox.render_checkbox()
            # Verify inputs
            if(controller.verifyInput(input_number, input_mass_min, input_mass_max) == False or controller.verifyNb(input_number) == False):
                can_run = False
            else:
                can_run = True

            # Check state input
            if(active_nb):
                color_nb = color_active
                color_mass_min = color_passive
                color_mass_max = color_passive
            elif(active_mass_min):
                color_mass_min = color_active
                color_nb = color_passive
                color_mass_max = color_passive
            elif(active_mass_max):
                color_mass_max = color_active
                color_mass_min = color_passive
                color_nb = color_passive        

            # EVENT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_configurator = False
                    self.jsonController.storeDataJson(self.data)
                    pygame.quit()
                    sys.exit()
                # CLICK EVENT
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for box in boxes:
                        box.update_checkbox(event)
                        if box.checked is True:
                            for b in boxes:
                                if b != box:
                                    b.checked = False
                    # Return
                    if self.rect_return.collidepoint((mouseX,mouseY)):
                        self.run_menu = True
                        self.run_configurator = False
                        self.menu()

                    # Start simulation
                    if rect_jouer.collidepoint((mouseX,mouseY)):
                        if(can_run):
                            # Actualize data to store
                            self.numSimulations += 1
                            self.nbCorps = int(input_number)
                            self.algo = box.algo

                            self.run_simulation = True
                            self.run_configurator = False

                            if(file == None):
                                for box in boxes:
                                    if box.checked == True:
                                        self.simulation(nbBodies = int(input_number), mass_min = Utilities().bodyMassExp(input_mass_min), mass_max = Utilities().bodyMassExp(input_mass_max),algo=box.algo)
                            else:
                                for box in boxes:
                                    if box.checked == True:
                                        self.simulation(file, nbBodies = int(input_number), mass_min = Utilities().bodyMassExp(input_mass_min), mass_max = Utilities().bodyMassExp(input_mass_max), algo=box.algo)

                    # Type text input nb
                    if rect_input.collidepoint((mouseX,mouseY)):
                        if(active_mass_min == True):
                            active_mass_min = not active_mass_min
                        elif(active_mass_max == True):
                            active_mass_max = not active_mass_max
                        active_nb = not active_nb 

                    # Type text input mass_min
                    if rect_mass_min.collidepoint((mouseX,mouseY)):
                        if(active_nb == True):
                            active_nb = not active_nb
                        elif(active_mass_max == True):
                            active_mass_max = not active_mass_max
                        active_mass_min = not active_mass_min
                    
                    # Type text input mass_max
                    if rect_mass_max.collidepoint((mouseX,mouseY)):
                        if(active_mass_min == True):
                            active_mass_min = not active_mass_min
                        elif(active_nb == True):
                            active_nb = not active_nb
                        active_mass_max = not active_mass_max
                
                    Utilities().display_text(self.window_surface, "Fichier incorrect", (self.button_posX, 410), self.poppins_font_30, '#D10000')

                    if rect_trash.collidepoint((mouseX,mouseY)):
                        file = None
                        error = None

                    # Import file
                    if rect_import.collidepoint((mouseX, mouseY)):

                        file = filedialog.askopenfile(mode = "r",initialdir="./data", title="selectionner", filetypes=(("Fichier CSV","*.csv"),("Fichier PDF","*.pdf"))).name
                        
                        if file != None:
                            file = controller.getBodyFromCSV(file)
                            print(*file)
                        else :
                            error = True

                if event.type == pygame.KEYDOWN:
                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:
                        # get text input from 0 to -1 i.e. end.
                        if(active_nb):
                            input_number = input_number[:-1]
                        elif(active_mass_min):
                            input_mass_min = input_mass_min[:-1]
                        elif(active_mass_max):
                            input_mass_max = input_mass_max[:-1]

                    # Unicode standard is used for string
                    # formation
                    else:
                        if event.unicode.isdigit():
                            if(active_nb):
                                input_number += event.unicode
                            elif(active_mass_min):
                                input_mass_min += event.unicode
                            elif(active_mass_max):
                                input_mass_max += event.unicode
            # Draw icon return
            self.window_surface.blit(self.icon_return, ((1200-self.icons_size-25, 800-self.icons_size-25)))

            # Draw play
            self.window_surface.blit(self.icon_play, (self.width//1.8, 700))       

            # Display text on inputs
            Utilities().display_text(self.window_surface, "Lancer la simulation", (self.width//3.3,700), self.poppins_font_30, '#007AB5')
            Utilities().display_text(self.window_surface,"Nombre de corps ? (2 - 100)", (400,75),self.poppins_font_30,'#007AB5')
            Utilities().display_text(self.window_surface,"Masse des corps minimum ? (x * (10**11 - 10**24) )", (400,200),self.poppins_font_30,'#007AB5')
            Utilities().display_text(self.window_surface,"Masse des corps maximum ? (x * (10**11 - 10**24) )", (400,325),self.poppins_font_30,'#007AB5')

            # Draw the rectangles
            pygame.draw.rect(self.window_surface,"#007AB5", rect_input_outline)
            pygame.draw.rect(self.window_surface, color_nb, rect_input)
            pygame.draw.rect(self.window_surface, "#007AB5", rect_mass_min_outline)
            pygame.draw.rect(self.window_surface, color_mass_min, rect_mass_min)
            pygame.draw.rect(self.window_surface, "#007AB5", rect_mass_max_outline)
            pygame.draw.rect(self.window_surface, color_mass_max, rect_mass_max)

            # Apply text surface
            Utilities().display_text(self.window_surface, input_number, (rect_input.x, rect_input.y), self.poppins_font_30, 'black')
            Utilities().display_text(self.window_surface, input_mass_min, (rect_mass_min.x, rect_mass_min.y), self.poppins_font_30, 'black')
            Utilities().display_text(self.window_surface, input_mass_max, (rect_mass_max.x, rect_mass_max.y), self.poppins_font_30, 'black')
            
            # Animation hover import button
            if not rect_import.collidepoint(mouseX, mouseY):
                if(error == True):
                    self.window_surface.blit(self.box_idle_incorrect, (self.button_posX,500))
                elif(error == False):
                    self.window_surface.blit(self.box_idle_correct, (self.button_posX,500))
                else:
                    self.window_surface.blit(self.box_idle, (self.button_posX,500))   
            else:
                if(error == True):
                    self.window_surface.blit(self.box_pressed_incorrect, (self.button_posX,500))
                elif(error == False):
                    self.window_surface.blit(self.box_pressed_correct, (self.button_posX,500))
                else:
                    self.window_surface.blit(self.box_pressed, (self.button_posX,500))
            
            # Graphics for import error
            if(error == True):
                Utilities().display_text(self.window_surface, "Fichier incorrect", (self.button_posX + 125, 450), self.poppins_font_30, '#D10000')
                self.window_surface.blit(self.icon_import_incorrect, (self.button_posX + 45, 500 + 35))  
                Utilities().display_text(self.window_surface, "Import", (self.button_posX + 225, 535), self.poppins_font_35, '#D10000')
            elif(error == False):
                Utilities().display_text(self.window_surface, "Fichier importé", (self.button_posX + 125, 450), self.poppins_font_30, '#10CA00')
                self.window_surface.blit(self.icon_import_correct, (self.button_posX + 45, 500 + 35))  
                self.window_surface.blit(self.icon_trash, (self.button_posX + self.button_dim[0] + 25, 500 + 35))
                Utilities().display_text(self.window_surface, "Import", (self.button_posX + 225, 535), self.poppins_font_35, '#10CA00')
            else:
                self.window_surface.blit(self.icon_import, (self.button_posX + 45, 500 + 35))  
                Utilities().display_text(self.window_surface, "Import", (self.button_posX + 225, 535), self.poppins_font_35, '#007AB5')
            # Update the screen
            pygame.display.update()

    
