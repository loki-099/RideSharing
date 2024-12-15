from tabulate import tabulate

from database import Database
from config import DB_CONFIG

db = Database(**DB_CONFIG)

class Payment:
    bookedTrip = []
    
    @staticmethod
    def calculateTotalFare(distance, fareRate):
        totalFare = distance * fareRate
        return totalFare
    
    @staticmethod
    def insertBookTrip(passengerID, driverID, routeID, totalFare):
        db.execute_query("INSERT INTO BookedTrip (passengerID, driverID, routeID, totalFare, status) VALUES (?,?,?,?,?)", (passengerID, driverID, routeID, totalFare, 'Pending'))
        db.close()

    @staticmethod
    def getBookedTrip(passengerID):
        results = db.execute_query("SELECT dbo.BookedTrip.bookID, dbo.Trip.fromLocation, dbo.Trip.toLocation, dbo.Driver.fullName, dbo.BookedTrip.totalFare, dbo.BookedTrip.status FROM dbo.BookedTrip INNER JOIN dbo.Route ON dbo.BookedTrip.routeID = dbo.Route.routeID INNER JOIN dbo.Trip ON dbo.Route.tripID = dbo.Trip.tripID INNER JOIN dbo.Driver ON dbo.BookedTrip.driverID = dbo.Driver.driverID INNER JOIN dbo.Passenger ON dbo.BookedTrip.passengerID = dbo.Passenger.passengerID WHERE dbo.BookedTrip.passengerID = ?", (passengerID))
        db.close()
        return results

    @classmethod
    def displayPassengerBookedTrip(cls, passengerID):
        cls.bookedTrip = Payment.getBookedTrip(passengerID)
        header = ["Booked Trip ID", "Trip", "Driver", "Total Fare", "Status"]
        datas = []
        for trip in cls.bookedTrip:
            curData = []
            if trip[5] == "Pending" or trip[5] == "On-Going":
                curData.append(trip[0])
                curData.append(f"{trip[1]} - {trip[2]}")
                curData.append(trip[3])
                curData.append(f"{trip[4]} pesos")
                curData.append(trip[5])
                datas.append(curData)
        print(tabulate(datas, header, tablefmt="rounded_grid"))

    @classmethod
    def displayTransactionHistory(cls, passengerID):
        cls.bookedTrip = Payment.getBookedTrip(passengerID)
        header = ["Booked Trip ID", "Trip", "Driver", "Total Fare", "Status"]
        datas = []
        for trip in cls.bookedTrip:
            curData = []
            if trip[5] == "Cancelled" or trip[5] == "Paid":
                curData.append(trip[0])
                curData.append(f"{trip[1]} - {trip[2]}")
                curData.append(trip[3])
                curData.append(trip[4])
                curData.append(trip[5])
                datas.append(curData)
        print(tabulate(datas, header, tablefmt="rounded_grid"))
        
    @staticmethod
    def cancelBookedTrip(bookID):
        db.execute_query("UPDATE BookedTrip SET status = ? WHERE bookID = ?", ("Cancelled", bookID))
        db.close()