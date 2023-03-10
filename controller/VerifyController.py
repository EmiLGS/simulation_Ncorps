import csv

class VerifyController():
    def __init__(self, window):
        self.window = window

    def verifyNb(self, nb):
        return (int(nb) >= 2 and int(nb) <= 200)
    
    def verifyMass(self, mass):
        return (mass >= 1)

    def verifyInput(self, input_number, input_mass_min, input_mass_max):
        # Check if parameters have been given
        return(input_number != '' and input_mass_min != '' and input_mass_max != '') 

    def verifyImport(self, file):
        tab = self.getBodyFromCSV(file)
 
        # Verify size
        if(len(tab) < 2 or len(tab) > 200):
            return False

        # Verify position of each objects
        for i in range(len(tab)):
            if(int(tab[i][0]) < 0 or int(tab[i][0]) > self.window[0]):
                return False  
            if(int(tab[i][1]) < 0 or int(tab[i][1]) > self.window[1]):
                return False
        
        return True
    
    def getBodyFromCSV(self, file):
        tab = []
        row_count = 0

        # Défine size of the array
        with open(file, 'r') as f:
            obj = csv.reader(f)
            row_count = sum(1 for row in obj)
            tab = [0] * (row_count-1)

        # Migrate data from csv to the array
        with open(file, 'r') as f:
            obj = csv.reader(f)
            i = -1
            for ligne in obj:
                if(i != -1):
                    tab[i] = ligne
                i += 1

        return tab