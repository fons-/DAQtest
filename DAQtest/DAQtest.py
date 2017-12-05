
from PyDAQmx import Task
import PyDAQmx

import numpy as np
import time

from MultiChannelAnalogInput import *


writeTask = Task()
writeTask.CreateAOVoltageChan("/Dev1/ao0","",0.0,5.0,PyDAQmx.DAQmx_Val_Volts,None)

anIn = MultiChannelAnalogInput(["Dev1/ai0"])
anIn.configure()


def setVoltage(value):
    writeTask.StartTask()
    writeTask.WriteAnalogScalarF64(1,5.0,1.5927*value,None)
    writeTask.StopTask()


def getVoltage(freq=10000, Nsamples=50):
    sum = 0;
    for i in range(Nsamples):
        sum += anIn.read()
        time.sleep(1/freq)
    return sum/Nsamples


while True:
    print(getVoltage())
    time.sleep(.5)