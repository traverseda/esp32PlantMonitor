import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('FibreOp730', '24F2M3ATYNGY4M34')

from ntptime import settime
settime() #No timezones, we use UTC.

import uasyncio as asyncio
import utime as time

hourOffset=3

async def setLights():
    t = time.localtime(time.time())
    if  20 < t.[3]+hourOffset > 8:
        pass
    else:
        pass
    await asyncio.sleep(60*15) #15 minutes

loop = asyncio.get_event_loop()
loop.create_task(runStepper())

