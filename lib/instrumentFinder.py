from pyvisa import *


class instrumentFinder:
    def __init__(self):
        self.isConnectedToInstrument = False
        try:
            self.rm = ResourceManager()
            self.instrument_list = self.rm.list_resources()
        except VisaIOError:
            print("Couldn't Find instruments")
    def printInstrumentList(self):
        print(self.instrument_list)
    def __getInstrumentList(self):
        return self.instrument_list
    def __getInstrumentCount(self):
        return len(self.instrument_list)
    def __getInstrumentIdn(self,instNum):
        try:
            self.device = self.rm.open_resource(self.instrument_list[instNum])
            self.resp = self.device.query("*IDN?")
            self.device.close()
            return self.resp
        except:
            return "noone is not a word"
    def __connectToInstrument(self, instNum):
        try:
            self.device = self.rm.open_resource(self.instrument_list[instNum])
            self.isConnectedToInstrument = True
        except:
            print("Connection failed")
            self.isConnectedToInstrument = False
    def disconnectFromInstrument(self, instNum):
        self.isConnectedToInstrument = False
        self.device.close()
    def findAndConnectToInstrument(self, instString):
        a = self.__getInstrumentList()
        b = 0
        while(b  < self.__getInstrumentCount()):
            if(0 <= self.__getInstrumentIdn(b).find(instString)):
                self.__connectToInstrument(b)
                self.isConnectedToInstrument = True
                b = self.__getInstrumentCount()+1
                print("Connected to " + instString)
            b+=1
        if(self.isConnectedToInstrument == False):
            print("Instrument not found")
            return -1
        return 0

#This method is fater than the original because it does not connect to each instrument to query its id...it just connects
#to the correct one based on what is in the list
    def findAndConnectToInstrumentFast(self, instString):
        a = self.__getInstrumentList()
        b = 0
        while (b < self.__getInstrumentCount()):
            if(0 <=self.instrument_list[b].find(instString)):
                self.__connectToInstrument(b)
                self.__isConnectedToInstrument = True
                b = self.__getInstrumentCount()+1
                print("Connected to " + instString)
            b+=1
        if(self.isConnectedToInstrument == False):
            print("Instrument not found")
            return -1
        return 0


    def isConnected(self):
        return self.isConnectedToInstrument
    def __del__(self):
        print("InstrumentFinder deleted")