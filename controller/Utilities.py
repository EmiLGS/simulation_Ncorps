class Utilities():
    def __init__(self):
        """
         Initialize the class by setting width and height to 1200x800. @ In None @ Out
        """
        self.width = 1200
        self.height = 800

    # Function to write paragraphes
    def display_text(self, surface, text, pos, font, color):
            """
             Display text on the screen. This is a helper for : meth : ` display_text_and_draw `
             
             @param surface - Surface to draw on.
             @param text - Text to display. Each line is separated by a space.
             @param pos - X and Y position of the text. This is a tuple ( x y ) where x is the horizontal position and y is the vertical position.
             @param font - Font to use for rendering the text. The font must have a
             @param color - Color to use for rendering
            """
            collection = [word.split(' ') for word in text.splitlines()]
            space = font.size(' ')[0]
            x,y = pos
            # Draws the font for each line in the collection.
            for lines in collection:
                # Draw the words in the font.
                for words in lines:
                    word_surface = font.render(words, True, color)
                    word_width, word_height = word_surface.get_size()
                    # Move the word to the first word.
                    if x + word_width >= self.width:
                        x = pos[0]
                        y += word_height
                    surface.blit(word_surface, (x,y))
                    x += word_width + space
                x = pos[0]
                y += word_height

    # Function that convert mass
    def convertMassForDisplay(self, mass):
        """
         Converts mass to display units for display. Mass is in kilograms per millimeters
         
         @param mass - mass to convert to display units
         
         @return mass in display units for mass in kilograms per millimeters rounded to the nearest
        """
        mass = mass / (10**24)
        mass = round(mass)
        return(mass)

    # Function to return the correct float of the input mass field
    def bodyMass(self,mass_val):
        """
         Calculate the mass of the body. It is assumed that the mass_val is in microns
         
         @param mass_val - string with the mass of the body
         
         @return float with the mass of the body in microns. This is used to calculate the mass
        """
        res = ''
        res2 = ''
        i = 0
        j = -1
        # Returns the mass of the value of the i th element in mass_val
        while (mass_val[i]) in ['1','2','3','4','5','6','7','8','9','.']:
            res += mass_val[i]
            i+=1
        # Find the value of the first element of mass_val
        while mass_val[j] != '*':
            res2 = mass_val[j] + res2
            j -= 1
        return float(res) * 10 ** int(res2)
    
    def bodyMassExp(self, mass_val):
        """
         Calculate the exponent of the body mass. This is used to calculate the mass of the body when it is in terms of masses
         
         @param mass_val - string representation of the mass
         
         @return int value of the
        """
        res = ''
        i = -1
        # Returns the value of the mass of the value i.
        while mass_val[i] != '*':
            res = mass_val[i] + res
            i -= 1
        return int(res)
        
