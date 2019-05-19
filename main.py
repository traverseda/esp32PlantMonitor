import uasyncio as asyncio
loop = asyncio.get_event_loop()

import machine
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('FibreOp730', '24F2M3ATYNGY4M34')

from ntptime import settime
settime() #No timezones, we use UTC.

import utime as time
hourOffset=3

async def setLights():
    t = time.localtime(time.time())
    if  20 < t.[3]+hourOffset > 8:
        pass
    else:
        pass
    await asyncio.sleep(60*15) #15 minutes

loop.create_task(runStepper())

p0 = machine.Pin(33, machine.Pin.OUT)
p1 = machine.Pin(25, machine.Pin.OUT)
p2 = machine.Pin(26, machine.Pin.OUT)
p3 = machine.Pin(27, machine.Pin.OUT)
p0.off()
p1.off()
p2.off()
p3.off()

rpmTarget=60
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

import gc
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
async def collectGarbage():
    gc.collect()
    await asyncio.sleep(60*15)

loop.create_task(runStepper())
loop.create_task(collectGarbage())

loop.run_forever()
