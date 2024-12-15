from user import User, Driver, Passenger
from trip import Trip
from route import Route
from vechicle import Vehicle
from payment import Payment

from os import system, name

def clear(): #* clearing terminals
    if name == 'nt': #* for windows
        _ = system('cls')
    else: # for mac and linux
        _ = system('clear')

###############################################################################################################*
#* PASSENGER PAGE

def routesPage(tripID, fromLocation, toLocation):
    print("ROUTE FOR TRIP MO KO:")
    Route.displayRoutes(tripID)
    print("\n0 - Cancel")
    index = int(input("Enter Route Number: ")) - 1

    if index == -1:
        clear()
        passengerPage()
    else:
        clear()
        route = Route.routes[index]
        print("CHOOSE A DRIVER:")
        Driver.displayAllDriver()
        print("\n0 - Cancel")
        driverIndex = int(input("Enter Driver ID: ")) - 1

        if driverIndex == -1:
            clear()
            passengerPage()
        else:
            clear()
            driver = Driver.drivers[driverIndex]
            totalFare = Payment.calculateTotalFare(route[2], driver[2])
            print("BOOK INFORMATION:")
            print("FROM LOCATION:", fromLocation)
            print("TO LOCATION:", toLocation)
            print("ROUTE: Route", index + 1)
            print(f"DISTANCE: {route[2]}km")
            print("DRIVER:", driver[3])
            print(f"TOTAL PAYMENT: {totalFare} pesos")
            choice = input("\n1 - Confirm\n0 - Cancel\nEnter choice: ")

            if choice == "1":
                Payment.insertBookTrip(User.currentUser.id, driver[0], route[0], totalFare)
                clear()
                print("SUCCESSFULLY BOOKED A TRIP!")
                input("Enter any key to back: ")
                clear()
                passengerPage()
            else:
                clear()
                print("BOOK CANCELLED!")
                passengerPage()


def bookATripPage():
    print("SELECT A STARTING LOCATION: ")
    Trip.displayFromLocations()
    print("\n0 - Go Back")
    index = int(input("Enter Location Number: ")) - 1

    if index == -1:
        clear()
        passengerPage()
    else: 
        clear()
        fromLocation = Trip.fromLocations[index]
        print("SELECT A DESTINATION LOCATION: ")
        Trip.displayToLocations(fromLocation)
        print("\n0 - Cancel")
        index = int(input("Enter Location Number: ")) - 1

        if index == -1:
            clear()
            passengerPage()
        else:
            clear()
            toLocation = Trip.toLocations[index]
            tripID = Trip.getTripID(fromLocation, toLocation)
            routesPage(tripID, fromLocation, toLocation)
            

def bookedTripPage():
    print("BOOKED TRIP:")
    Payment.displayPassengerBookedTrip(User.currentUser.id)
    choice = input("1 - Cancel a Trip\n0 - Back\n\nEnter choice: ")

    if choice == "1":
        bookID = int(input("Enter Booked Trip ID: "))
        Payment.cancelBookedTrip(bookID)
        clear()
        bookedTripPage()
    else:
        clear()
        passengerPage()


def transactionPage():
    print("TRANSACTION HISTORY:")
    Payment.displayTransactionHistory(User.currentUser.id)
    input("Enter any key to back: ")
    clear()
    passengerPage()
    

def passengerPage():
    print(f"Welcome, {User.currentUser.fullName}") 
    choice = input("1 - Book a Trip\n2 - See Booked Trip\n3 - See Transaction History\n4 - View Account Information\n0 - Log Out \n\nEnter your choice: ")
    
    if choice == "1":
        clear()
        bookATripPage()

    elif choice == "2":
        clear()
        bookedTripPage()

    elif choice == "3":
        clear()
        transactionPage()

    elif choice == "4":
        clear()
        Passenger.displayInformation()
        input("\nEnter any key to back: ")
        clear()
        passengerPage()

    elif choice == "0":
        clear()
        main()

#################################################################################################################*
#* DRIVER PAGE

def bookingsPage():
    print("BOOKINGS:")
    Driver.displayBookings(User.currentUser.id)
    choice = input("\n1 - Mark as Done\n2 - Accept\n3 - Decline\n0 - Back\n\nEnter choice: ")

    if choice == "1":
        bookID = input("Enter Booking ID: ")
        Driver.updateBooking(bookID, User.currentUser.id)
        clear()
        print("BOOKING DONE!")
        input("Enter any key to back: ")
        clear()
        bookingsPage()

    elif choice == "2":
        bookID = input("Enter Booking ID: ")
        Driver.acceptBooking(bookID, User.currentUser.id)
        clear()
        print("BOOKING ACCEPTED!")
        input("Enter any key to back: ")
        clear()
        bookingsPage()

    elif choice == "3":
        bookID = input("Enter Booking ID: ")
        Driver.cancelBooking(bookID)
        clear()
        print("BOOKING DECLINED!")
        input("Enter any key to back: ")
        clear()
        bookingsPage()

    else:
        clear()
        driverPage()


