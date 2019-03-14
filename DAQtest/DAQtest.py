
from PyDAQmx import Task
import PyDAQmx

import numpy as np
import time

from MultiChannelAnalogInput import *


writeTask = Task()
writeTask.CreateAOVoltageChan("/Dev1/ao0","",0.0,5.0,PyDAQmx.DAQmx_Val_Volts,None)

anIn = MultiChannelAnalogInput(["Dev1/ai0","Dev1/ai1","Dev1/ai2"], (0.0,5.0))
anIn.configure()


def setVoltage(value):
    conversionFactor = 1.5927
    writeTask.StartTask()
    writeTask.WriteAnalogScalarF64(1,5.0,conversionFactor*value,None)
    writeTask.StopTask()


def getVoltages(freq=10000, Nsamples=1):
    sum0 = 0;
    sum1 = 0;
    sum2 = 0;
    for i in range(Nsamples):
        vals = anIn.readAll()
        sum0 += vals['Dev1/ai0']
        sum1 += vals['Dev1/ai1']
        sum2 += vals['Dev1/ai2']
        time.sleep(1/freq)
    return (sum0/Nsamples, sum1/Nsamples, sum2/Nsamples)

def getAngleVoltAmp():
    vals = getVoltages()
    angle = vals[0]
    volt = vals[1]
    amp = vals[2] * .4337 # amps per volt
    return(angle,volt,amp)


while True:
    print(getAngleVoltAmp())
    time.sleep(.5)