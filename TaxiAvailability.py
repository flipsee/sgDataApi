from sgDataApiBase import sgDataApiBase
from math import cos, sin, pi
import sgDataModel

class TaxiAvailability(sgDataApiBase):
    def __init__(self):
        sgDataApiBase.__init__(self, "LTA")
        sgDataApiBase.servicename = 'Taxi-Availability'

    def result(self, Latitude, Longitude, Radius):
        data = sgDataModel.sgDataBL()
        try:
            query = data.get_taxiavailability(Latitude, Longitude, Radius)
            _result = str(len(query)) + " Available within " + str(Radius) + " KM"
            #for entry in query:
            #    _result = "ServiceNo:" + entry.ServiceNo + "\n" + \
            #             "Operator:" + entry.Operator + "\n" + \
            #              "Category:" + entry.Direction
        finally:
            data.close()
        return _result
    
    def refreshStoredData(self):
        results = []
        data = sgDataModel.sgDataBL()
        try:
            print("Getting Data...")            
            with data.atomic() as txn:
                data.clear_taxiavailability()

                while True:
                    jsonObj = self.getServiceResponse(skip=len(results))['value']
                    if jsonObj == []:
                        break
                    else:
                        temp = []
                        for entry in jsonObj:
                            lat = entry["Latitude"]
                            lng = entry["Longitude"]
                            cos_lat = cos(lat * pi / 180)
                            sin_lat = sin(lat * pi / 180)
                            cos_lng = cos(lng * pi / 180)
                            sin_lng = sin(lng * pi / 180)
                            data.add_taxiavailabilitysingle(Latitude=lat, Longitude=lng, cos_lat=cos_lat, sin_lat=sin_lat, cos_lng=cos_lng, sin_lng=sin_lng)
                            #r = {"id": None ,"Latitude" : lat, "Longitude" : lng, "cos_lat" : cos_lat, "sin_lat" : sin_lat, "cos_lng" : cos_lng, "sin_lng" : sin_lng}
                            #temp += r
                            #print(str(r))
                        #data.add_taxiavailability(temp)
                        results += jsonObj
            print("Completed Getting Data")
        finally:
            data.close()        
        return self


