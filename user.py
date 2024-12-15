from tabulate import tabulate

from abc import ABC, abstractmethod

from database import Database
from config import DB_CONFIG

db = Database(**DB_CONFIG)


class User(ABC):
    currentUser = None
    
    def __init__(self, id, username, password, fullName, birthDate, address, sex, email, contact):
        self.id = id
        self.username = username
        self.password = password
        self.fullName = fullName
        self.birthDate = birthDate
        self.address = address
        self.sex = sex
        self.email = email
        self.contact = contact

    @staticmethod
    def validateEmail(email):
        return True if "@" in email else False
    
    @abstractmethod
    def displayInformation():
        pass




class Driver(User):
    drivers = []

    def __init__(self, id, username, password, fullName, birthDate, address, sex, email, contact, fareRate, status):
        super().__init__(id, username, password, fullName, birthDate, address, sex, email, contact)
        self.fareRate = fareRate
        self.status = status

    def displayInformation():
        passenger = User.currentUser
        print("DRIVER INFORMATION:")
        print(f"FULLNAME: {passenger.fullName}\nBIRTHDATE: {passenger.birthDate}\nADDRESS: {passenger.address}\nSEX: {passenger.sex}\nEMAIL: {passenger.email}\nCONTACT: {passenger.contact}")

    @staticmethod
    def getAllDrivers():
        drivers = db.execute_query("SELECT dbo.Driver.driverID, dbo.Driver.status, dbo.Driver.fareRate, dbo.Driver.fullName, dbo.Vehicle.vehicleType, dbo.Vehicle.brand, dbo.Vehicle.model FROM dbo.Vehicle INNER JOIN dbo.Driver ON dbo.Vehicle.driverID = dbo.Driver.driverID")
        return drivers
    
    @classmethod
    def displayAllDriver(cls):
        cls.drivers = Driver.getAllDrivers()
        header = ["Driver ID", "Name", "Status", "Fare Rate (pesos)", "Vehicle"]
        datas = []
        number = 1
        for driver in cls.drivers:
            curData = []
            curData.append(number)
            number += 1
            curData.append(driver[3])
            curData.append(driver[1])
            curData.append(f"{driver[2]} pesos per km")
            curData.append(f"{driver[4]}, {driver[5]} {driver[6]}")
            datas.append(curData)
        print(tabulate(datas, header, tablefmt="rounded_grid"))

    @staticmethod
    def validateDriver(username, password):
        resultCount = db.execute_query("SELECT COUNT(*) FROM Driver WHERE username = ? AND password = ?", (username, password), False)[0]
        return True if resultCount != 0 else False
    
    @staticmethod
    def changeUser(username, password):
        result = db.execute_query("SELECT * FROM Driver WHERE username = ? AND password = ?", (username, password), False)
        User.currentUser = Driver(*result)

    @staticmethod
    def registerToDB(username, password, fullName, birthDate, address, sex, email, contact):
        rowAffected = db.execute_query("INSERT INTO Driver (username, password, fullName, birthDate, address, sex, email, contact, fareRate, status) VALUES (?,?,?,?,?,?,?,?,?,?)", (username, password, fullName, birthDate, address, sex, email, contact, 0.00, 'Available'))
        return True if rowAffected else False
    
    @staticmethod
    def displayBookings(driverID):
        results = db.execute_query("SELECT dbo.BookedTrip.bookID, dbo.Trip.fromLocation, dbo.Trip.toLocation, dbo.Passenger.fullName, dbo.BookedTrip.totalFare, dbo.BookedTrip.status FROM dbo.BookedTrip INNER JOIN dbo.Passenger ON dbo.BookedTrip.passengerID = dbo.Passenger.passengerID INNER JOIN dbo.Driver ON dbo.BookedTrip.driverID = dbo.Driver.driverID INNER JOIN dbo.Route ON dbo.BookedTrip.routeID = dbo.Route.routeID INNER JOIN dbo.Trip ON dbo.Route.tripID = dbo.Trip.tripID WHERE dbo.BookedTrip.driverID = ?", (driverID))
        header = ["Booked ID", "Trip", "Passenger", "Total Fare", "Status"]
        datas = []
        for booking in results:
            curData = []
            if booking[5] == "Pending" or booking[5] == "On-Going":
                curData.append(booking[0])
                curData.append(f"{booking[1]} - {booking[2]}")
                curData.append(booking[3])
                curData.append(f"{booking[4]} pesos")
                curData.append(booking[5])
                datas.append(curData)
        print(tabulate(datas, header, tablefmt="rounded_grid"))

    @staticmethod
    def acceptBooking(bookID, driverID):
        db.execute_query("UPDATE BookedTrip SET status = ? WHERE bookID = ?", ("On-Going", bookID))
        db.execute_query("UPDATE Driver SET status = ? WHERE driverID = ?", ("Not Available", driverID))
        db.close()

    @staticmethod
    def cancelBooking(bookID):
        db.execute_query("UPDATE BookedTrip SET status = ? WHERE bookID = ?", ("Cancelled", bookID))
        db.close()

    @staticmethod
    def updateBooking(bookID, driverID):
        db.execute_query("UPDATE BookedTrip SET status = ? WHERE bookID = ?", ("Done", bookID))
        db.execute_query("UPDATE Driver SET status = ? WHERE driverID = ?", ("Available", driverID))
        db.close()

    @staticmethod
    def seeTransaction(driverID):
        results = db.execute_query("SELECT dbo.BookedTrip.bookID, dbo.Trip.fromLocation, dbo.Trip.toLocation, dbo.Passenger.fullName, dbo.BookedTrip.totalFare, dbo.BookedTrip.status FROM dbo.BookedTrip INNER JOIN dbo.Passenger ON dbo.BookedTrip.passengerID = dbo.Passenger.passengerID INNER JOIN dbo.Driver ON dbo.BookedTrip.driverID = dbo.Driver.driverID INNER JOIN dbo.Route ON dbo.BookedTrip.routeID = dbo.Route.routeID INNER JOIN dbo.Trip ON dbo.Route.tripID = dbo.Trip.tripID WHERE dbo.BookedTrip.driverID = ?", (driverID))
        header = ["Booked ID", "Trip", "Passenger", "Total Fare", "Status"]
        datas = []
        for booking in results:
            curData = []
            if booking[5] == "Cancelled" or booking[5] == "Done":
                curData.append(booking[0])
                curData.append(f"{booking[1]} - {booking[2]}")
                curData.append(booking[3])
                curData.append(f"{booking[4]} pesos")
                curData.append(booking[5])
                datas.append(curData)
        print(tabulate(datas, header, tablefmt="rounded_grid"))

    @staticmethod
    def updateFareRate(driverID, fareRate):
        db.execute_query("UPDATE Driver SET fareRate = ? WHERE driverID = ?", (fareRate, driverID))
        db.close()

