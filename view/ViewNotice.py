class ViewNotice(ViewTestPygame):
    def __init__(self):
        super().__init__()
        
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
                        self.jsonController.deleteJsonFile()
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