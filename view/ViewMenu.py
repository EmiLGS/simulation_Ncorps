from view.ViewTestPygame import ViewTestPygame
import pygame, sys
from controller.Utilities import Utilities
from controller.JsonController import JsonController
from view.ViewConfiguration import ViewConfiguration

class ViewMenu(ViewTestPygame):
    def __init__(self):
        super().__init__()

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
                    self.jsonController.deleteJsonFile()
                    pygame.quit()
                    sys.exit()

                # Event when click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Click on Play
                    if rect_jouer.collidepoint((mouseX,mouseY)):
                        # Run the screen
                        self.run_menu = False
                        self.run_configurator = True
                        ViewConfiguration(self.run_configurator).configuration()
                    
                    # Click on Notice
                    if rect_notice.collidepoint((mouseX,mouseY)):
                        # Run the screen
                        self.run_menu = False
                        self.run_notice = True
                        ViewNotice(self.run_notice).Notice()

                    # Click on Quit
                    if rect_quitter.collidepoint((mouseX,mouseY)):
                        self.jsonController.deleteJsonFile()
                        sys.exit()
            
            
            pygame.display.flip()