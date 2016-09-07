from abc import ABCMeta, abstractmethod
#imports
import configparser
import xmltodict, json
import re
from urllib.parse import urlparse
import httplib2 as http

class sgDataApiBase(metaclass=ABCMeta):
    servicename = ''
    APIConfig = None

    def __init__(self, servicetype):
        self.config = configparser.ConfigParser()
        self.config.read('sgDataApi.conf')
        self.configname = servicetype.upper() + "_API"
        self.APIConfig = self.config[self.configname] 

    def getServiceHeaders(self):
        #Header parameters
        _headers = dict()
        for key in self.APIConfig: 
            if key.upper().startswith('HEADER_'): _headers[re.sub("(?i)HEADER_","",key)] = self.APIConfig[key]
        return _headers 

    def getServiceURL(self, **kwargs):
        #Build query string & specify type of API call
        param = '' 
        
        for key in self.APIConfig:
            if not param:
                param = '?'
            elif param[len(param)-1] != '?':
                param = param + '&'
            if key.upper().startswith('PARAM_'): param = param + re.sub("(?i)PARAM_","",key) + '=' + self.APIConfig[key]

        for key, value in kwargs.items():
            if not param:
                param = '?'
            elif param[len(param)-1] != '?':
                param = param + '&'

            if key == 'skip': 
                key = '$skip'
            param = param + key + '=' + str(value)
        
        _serviceURL = urlparse(self.APIConfig["URI"] + self.servicename + param)        
        print(_serviceURL)
        return _serviceURL

    def getServiceResponse(self, **kwargs):
        method = 'GET'
        body = ''
        headers = self.getServiceHeaders()
        target = self.getServiceURL(**kwargs)
        
        #Get handle to http
        h = http.Http()

        #Obtain results
        response, content = h.request(target.geturl(),method,body,headers)

        if (response.status == 200): 
            #Parse JSON to print
            str_response = content.decode('utf-8')
            try:
                jsonObj = json.loads(str_response)
            except ValueError: #if not Json what should we do? 
                jsonObj = xmltodict.parse(str_response)            
                #print(json.dumps(jsonObj, sort_keys=True, indent=4))
            return jsonObj
        else: 
            print("getServiceResponse Failed: " + str(response.status))
            return None
        
    def dump(self, **kwargs):
        jsonObj = self.getServiceResponse(**kwargs)        
        _result = json.dumps(jsonObj, sort_keys=True, indent=4)        
        return _result
    
    @abstractmethod
    def result(self, **kwargs):
        pass
    
    #to delete and re-load data.
    def refreshStoredData(self, **kwargs):
        pass

