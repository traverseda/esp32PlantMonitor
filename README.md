```
#Reset to factory defaults
esptool --chip esp32 --port /dev/ttyUSB0 erase_flash
esptool --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-ppp-fix.bin

#Upload our code
ampy -p /dev/ttyUSB0  --baud 115200 put uasyncio/
ampy -p /dev/ttyUSB0  --baud 115200 put main.py
```
