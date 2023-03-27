class ViewSimulation(ViewTestPygame):
    def __init__(self):
        super().__init__()

    def simulation(self, file=None, nbBodies = 50, mass_min = (5.9722*10**24), mass_max = (5.9722*10**24)):
            # Use a specific simulation
            sim = None
            if file == None:
                sim = MoreBodiesSimulation(nbBodies, mass_min, mass_max, self.width, self.height)
            else:
                sim = ImportBodiesSimulation(file, len(file))

            cmpt = 0
            data = [[],[]]
            initTime = time.time()
        
            #sim = BarnesHutSimulation(nbBodies ,mass,self.width,self.height,precision=1)

            while self.run_simulation:
                # Get mouse position
                cmpt += 1
                data[0].append( round(time.time() - initTime, 3) )
                data[1].append(cmpt)
                mouseX, mouseY = pygame.mouse.get_pos()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run_simulation = False
                        self.jsonController.deleteJsonFile()
                        pygame.quit()
                        sys.exit()
                    
                    # Events when click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Click on return
                        if cmpt > 200 :
                            if self.rect_return.collidepoint((mouseX,mouseY)):
                                # finishTime = time.time() - initTime
                                # print(f"Il y a eu {cmpt} Frame en {round(finishTime,3)} seconde(s)")

                                # Save simulation
                                # self.jsonController.storeDataJson([finishTime, 0])

                                self.run_statistic = True
                                self.run_simulation = False
                                self.statistic(data)

                        if self.rect_next.collidepoint((mouseX,mouseY)):
                            # Save simulation
                            # self.jsonController.storeDataJson([finishTime, 0])

                            # Run screen
                            self.run_configurator = True
                            self.run_simulation = False
                            self.configuration()

                # Draw background
                self.window_surface.blit(self.background, (0, 0))

                # Get base values for min and max exponential
                mass_min_r = math.floor(math.log(sim.bodies[0].mass, 10))
                mass_max_r = math.floor(math.log(sim.bodies[0].mass, 10))
                # Values for the size in pixels of the bodies
                minp = 1
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
                sim.advance()

                self.window_surface.blit(self.icon_return, ((self.icons_size, 800-self.icons_size-25)))

                # Draw next icon
                if cmpt > 200 :
                    self.window_surface.blit(self.icon_next, ((1200-self.icons_size-25, 800-self.icons_size-25)))

                pygame.display.update()