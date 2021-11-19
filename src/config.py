class config:
    CONFIGURATION={}
    def __init__(self,conf_filename):
        with open(conf_filename,'r') as cf:
            for line in cf:
                kvpair=line.strip()
                if kvpair and kvpair[0] != '#':
                    key,value=kvpair.split('=')
                    self.CONFIGURATION[key]=value #If there is a key value pair more than once, latest one will be sdded.
    def get(self,key):
        return self.CONFIGURATION[key] if key in self.CONFIGURATION else None
    def put(self,key,value):
        self.CONFIGURATION[key]=value
