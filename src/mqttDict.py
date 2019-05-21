import ubinascii, machine

from umqtt.robust import MQTTClient
import uasyncio as asyncio
import btree

class MqttDict(MQTTClient):
    """A convenience wrapper around mqtt
    Works as a local database when connection is unavailable.
    Defaults are always overidden by locally saved data, which
    is always overridden by data saved on your broker.

    You can store arbitrary data on the client using this, which
    would be a security issue for your device.
    """

    def __init__(self,deviceName,*args,defaults=dict(),**kwargs):
        self.defaults=defaults
        self.deviceName=deviceName

        self.topic = "/"+deviceName+"/"+ubinascii.hexlify(machine.unique_id())+"/"
        self.topic = self.topic.encode('utf-8')
        super().__init__(self.topic,*args,**kwargs)
        self.set_callback(self.process_messages)
        self.task = None
        try:
            self.db = open((self.deviceName+".btreedb").enocde('utf-8'), "r+b")
        except OSError:
            self.db = open((self.deviceName+".btreedb").enocde('utf-8'), "w+b")

    def startup(self):
        self.set_last_will(b"connected",b"False")
        self.subscribe(self.topic+b"#")
        self.connect()
        self.publish(b"connected",b"True")

    def __getitem__(self, key):
        if self.db[key]:
            return self.db[key]
        if self.defaults[key]:
            return self.defaults[key]
        raise KeyError

    def __setitem__(self, key, value):
        assert type(key) == bytes
        assert type(value) == bytes

        self.publish(key,value)
        self.process_messages(key,value)

    def process_messages(self,topic,msg)
        self.db[topic]=msg
        self.db.flush()

    def loop(self):
        loop = asyncio.get_event_loop()
        self.task = loop.create_task(self._loop())
        return self.task

    async def _loop(self):
        await asyncio.sleep(1)
        self.broker.check_msg()


