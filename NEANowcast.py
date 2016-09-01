from sgDataApiBase import sgDataApiBase
from dateutil import parser
from datetime import datetime
import dateutil
import pytz

class NEANowcast(sgDataApiBase):
    serviceName = '2hr_nowcast'

    def __init__(self):
        sgDataApiBase.__init__(self,"NEA")

    def result(self):
        jsonObj = self.getServiceResponse(dataset=self.serviceName)

        now = datetime.now(pytz.timezone('Asia/Singapore'))
        _result = "Time Now:" + now.strftime('%A,%d %B %H:%M %Z')

        for entry in jsonObj['channel']['item']['weatherForecast']['area']:
            _result = _result + "\n" + \
                    "Area Name: " + entry['@name'] + " Forecast: " + entry['@forecast']
        return _result
    
    def dump(self):
        return sgDataApiBase.dump(dataset=self.serviceName)


