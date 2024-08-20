from pyvisa import *
import time
from lib.instrumentFinder import instrumentFinder

class chroma61501(instrumentFinder):
    def __init__(self):
        super().__init__()
        self.connect()
    def connect(self):
        self.findAndConnectToInstrument("ATE,61501")
        self.findAndConnectToInstrumentFast("GPIB0::30::INSTR")
        print("Connected to Chroma 61501")
    def standardInit(self, vin):
        self.setHighVoltageModeNone()
        self.setCouplingAC()
        self.setOutputModeFixed()
        self.setFrequency("60")
        self.setOutputVolts(vin)
    def setCouplingAC(self):
        self.device.write("OUTP:COUP AC")
        print("Chroma 61501: set coupling to AC")
    def setCouplingDC(self):
        self.device.write("OUTP:COUP DC")
        print("Chroma 61501: set coupling to DC")
    def setCouplingACDC(self):
        self.device.write("OUTP:COUP ACDC")
        print("Chroma 61501: set coupling to ACDC")
    def setFrequency(self, freq):
        self.device.write("SOUR:FREQ:IMM " + freq)
        print("Chroma 61501: set frequency to " + freq)
    def setOutputModeFixed(self):
        self.device.write("OUTP:MODE FIXED")
        print("Chroma 61501: set mode to fixed")
    def setOutputVolts(self, volts):
        self.device.write("VOLT:AC %s" % volts)
        print("Chroma 61501: set output to %s" % volts + " volts")
    def setHighVoltageModeNone(self):
        self.device.write("OUTPut:OPTIon:HV NONE")
        print("Chroma 61501: Disabled high voltage option")
    def setOutputOn(self):
        self.device.write("OUTPUT ON")
        print("Chroma 61501: Turned on output")
    def setOutputOff(self):
        self.device.write("OUTPUT OFF")
        print("Chroma 61501: Turned off output")
    def __del__(self):
        print("Chroma 61501: Deleting.")
        self.setOutputOff()


