from umqtt.simple import MQTTClient
from ujson import loads, dumps

class Electrolink:
    # Constructor, give name of your board
    def __init__(self, objectName):

        # Write here board name, board info and board capabilities
        # Name will be set in constructor
        self.info = {"board":"ESP8266", "name":None}

        # Setting all function names that can be called by electrolink
        # and it's pointers
        # See function addSpells that is used to extend spells with your on functions
        self.spells = {
                  "ping":self.ping,
                  "getInfo": self.getInfo,
                  "getSpells": self.getSpells}

        # Name of
        self.CLIENT_ID = objectName
        self.info["name"] =  self.CLIENT_ID
        # Name of board is used as root name
        # Command topic is used to receive instructions
        self.REQUEST_TOPIC = self.CLIENT_ID+"/command"
        # Reply topic is used to answer when there is need to 
        self.ANSWER_TOPIC =  self.CLIENT_ID+"/reply"
        # Error tocpi is used to explain what caused error
        self.ERROR_TOPIC =   self.CLIENT_ID+"/error"

    # Connects to broker using native mqtt interface
    # Aftr connexion subscription to command topic will be done
    def connectToServer(self, mqttServer):
        # This is server address
        self.server = mqttServer

        self.client = MQTTClient(self.CLIENT_ID, self.server)
        self.client.set_callback(self.subscriptionCallback)

        self.client.connect()
        self.client.subscribe(self.REQUEST_TOPIC)

    # Returns number 1 to show that he is alive
    def ping(self, arg):
        return 1

    # This is BLOCKING function, it will wait until gets new message to continue execution
    def waitForMessage(self):
        self.client.wait_msg()

    # This is NON-BLOCKING function and it will not wait getting new message.
    def checkForMessage(self):
        self.client.check_msg()

    # Callback to be called when receive the message
    def subscriptionCallback(self, topic, msg):
        data = loads(msg)
        method = data["method"]
        params = data["params"]
        #print(method, params)

        # Try to execute function by calling directly spells dictionary
        try:
            # direct call here
            response = self.spells[method](params)

            # If there is value that was returned from the function then reply and copy requested parameters
            # Copying parameters is important so receiver can match it's call back function
            if not(response is None):
                p = {"requested":method, "params":params, "value":response} #pass back params to client
                out = dumps(p)
                self.client.publish(self.ANSWER_TOPIC, out)

        # These are common errors
        except IndexError:
            p = {"rawMessageReceived":[topic,msg], "error":"Incorrect number of parameters"}
            out = dumps(p)
            self.client.publish(self.ERROR_TOPIC, out)
        except KeyError:
            p = {"rawMessageReceived":[topic,msg], "error":"Method don't exist"}
            out = dumps(p)
            self.client.publish(self.ERROR_TOPIC, out)
        except Exception as err:
            p = {"rawMessageReceived":[topic,msg], "error":str(err)}
            out = dumps(p)
            self.client.publish(self.ERROR_TOPIC, out)

    # Extend with new function calls
    def addSpells(self, newSpells):
        self.spells.update(newSpells)

    # Returns list of available functions that can be called
    def getSpells(self, arg):
        return list(self.spells)

    # Get info for the board
    def getInfo(self,arg):
        return self.info
