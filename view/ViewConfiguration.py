from view.ViewTestPygame import ViewTestPygame
from view.ViewMenu import ViewMenu
import pygame, sys
from controller.Utilities import Utilities
from controller.JsonController import JsonController
from controller.VerifyController import VerifyController

class ViewConfiguration(ViewTestPygame):
    def __init__(self, run):
        super().__init__()
        self.run_configurator = run

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
        rect_import = pygame.Rect(self.button_posX,500,456,118)
        rect_trash = pygame.Rect(self.button_posX + self.button_dim[0] + 25, 500 + 35, self.icons_size, self.icons_size)

        file = None

        while self.run_configurator:
            # Get mouse position
            mouseX, mouseY = pygame.mouse.get_pos()

            controller = VerifyController((800,1200))

            # Draw background
            self.window_surface.blit(self.background, (0, 0))

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
                    self.jsonController.deleteJsonFile()
                    pygame.quit()
                    sys.exit()
                # CLICK EVENT
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Return
                    if self.rect_return.collidepoint((mouseX,mouseY)):
                        self.run_menu = True
                        self.run_configurator = False
                        ViewMenu().menu()

                    # Start simulation
                    if rect_jouer.collidepoint((mouseX,mouseY)):
                        if(can_run):
                            self.nb_simulations += 1
                            self.run_simulation = True
                            self.run_configurator = False

                            if(file == None):
                                ViewSimulation().simulation(nbBodies = int(input_number), mass_min = input_mass_min, mass_max = input_mass_max)
                            else:
                                self.simulation(file, nbBodies = int(input_number), mass_min = Utilities().bodyMass(input_mass_min), mass_max = Utilities().bodyMass(input_mass_max))

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
                        file = filedialog.askopenfile(mode = "r",initialdir="./data", title="selectionner", filetypes=(("Fichier CSV","*.csv"),("Fichier PDF","*.pdf")))
                        if file != None:
                            file = controller.getBodyFromCSV(file)
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