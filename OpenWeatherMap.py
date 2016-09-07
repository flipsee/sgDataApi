from sgDataApiBase import sgDataApiBase
from dateutil import parser
from datetime import datetime
import dateutil
import pytz

class OpenWeatherMap(sgDataApiBase):

    def __init__(self):
        sgDataApiBase.__init__(self,"openweathermap")
        self.servicename = 'forecast'

    def result(self, City):
        jsonObj = self.getServiceResponse(q=City)

        now = datetime.now(pytz.timezone('Asia/Singapore'))
        _result = "Time Now:" + now.strftime('%A,%d %B %H:%M %Z')

        #implement open weather map data reading.
        #for entry in jsonObj['channel']['item']['weatherForecast']['area']:
        #    _result = _result + "\n" + \
        #            "Area Name: " + entry['@name'] + " Forecast: " + entry['@forecast']
        return _result
    
    def dump(self, City):
        return super(OpenWeatherMap,self).dump(q=City)


