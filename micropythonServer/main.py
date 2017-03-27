import electrolink
# electroDebug is pc based electrolink, just for testing purposes, doing nothing in electronics
import electroGPIOdebug as electroGPIO
# real interface with electronics for ESP8266 processor
#import electroGPIO

# Give board a name
e = electrolink.Electrolink("weioESP")

# extend Electrolink with additional fnctions
e.addSpells(electroGPIO.spells)

# Broker MQTT server, mqtt protocol default port 1883
e.connectToServer("XXX.XXX.XXX.XXX")

while True:
    # blocking function, waiting for new message
    e.waitForMessage()

    # or use non-blocking message to do something else in this file
    # while checking for new messages
    #e.checkForMessage()
