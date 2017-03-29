import electroServer.electrolink as electrolink
# electroDebug is pc based electrolink, just for testing purposes, doing nothing in electronics
import modules.electroFiles.electroFiles as electroFiles
# real interface with electronics for ESP8266 processor
#import electroGPIO

from ujson import loads
config = loads((open("config.json", "r").read()))

# Give board a name
e = electrolink.Electrolink(config["thing_name"])

# extend Electrolink with additional fnctions
e.addCallbacks(electroFiles.callbacks)

# Broker MQTT server, mqtt protocol default port 1883
e.connectToServer(config["broker_server"])

while True:
    # blocking function, waiting for new message
    e.waitForMessage()

    # or use non-blocking message to do something else in this file
    # while checking for new messages
    #e.checkForMessage()
