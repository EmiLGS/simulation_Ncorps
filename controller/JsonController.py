import json, os
import random

class JsonController():
    def __init__(self, file):
        """
         Initialize the class with data from a file. This is the method that should be called by the user
         
         @param file - File to read data
        """
        self.file = file
        self.cpt = int(self.getSimulationNumber())
    
    # Function to store and add simulation's data in a json file
    def storeDataJson(self, data):
        """
         Stores data in json file. Stores data in json file and increases cpt by 1. If file exists it is loaded and the data is stored in array
         
         @param data - array with data to
        """
        self.cpt += 1
        values = [{
            "Numero Simulation":str(self.cpt),
            "Nombre corps":str(data[1]),
            "Algorithme":str(data[2]),
            "Temps calcul": data[3],
            "Precision":data[4],
        }]

        array = []
        array.append(values)

        # Write the values to the file.
        if(os.path.getsize(self.file) == 2):
            with open(self.file, "w") as json_file:
                json.dump(array, json_file, indent=None, separators=(',',':'))
        else:
            with open(self.file) as f:
                array = json.load(f)
                array.append(values)

            with open(self.file, "w") as json_file:
                json.dump(array, json_file, indent=None, separators=(',',': '))

    def getSimulationNumber(self):
        """
         Returns the number of simulations. It is used to determine the number of times the simulation was run.
         
         
         @return int number of simulation ( 1 if simulation failed ) or None if not found in the file ( in which case the number will be 1
        """
        with open(self.file, 'r') as file:
            data = json.load(file)
        return 1 if data == [] else data[-1][-1]["Numero Simulation"]
    # Function to reset the file
    def deleteJsonFile(self):
        """
         Delete json file to avoid re - reading it every time it is called. @ In None @ Out
        """
        self.cpt = 0
        with open(self.file, "w") as json_file:
                json.dump([], json_file)

    def getNumberOfItems(self):
        """
         Returns the number of items in the cache. This is used to determine how many items are cached for a given set of data.
         
         
         @return The number of items in the cache as an integer or None if there are no items in the cache
        """
        with open(self.file, 'r') as f:
            return len(json.load(f))