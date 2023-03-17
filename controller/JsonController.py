import json, os

class JsonController():
    def __init__(self, file):
        self.file = file
    
    # Function to store and add simulation's data in a json file
    def storeDataJson(self, data=[0,0]):
        print(data[0], data[1])
        values = {
            "Temps calcul":str(data[0]),
            "Approximation":str(data[1])
        }

        array = []
        array.append(values)

        if(os.path.getsize(self.file) == 2):
            with open(self.file, "w") as json_file:
                json.dump(array, json_file, indent=3, separators=(',',': '))
        else:
            with open(self.file) as f:
                array = json.load(f)
                array.append(values)

            with open(self.file, "w") as json_file:
                json.dump(array, json_file, indent=3, separators=(',',': '))

    # Function to reset the file
    def deleteJsonFile(self):
        with open(self.file, "w") as json_file:
                json.dump([], json_file)