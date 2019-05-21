import machine, network
import uasyncio as asyncio
import utime as time
from uasyncio.synchro import Lock
from ntptime import settime

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('FibreOP730', '24F2M3ATYNGY4M34')

loop = asyncio.get_event_loop()

async def setTime():
    while True:
        print("time is unset")
        try:
            settime() #No timezones, we use UTC.
        except IndexError:
            await asyncio.sleep(5) #Wait 5 seconds and try again
        else:
            print("time is", *time.localtime())
            break
loop.create_task(setTime())

hourOffset=3

async def setLights():
    t = time.localtime(time.time())[3]+hourOffset
    if 20 > t and t > 8:
        pass
    else:
        pass
    await asyncio.sleep(60*15) #15 minutes

loop.create_task(setLights())


from machine import ADC
adc = ADC(machine.Pin(32))
adc.atten(ADC.ATTN_6DB)

adcLock = Lock()

async def monitorPh():
    while True:
        await adcLock.acquire()
        samples=[]
        for i in range(0,9):
            samples.append(adc.read())
            await asyncio.sleep(0.1)
        sample=sum(samples)/10
        value = (sample/4095)*100

        print("ph =", value, "%")
        adcLock.release()
        await asyncio.sleep(5)

loop.create_task(monitorPh())

async def monitorEc():
    while True:
        await adcLock.acquire()
        adcLock.release()
        await asyncio.sleep(20*60)
loop.create_task(monitorEc())

p0 = machine.Pin(25, machine.Pin.OUT)
p1 = machine.Pin(26, machine.Pin.OUT)
p2 = machine.Pin(27, machine.Pin.OUT)
p3 = machine.Pin(14, machine.Pin.OUT)
p0.off()
p1.off()
p2.off()
p3.off()

rpmTarget=0.2
stepsPerRotation=4076*2 #An approximate value, double because of microstepping
sleepTime=60/rpmTarget/stepsPerRotation

states = (
    (1,0,0,0),
    (1,1,0,0),
    (0,1,0,0),
    (0,1,1,0),
    (0,0,1,0),
    (0,0,1,1),
    (0,0,0,1),
    (1,0,0,1),
)

async def runStepper():
    while True:
        for state in states:
            await asyncio.sleep(sleepTime)
            p0.value(state[0])
            p1.value(state[1])
            p2.value(state[2])
            p3.value(state[3])

loop.create_task(runStepper())

import gc
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
async def collectGarbage():
    gc.collect()
    await asyncio.sleep(60*5)

loop.create_task(collectGarbage())

loop.run_forever()
