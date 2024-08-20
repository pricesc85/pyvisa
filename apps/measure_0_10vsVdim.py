
from lib.DP832 import *
from lib.Xitron2802 import *
import numpy
import pandas as pd
import matplotlib as plt
#def endSafeState():
#    PSU2 = DP832()
#    PSU2.set_voltage(1,0)
#    PSU2.toggle_output(1,0)
#    print("Output set to 0 and off")

#atexit.register(endSafeState)

if __name__ == '__main__':
    PSU = DP832("DP8C174504862")
    PA  = Xitron2802()

    PSU.set_voltage  (1, 0)
    PSU.toggle_output(1, 1)
    time.sleep(2)
    dimVoltage = 0.0
    i = 0
    data = numpy.zeros((1001,4))
    sleepVal = 0.1
    while(dimVoltage < 9.0):
        PSU.set_voltage(1,dimVoltage)

        time.sleep(sleepVal)
        iLED = PA.getI_ACDC(1, True)
        vLED = PA.getV_ACDC(1, True)
        data[i][0] = dimVoltage
        data[i][1] = iLED
        if(dimVoltage > 3) and (dimVoltage < 7):
            dimVoltage+=.5
            sleepVal = 1
        else:
            dimVoltage += .01
            sleepVal = 0.2
        i+=1
    i = 0
    dimVoltage = 9.0
    while(dimVoltage > 0.0):
        i+=1
        PSU.set_voltage(1,dimVoltage)
        time.sleep(sleepVal)
        iLED = PA.getI_ACDC(1, True)
        vLED = PA.getV_ACDC(1, True)
        data[i][2] = dimVoltage
        data[i][3] = iLED
        if(dimVoltage > 3) and (dimVoltage < 7):
            dimVoltage-=.5
            sleepVal = 1
        else:
            dimVoltage -= .01
            sleepVal = .2


    #print(data)
    df = pd.DataFrame(data,columns=['0-10 up','iLEDup','0-10 down','iLEDdn'])
    print(df)
    df.plot(x='0-10 up', y='iLEDup', kind = 'scatter')
    plt.pyplot.grid()
    plt.pyplot.show()
    filename = input("type filename if you want to save to csv")
    filename = filename + ".csv"
    df.to_csv(filename,mode="a")
#    print("Script complete")


