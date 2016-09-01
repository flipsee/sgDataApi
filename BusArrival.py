from sgDataApiBase import sgDataApiBase
from dateutil import parser
from datetime import datetime
import dateutil
import pytz
import math

class BusArrival(sgDataApiBase):
    def __init__(self):
        sgDataApiBase.__init__(self,"LTA")
        sgDataApiBase.servicename = 'BusArrival'

    def result(self, BusStopID):
        jsonObj = self.getServiceResponse(BusStopID=BusStopID,SST='True')

        now = datetime.now(pytz.timezone('Asia/Singapore'))
        _result = "Time Now:" + now.strftime('%A,%d %B %H:%M %Z')

        for entry in jsonObj['Services']:
            try:
                nextBusArrival = dateutil.parser.parse(entry['NextBus']['EstimatedArrival'])
                nextBusInterval = math.floor(((nextBusArrival - now).total_seconds()/60))
            except:
                nextBusArrival = now
                nextBusInterval = 0

            try:
                next2BusArrival = dateutil.parser.parse(entry['SubsequentBus']['EstimatedArrival'])
                next2BusInterval = math.floor(((next2BusArrival - now).total_seconds()/60))
            except:
                next2BusArrival = now
                next2BusInterval = 0

            try:
                next3BusArrival = dateutil.parser.parse(entry['SubsequentBus3']['EstimatedArrival'])
                next3BusInterval = math.floor(((next3BusArrival - now).total_seconds()/60))
            except:
                next3BusArrival = now
                next3BusInterval = 0

            _result = _result + "\n" + \
                    "ServiceNo: " + str(entry['ServiceNo'] + ' >>> ') + \
                    str(nextBusInterval) + " Minutes (" + nextBusArrival.strftime('%H:%M') + ")," + \
                    str(next2BusInterval) + " Minutes (" + next2BusArrival.strftime('%H:%M') + ")," + \
                    str(next3BusInterval) + " Minutes (" + next3BusArrival.strftime('%H:%M') + ")"
        return _result
    