def driverTransactionPage():
    print("TRANSACTION HISTORY:")
    Driver.seeTransaction(User.currentUser.id)
    input("Enter any key to back: ")
    clear()
    driverPage()


def registerVehicle(driverID):
    print("REGISTER YOUR VEHICLE:")
    vehicleType = input("Enter Vehicle Type(Car, Motor, etc..): ")
    brand = input("Enter Vehicle Brand: ")
    model = input("Enter Vehicle Model: ")
    newVehicle = Vehicle(driverID, vehicleType, brand, model)
    newVehicle.registerToDB()
    clear()
    print("VEHICLE SUCCESSFULLY REGISTERED!")
    fareRate = int(input("Enter your Fare Rate(pesos per km): "))
    Driver.updateFareRate(User.currentUser.id, fareRate)
    input("Enter any key to back: ")
    clear()
    driverPage()


def driverPage():
    print(f"Welcome, {User.currentUser.fullName}") 
    print("1 - See Bookings\n2 - See Transaction History\n3 - View Account Information")
    if not Vehicle.checkDriver(User.currentUser.id):
        print("4 - REGISTER A VEHICLE FIRST!")
    choice = input("0 - Log Out \n\nEnter your choice: ")
    
    if choice == "1":
        clear()
        bookingsPage()

    elif choice == "2":
        clear()
        driverTransactionPage()

    elif choice == "3":
        clear()
        Driver.displayInformation()
        input("\nEnter any key to back: ")
        clear()
        driverPage()

    elif choice == "4":
        clear()
        registerVehicle(User.currentUser.id)

    elif choice == "0":
        clear()
        main()

#####################################################################################################################*

def main():
    # clear()
    print("RIDE SHARING APP")
    choice = input("1 - Passenger LogIn\n2 - Driver LogIn\n3 - Passenger Register\n4 - Driver Register\n\nEnter your choice: ")

    if choice == "1":
        clear()
        print("PASSENGER LOGIN")
        username = input("Enter username: ")
        password = input("Enter password: ")
        isValidated = Passenger.validatePassenger(username, password) 
        
        if (isValidated):
            Passenger.changeUser(username, password)
            clear()
            passengerPage() #* TO PASSENGER PAGE
        else:
            clear()
            print("NO USER FOUND")
            main()

    elif choice == "2":
        clear()
        print("DRIVER LOGIN")
        username = input("Enter username: ")
        password = input("Enter password: ")
        isValidated = Driver.validateDriver(username, password) 
        
        if (isValidated):
            Driver.changeUser(username, password)
            clear()
            driverPage() #* TO DRIVER PAGE
        else:
            clear()
            print("NO USER FOUND")
            main()

    elif choice == "3":
        clear()
        print("PASSENGER REGISTER: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        fullName = input("Enter Full Name: ")
        birthDate = input("Enter Birthdate(yyyy-mm-dd): ")
        address = input("Enter Address: ")  
        sex = input("Enter Sex: ")  
        while True:
            email = input("Enter email: ")
            if User.validateEmail(email):
                break
            print("Invalid Email Format. Try again!")
        contact = input("Enter Contact Number: ")

        if Passenger.registerToDB(username, password, fullName, birthDate, address, sex, email, contact):
            clear()
            print("SUCCESSFULLY REGISTERED!")
            main()
        else:
            clear()
            print("NOT REGISTERED!")
            main()

    elif choice == "4":
        clear()
        print("DRIVER REGISTER: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        fullName = input("Enter Full Name: ")
        birthDate = input("Enter Birthdate(yyyy-mm-dd): ")
        address = input("Enter Address: ")  
        sex = input("Enter Sex: ")  
        while True:
            email = input("Enter email: ")
            if User.validateEmail(email):
                break
            print("Invalid Email Format. Try again!")
        contact = input("Enter Contact Number: ")
        if Driver.registerToDB(username, password, fullName, birthDate, address, sex, email, contact):
            clear()
            print("SUCCESSFULLY REGISTERED!")
            main()
        else:
            clear()
            print("NOT REGISTERED!")
            main()


main()