class Passenger(User):

    def __init__(self, id, username, password, fullName, birthDate, address, sex, email, contact):
        super().__init__(id, username, password, fullName, birthDate, address, sex, email, contact)

    def displayInformation():
        passenger = User.currentUser
        print("PASSENGER INFORMATION:")
        print(f"FULLNAME: {passenger.fullName}\nBIRTHDATE: {passenger.birthDate}\nADDRESS: {passenger.address}\nSEX: {passenger.sex}\nEMAIL: {passenger.email}\nCONTACT: {passenger.contact}")

    @staticmethod
    def validatePassenger(username, password):
        resultCount = db.execute_query("SELECT COUNT(*) FROM Passenger WHERE username = ? AND password = ?", (username, password), False)[0]
        return True if resultCount != 0 else False
    
    @staticmethod
    def changeUser(username, password):
        result = db.execute_query("SELECT * FROM Passenger WHERE username = ? AND password = ?", (username, password), False)
        User.currentUser = Passenger(*result)

    @staticmethod
    def registerToDB(username, password, fullName, birthDate, address, sex, email, contact):
        rowAffected = db.execute_query("INSERT INTO Passenger (username, password, fullName, birthDate, address, sex, email, contact) VALUES (?,?,?,?,?,?,?,?)", (username, password, fullName, birthDate, address, sex, email, contact))
        return True if rowAffected else False

        


# Passenger.validatePassenger("idol", "idol")
# Passenger.changeUser()
# print(User.currentUser)



    
