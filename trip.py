from tabulate import tabulate

from database import Database
from config import DB_CONFIG

db = Database(**DB_CONFIG)

class Trip:
    fromLocations = []
    toLocations = []
    
    @staticmethod
    def getFromLocations():
        fromLocations = db.execute_query("SELECT fromLocation FROM Trip")
        locations = []
        for location in fromLocations:
            if location[0] not in locations:
                locations.append(location[0])
        return locations
        
    @classmethod
    def displayFromLocations(cls):
        cls.fromLocations = Trip.getFromLocations()
        header = ["Number", "From Location"]
        datas = []
        number = 1
        for location in cls.fromLocations:
            curData = []
            curData.append(number)
            number += 1
            curData.append(location)
            datas.append(curData)
        print(tabulate(datas, header, tablefmt="rounded_grid"))

    @staticmethod
    def getToLocations(fromLocation):
        toLocations = db.execute_query("SELECT toLocation FROM Trip WHERE fromLocation = ?" , (fromLocation))
        locations = []
        for location in toLocations:
            locations.append(location[0])
        return locations

    @classmethod
    def displayToLocations(cls, fromLocation):
        cls.toLocations = Trip.getToLocations(fromLocation)
        header = ["Number", "To Location"]
        datas = []
        number = 1
        for location in cls.toLocations:
            curData = []
            curData.append(number)
            number += 1
            curData.append(location)
            datas.append(curData)
        print(tabulate(datas, header, tablefmt="rounded_grid"))

    @staticmethod
    def getTripID(fromLocation, toLocation):
        result =  db.execute_query("SELECT * FROM Trip WHERE fromLocation = ? AND toLocation = ?", (fromLocation, toLocation), False)
        return result[0]
        


            
