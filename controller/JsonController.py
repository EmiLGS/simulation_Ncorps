import json, os
import random

class JsonController():
    def __init__(self, file):
        self.file = file
    
    # Function to store and add simulation's data in a json file
    def storeDataJson(self, data=[0,0],id=random.randint(50,100)):
        print(id)
        values = {
            id : {
            "Temps_calcul":data[0],
            "Approximation":data[1]
            },
        }

        array = []
        array.append(values)

        if(os.path.getsize(self.file) == 2):
            with open(self.file, "w") as json_file:
                json.dump(array, json_file, indent=None, separators=(',',':'))
        else:
            with open(self.file) as f:
                array = json.load(f)
                array.append(values)

            with open(self.file, "w") as json_file:
                json.dump(array, json_file, indent=None, separators=(',',': '))

    # Function to reset the file
    def deleteJsonFile(self):
        with open(self.file, "w") as json_file:
                json.dump([], json_file)