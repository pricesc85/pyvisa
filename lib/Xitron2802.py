from pyvisa import *
import time
#import lib.instrumentFinder
from lib.instrumentFinder import instrumentFinder
_delay = .01
_identity = "XITRON,2802,0,v2.12,v2.11,v1.01,v1.02,v1.02,v1.02"

class Xitron2802(instrumentFinder):
    def __init__(self):
        super().__init__()
#        self.findAndConnectToInstrument("XITRON,2802")
        self.findAndConnectToInstrumentFast("GPIB0::3::INSTR")
#        print("Connected to Xitron 2802")

    def getI_AC(self, ch, bPrint):
        self.resp = self.device.query("READ=AMPS[CH1,AC]")
        if(True == bPrint):
            print(self.resp)
        return float(self.resp)

    def getI_ACDC(self, ch, bPrint):
        self.resp = self.device.query("READ=AMPS[CH1,ACDC]")
        if (True == bPrint):
            print(self.resp)
        return float(self.resp)

    def getI_DC(self, ch, bPrint):
        self.resp = self.device.query("READ=AMPS[CH1,DC]")
        if(True == bPrint):
            print(self.resp)
        return float(self.resp)

    def getV_AC(self, ch, bPrint):
        self.resp = self.device.query("READ=VOLTS[CH1,AC]")
        if (True == bPrint):
            print(self.resp)
        return float(self.resp)

    def getV_ACDC(self, ch, bPrint):
        self.resp = self.device.query("READ=VOLTS[CH1,ACDC]")
        if (True == bPrint):
            print(self.resp)
        return float(self.resp)

    def getP_ACDC(self, ch, bPrint):
        self.resp = self.device.query("READ=WATTS[CH1,ACDC]")
        if (True == bPrint):
            print(self.resp)
        return self.resp

    def getPF_ACDC(self, ch, bPrint):
        self.resp = self.device.query("READ=PF[CH1,ACDC]")
        if (True == bPrint):
            print(self.resp)
        return self.resp