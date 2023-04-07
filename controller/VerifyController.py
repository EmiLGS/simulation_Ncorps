import csv
import os

class VerifyController():
    def __init__(self, window):
        """
         Initializes the instance. This is called by __init__ and should not be called directly. The window is passed as an argument to the constructor.
         
         @param window - The window to use for the event loop. If it is a : class : ` pyqtgraph. Window ` it will be used as the window
        """
        self.window = window

    def verifyNb(self, nb):
        """
         Verify the number of items to be downloaded. This is a sanity check to make sure we don't have too many items
         
         @param nb - The number of items to download
         
         @return True if the number is valid False if it's not valid or an error occured ( in which case the user should be prompted
        """
        return (int(nb) >= 2 and int(nb) <= 200)
    
    def verifyMass(self, mass):
        """
         Verify mass. This is a method to be overridden by subclasses. The mass must be greater than 1
         
         @param mass - the mass of the object
         
         @return True if mass is greater than 1 False if mass is equal to 1 or the object is unsat
        """
        return (mass >= 1)

    def verifyInput(self, input_number, input_mass_min, input_mass_max):
        """
         Verify input parameters are valid. This method is called by L { process } when it is about to process a file or the command line arguments have been parsed.
         
         @param input_number - The number of the file or the command line arguments as a string.
         @param input_mass_min - The minimum mass of the file or the command line arguments as a string.
         @param input_mass_max - The maximum mass of the file or the command line arguments as a string.
         
         @return True if the parameters are valid False otherwise. In this case the method should return True even if there are parameters that aren't
        """
        # Check if parameters have been given
        return(input_number != '' and input_mass_min != '' and input_mass_max != '') 

    def verifyImport(self, file):
        """
         Verify import is valid. This is a helper for L { import } and L { import_csv }
         
         @param file - File to import as CSV
         
         @return True if import is valid False if import is not valid or if error is raised in some way ( such as file not found
        """
        tab = self.getBodyFromCSV(file)

        # Verify size
        # Check if tab is a valid tab.
        if(len(tab) < 2 or len(tab) > 200):
            return False

        # Verify position of each objects
        # Check if the window is within the window
        for i in range(len(tab)):
            # Check if the tab is within window
            if(int(tab[i][0]) < 0 or int(tab[i][0]) > self.window[0]):
                return False
            # Check if the tab is within the window
            if(int(tab[i][1]) < 0 or int(tab[i][1]) > self.window[1]):
                return False
        
        return True
    
    # def verifyExtension(self,file):
    #     file_name, file_extension = os.path.splitext(file)
    #     print(file_extension)
    #     if (file_extension == '.csv'):
    #         return True
    #     return False
    
    def getBodyFromCSV(self, file):
        """
         Reads the body of the file and returns it as a 2D array. The first column is the header the second column is the data
         
         @param file - File to read from.
         
         @return Array of data from the csv file. It is assumed that the header is a column of the first
        """
        tab = []
        row_count = 0
        

        # Define size of the array
        with open(file, 'r') as f:
            obj = csv.reader(f)
            row_count = sum(1 for row in obj)
            tab = [0] * (row_count-1)

        # Migrate data from csv to the array
        with open(file, 'r') as f:
            obj = csv.reader(f)
            i = -1
            # Set tab to the ligne in obj
            for ligne in obj:
                # Set tab at index i to ligne
                if(i != -1):
                    tab[i] = ligne
                i += 1

        return tab