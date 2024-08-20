from lib.DP832 import *
from lib.Xitron2802 import *
import numpy
import pandas as pd
import matplotlib as plt

if __name__ == '__main__':
    PSU = DP832("DP8C174504862")
    PA  = Xitron2802()

    PSU.set_voltage  (1, 0)
    PSU.toggle_output(1, 1)
    dimVoltage = 0.5
    i = 0
    data = numpy.zeros((1001,3))
    sleepVal = 0.1
    while(dimVoltage < 9.0):
        PSU.set_voltage(1,dimVoltage)

        time.sleep(sleepVal)
        iLED = PA.getI_ACDC(1, True)
        vLED = PA.getV_ACDC(1, True)
        data[i][0] = dimVoltage
        data[i][1] = iLED
        data[i][2] = vLED
        if(dimVoltage <= 2) or (dimVoltage >= 7):
            dimVoltage += .01
            sleepVal = .1
        else:
            dimVoltage += 0.5
            sleepVal = 1
        i+=1

    #print(data)
    df = pd.DataFrame(data,columns=['0-10','iLED','vLED'])
    print(df)
    df.plot(x='0-10', y='iLED', kind = 'scatter')
    plt.pyplot.grid()
    plt.pyplot.show()
    filename = input("type filename if you want to save to csv")
    filename = filename + ".csv"
    df.to_csv(filename,mode="a")