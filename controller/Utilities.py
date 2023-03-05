class Utilities():
    def __init__(self):
        self.width = 1200
        self.height = 800

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