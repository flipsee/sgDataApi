from sgDataApiBase import sgDataApiBase
import sgDataModel

class BusServices(sgDataApiBase):
    def __init__(self):
        sgDataApiBase.__init__(self,"API")
        sgDataApiBase.servicename = 'BusServices'

    def result(self, ServiceNo):
        data = sgDataModel.sgDataBL()
        try:
            query = data.get_busservices(ServiceNo)
            _result = ''
            for entry in query:
                _result = "ServiceNo:" + entry.ServiceNo + "\n" + \
                          "Operator:" + entry.Operator + "\n" + \
                          "Category:" + entry.Category
        finally:
            data.close()
        return _result
    
    def refreshStoredData(self):
        results = []
        data = sgDataModel.sgDataBL()
        try:
            print("Getting Data...")            
            with data.atomic() as txn:
                data.clear_busservices()

                while True:
                    jsonObj = self.getServiceResponse(skip=len(results))['value']
                    if jsonObj == []:
                        break
                    else:
                        data.add_busservices(jsonObj)
                        results += jsonObj

            print("Completed Getting Data, Count:" + str(len(results)))
        finally:
            data.close()        
        return self
