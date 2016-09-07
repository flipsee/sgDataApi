from BusArrival import BusArrival
from BusServices import BusServices
from BusRoutes import BusRoutes
from BusStop import BusStop
from TaxiAvailability import TaxiAvailability
from NEANowcast import NEANowcast


if __name__=="__main__":
    busStopID = "59419"
    print(BusStop().result(busStopID))
    print(BusArrival().result(busStopID))

    print("============================================")

    busStopID = "59411"
    #print(BusStop().result(busStopID))
    #print(BusArrival().result(busStopID))

    #BusStop().refreshStoredData()
    #print(BusStop().dump(skip=50))

    #BusServices().refreshStoredData()
    print(BusServices().result("806"))

    #BusRoutes().refreshStoredData()
    print(BusRoutes().result("806"))
    
    #TaxiAvailability().refreshStoredData()
    print(TaxiAvailability().result(1.3001925, 103.861926, 1))

    print(NEANowcast().result())
