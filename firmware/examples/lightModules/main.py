import electroServer.electrolink as electrolink
# import module to deal with files over network
import modules.electroFiles as electroFiles

# import lighting modules
import modules.electroLight as electroLight
import modules.electroNeopixel as electroNeo


from ujson import loads
config = loads((open("config.json", "r").read()))

# Give board a name
e = electrolink.Electrolink(config["thing_name"])

lamp = electroLight.Lamp(4)
neo = electroNeo.Lamp(5, 42)

# extend Electrolink with additional fnctions
e.addCallbacks(lamp.callbacks)
e.addCallbacks(neo.callbacks)

# Broker MQTT server, mqtt protocol default port 1883
e.connectToServer(config["broker_server"])

while True:
    # blocking function, waiting for new message
    e.waitForMessage()

    # or use non-blocking message to do something else in this file
    # while checking for new messages
    #e.checkForMessage()
