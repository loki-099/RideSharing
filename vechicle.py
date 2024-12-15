from database import Database
from config import DB_CONFIG

db = Database(**DB_CONFIG)


class Vehicle:
    
    def __init__(self, driverID, vehicleType, brand, model):
        self.driverID = driverID
        self.vehicleType = vehicleType
        self.brand = brand
        self.model = model

    @staticmethod
    def checkDriver(driverID):
        resultCount = db.execute_query("SELECT COUNT(*) FROM Vehicle WHERE driverID = ?", (driverID), False)[0]
        return True if resultCount != 0 else False
    
    def registerToDB(self):
        db.execute_query("INSERT INTO Vehicle (driverID, vehicleType, brand, model) VALUES (?,?,?,?)", (self.driverID, self.vehicleType, self.brand, self.model))
        db.close()
        