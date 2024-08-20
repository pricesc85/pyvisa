import signal
import sys
import subprocess
import threading
import multiprocessing
import os
import datetime
import time
import csv
#from lib.DP832 import *
from lib import DP832
#from lib.Xitron2802 import *
from lib import Xitron2802
#from lib.chroma61501 import *
from lib import chroma61501

EVERsetCommandPATH = r'C:\EVERsetCommand\batch_files\D21CC80UNVPWX12-C_calibrate.bat'
DP832_SN = "DP8C174504862"#This should be unique to the specific DP832, I select based on SN
XITRON_ADDR = 3 #This is assumed
CHROMA_ADDR = 30#This is assumed


#readPath = os.path.dirname(sys.argv[0]) + "/EVERsetCommand/EVERsetCommand.exe"
#C:\EVERsetCommand\EVERsetCommand.exe /ito "-1" /t "FEIG" /esn "TRUE" /dc "1" /o "READ" /pi "RFID"

PSU = DP832.DP832(DP832_SN)
PA = Xitron2802.Xitron2802()
CHR = chroma61501.chroma61501()

def runOnExit():
    global PSU, PA, CHR
    if PSU:
        del PSU
    if PA:
        del PA
    if CHR:
        del CHR
    os._exit(1)



def process_EVERsetCommandObserver(timeout):#This thread will kill EVERsetCommand if it does not terminate due to success
    time.sleep(timeout)
    retval = os.system('TASKKILL /f /IM EVERsetCommand.exe')#This will effectively kill the EVERsetCommand thread, if it is still running
    #if retval = 0, it terminated EVERsetCommand, program should stop
    #if retval = 128, EVERsetCommand terminated on its own
    if(retval == 0):
        runOnExit()
        #os._exit(1)

def thread_EVERsetCommandCalibrator(cPath):#I made this a thread so that I could create a separate thread to time it out
    timeout1 = multiprocessing.Process(target=process_EVERsetCommandObserver, args=(2,))
    timeout1.start()
    print("Calling EVERsetCommand to issue calibration command to driver")
    retval = subprocess.run(cPath, stdout=subprocess.PIPE).stdout.decode('utf-8')  # driver is ready to be turned on when this completes
    print(retval)
    timeout1.terminate()
    print("timeout terminated")

def thread_EVERsetCommandReader():
    global driverModel, serial
    driverModel = ''
    serial = ''
