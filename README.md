A 3D printed rotary hydroponics system. We use an esp32 for monitoring.

You need to edit `src/main.py` with your network credentials if you want the
timer to be accurate.

```
#Reset to factory defaults
esptool --chip esp32 --port /dev/ttyUSB0 erase_flash
esptool --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-ppp-fix.bin

#Upload our code
#Make sure you're in the right directory nathan! You need to run these command
#from the same folder as this readme
ampy -p /dev/ttyUSB0  --baud 115200 put src/*
ampy -p /dev/ttyUSB0  --baud 115200 put main.py
```

The 3D models are not as parametric as they look, you're probably better off
leaving all those values at defaults.
