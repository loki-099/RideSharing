from tabulate import tabulate

from database import Database
from config import DB_CONFIG

db = Database(**DB_CONFIG)


class Route:
    routes = []
    
    @staticmethod
    def getRouteForTrip(tripID):
        routes = db.execute_query("SELECT * FROM Route WHERE tripID = ?", (tripID))
        return routes
    
    @classmethod
    def displayRoutes(cls, tripID):
        cls.routes = Route.getRouteForTrip(tripID)
        header = ["Number", "Route", "Distance"]
        datas = []
        number = 1
        for route in cls.routes:
            curData = []
            curData.append(number)
            curData.append(f"Route {number}")
            number += 1
            curData.append(f"{route[2]} km")
            datas.append(curData)
        print(tabulate(datas, header, tablefmt="rounded_grid"))
        