#    timeout2 = multiprocessing.Process(target=process_EVERsetCommandObserver, args=(2,))
#    timeout2.start()
    print("Calling EVERsetCommand to read driver")
    print(readPath)
    retval = subprocess.run(readPath, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(retval)
    if(retval.count("EVERsetCommand is exiting with the following Exit Code:  0 (Success).") > 0):
        index1 = retval.index("Reading...:  ")
        index2 = retval.index(".", index1 + len("Reading...:  "))
        driverModel = retval[index1+ len("Reading...:  "):index2]
        index1 = retval.index("The serial Number of the mated driver is ")
        index2 = retval.index(".", index1 + len("The serial Number of the mated driver is "))
        serial = retval[index1 + len("The serial Number of the mated driver is "):index2]
        print(driverModel + " found with serial number " + serial)
#    timeout2.terminate()

def thread_xitronMonitor():
    threadData = threading.local()
    threadData.count = 0
    while threadData.count < 10:
        print(PA.getI_ACDC(1,False))
        threadData.count+=1

def thread_xitronThresholdUpMonitor(threshold):
    val = 0.0
    while(val < threshold):
        t1 = time.time()
        val = float(PA.getI_ACDC(1,False))
        t2 = time.time()
        print(t2-t1, ' seconds, ', val, ' Amps')
    print("rising threshold reached")

def thread_xitronThresholdDnMonitor(threshold):
    val = threshold + 1
    while(val > threshold):
        t1 = time.time()
        val = float(PA.getI_ACDC(1,False))
        t2 = time.time()
        print(t2 - t1, ' seconds, ', val, ' Amps')
    print("falling threshold reached")

def getElbows():
    CHR.setOutputOn()
    PSU.set_voltage(1,0)
    time.sleep(1)
    iMin = PA.getI_ACDC(1, 0)
    print(iMin)
    #find minimum dim elbow
    tol = .05
    vPG = 0.50
    iCur = 0
    count = 0
    while(    (iCur < (iMin*(1.03)))
          and (count < 5           )):
        if(count == 0):
            vPG += .01
            PSU.set_voltage(1,vPG)
            time.sleep(.2)
            iCur = PA.getI_ACDC(1,0)
            if(iCur >= iMin*1.03):
                count+=1
        else:
            time.sleep(0.2)
            iCur = PA.getI_ACDC(1,0)
            if(iCur >= iMin*1.03):
                count+=1
            else:
                count = 0
    #find full bright elbow
    vLo = vPG
    vPG = 8.5
    count = 0
    PSU.set_voltage(1,vPG)
    time.sleep(0.5)
    iMax = PA.getI_ACDC(1,0)
    iCur = iMax
    while (iCur > (iMax * .997)) and (count < 5):
        if count == 0:
            vPG -= .01
            PSU.set_voltage(1,vPG)
            time.sleep(0.2)
            iCur = PA.getI_ACDC(1, 0)
            if iCur <=(iMax * .997):
                count+=1
        else:
            time.sleep(0.2)
            iCur = PA.getI_ACDC(1,0)
            if iCur <= (iMax * .997):
                count +=1
            else:
                count = 0
    vHi = vPG
    print("low elbow " + vLo.__str__() + "V")
    print("high elbow " + vHi.__str__() + "V")
    PSU.set_voltage(1,0)
    CHR.setOutputOff()
    return vLo, vHi, iMin, iMax


if __name__ == '__main__':
    start = time.time()
    print(str(datetime.datetime.now()))
#    driverModel = "D21CC80UNVPWX12-C"
#    prfName = "./EVERsetCommand/" + driverModel + "_cal.csv"
    CHR.standardInit(120)
    PSU.set_voltage(1,0)
    PSU.toggle_output(1,1)
    CHR.setOutputOff()
    time.sleep(0.5)
    #read driver model
#    reader = threading.Thread(target=thread_EVERsetCommandReader)
#    reader.start()
#    reader.join()
#    if(driverModel == ''):
#        print("No driver found coupled to FEIG tool.")
#        runOnExit()
#    with open(".\EVERsetCommand\genericCalibrate.csv", "w") as f:
#    prfName = "./EVERsetCommand/" + driverModel + "_cal.csv"
#    with open(prfName,'w') as calFile:
#        csvWriter = csv.writer(calFile)
#        csvWriter.writerows([['CatalogNumber','Type','QtyDrivers','CalibrationCommand','CalibrationType','DwellAt0mV_mSec','DwellDelay_mSec','DwellAt9000mV_mSec'],
#                            [driverModel,'RFID','1','Calibrate','AnalogCtrlVoltage','500','2000','2000']])
    print("Issuing calibration command")
    subprocess.call([EVERsetCommandPATH],timeout=5)
    CHR.setOutputOn()
    #look for the updoot in current, indicating first part of cal is complete
    y = threading.Thread(target=thread_xitronThresholdUpMonitor, args=(0.3,))#create thread
    y.start()#start it
    y.join()#wait for it to complete
    # rising edge indicates 0V calibration point complete, set to 9V
    PSU.set_voltage(1, 9)
    PSU.toggle_output(1,1)
    time.sleep(.1)
    # falling edge indicates calibration is done
    y = threading.Thread(target=thread_xitronThresholdDnMonitor, args=(0.3,))
    y.start()
    y.join()
    #additional rising edge indicates driver restarted after cal
    y = threading.Thread(target=thread_xitronThresholdUpMonitor, args=(0.3,))
    y.start()
    y.join()
    print(str(datetime.datetime.now()))
    end = time.time()
    print("Elapsed time: ", end-start, " seconds")
#    print(end - start)
    runOnExit()




