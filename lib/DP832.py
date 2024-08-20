#!/usr/bin/env python

from pyvisa import *
import time
from lib.instrumentFinder import instrumentFinder

#_identity = "RIGOL TECHNOLOGIES,DP832,DP8C174504862,00.01.14"
_delay = 0.01  # in seconds


class DP832(instrumentFinder):
    snString = ""
    def __init__(self, SN):
        super().__init__()
        self.connect(SN)

    def connect(self, SN):
        if(SN == 0):
            self.findAndConnectToInstrumentFast("RIGOL TECHNOLOGIES,DP832,")#DP8C174504862,00.01.14")
        else:
            self.findAndConnectToInstrumentFast(SN)

    def select_output(self, chan):
        # define a CHANNEL SELECT function
        command = ':INST:NSEL %s' % chan
        self.device.write(command)
#        time.sleep(_delay)

    def toggle_output(self, chan, state):
        # define a TOGGLE OUTPUT function
        command = ':OUTP CH%s,%s' % (chan, state)
        self.device.write(command)
#        time.sleep(_delay)
        if(state == 1):
            print("DP832: Channel " + str(chan) + " output enabled")
        else:
            print("DP832: Channel " + str(chan) + " output disabled")
    def set_voltage(self, chan, val):
        # define a SET VOLTAGE function
        command = ':INST:NSEL %s' % chan
        self.device.write(command)
#        time.sleep(_delay)
        command = ':VOLT %s' % val
        self.device.write(command)
#        time.sleep(_delay)
        print("DP832:Set channel " + str(chan) + " to " + str(val) + " volts")
    def set_current(self, chan, val):
        # define a SET CURRENT function
        command = ':INST:NSEL %s' % chan
        self.device.write(command)
#        time.sleep(_delay)
        command = ':CURR %s' % val
        self.device.write(command)
#        time.sleep(_delay)

    def set_ovp(self, chan, val):
        # define a SET VOLT PROTECTION function
        command = ':INST:NSEL %s' % chan
        self.device.write(command)
#        time.sleep(_delay)
        command = ':VOLT:PROT %s' % val
        self.device.write(command)
#        time.sleep(_delay)

    def toggle_ovp(self, state):
        # define a TOGGLE VOLTAGE PROTECTION function
        command = ':VOLT:PROT:STAT %s' % state
        self.device.write(command)
#        time.sleep(_delay)

    def set_ocp(self, chan, val):
        # define a SET CURRENT PROTECTION function
        command = ':INST:NSEL %s' % chan
        self.device.write(command)
#        time.sleep(_delay)
        command = ':CURR:PROT %s' % val
        self.device.write(command)
 #       time.sleep(_delay)

    def toggle_ocp(self, state):
        # define a TOGGLE CURRENT PROTECTION function
        command = ':CURR:PROT:STAT %s' % state
        self.device.write(command)
 #       time.sleep(_delay)

    def measure_voltage(self, chan):
        # define a MEASURE VOLTAGE function
        command = ':MEAS:VOLT? CH%s' % chan
        volt = self.device.query(command)
        volt = float(volt)
#        time.sleep(_delay)
        return volt

    def measure_current(self, chan):
        # define a MEASURE CURRENT function
        command = ':MEAS:CURR? CH%s' % chan
        curr = self.device.query(command)
        curr = float(curr)
 #       time.sleep(_delay)
        return curr

    def measure_power(self, chan):
        # define a MEASURE POWER function
        command = ':MEAS:POWE? CH%s' % chan
        power = self.device.query(command)
        power = float(power)
#        time.sleep(_delay)
        return power

    def __del__(self):
        print("Deleting DP832")
        self.set_voltage(1,0)
        self.set_voltage(2, 0)
        self.set_voltage(3, 0)
        self.toggle_output(1, 0)
        self.toggle_output(2, 0)
        self.toggle_output(3, 0)
