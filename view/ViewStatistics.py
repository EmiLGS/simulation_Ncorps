class ViewStatistics(ViewTestPygame):
    def __init__(self):
        super().__init__()
        
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

                self.window_surface.blit(self.background, (0, 0))
                self.window_surface.blit(self.icon_return, ((self.icons_size, 800-self.icons_size-25)))

                # PRINT FPT
                FPTsize = FPTcanvas.get_width_height()
                FPTsurf = pygame.image.fromstring(FPTraw_data, FPTsize, "RGB")
                self.window_surface.blit(FPTsurf, (20,20))

                # Display title
                Utilities().display_text(self.window_surface, 'Statistiques', (self.width//2 - 150, -20), self.poppins_font_80, '#007AB5')

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run_statistic = False
                        self.jsonController.deleteJsonFile()
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