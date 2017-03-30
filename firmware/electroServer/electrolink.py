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
        # See function addCallbacks that is used to extend callbacks with your on functions
        # Parameters have to be declared in the most clear manner as they serve as a help
        # Description helps users to understand how to use function
        self.callbacks = {
                  "ping":         {"call": self.ping,          "parameters": None,         "description": "Verify if board responds, will respond 1"},
                  "getInfo":      {"call": self.getInfo,       "parameters": None,         "description": "Get board info"}, 
                  "getCallbacks": {"call": self.getCallbacks,  "parameters": None,         "description": "Get available instructions to call"},
                  "reset":        {"call": self.reset,         "parameters": None,         "description": "Hardware reset electronics"},
                  "setAckReceipt":{"call": self.setAckReceipt, "parameters": "true/false", "description": "Avis de reception"}
                  }

        # Acknowledge receipt - avis de reception
        self.ackReceipt = False
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
    def connectToServer(self, mqttServer, port=0, user=None, password=None, keepalive=0,
                 ssl=False, ssl_params={}):
        # This is server address
        self.server = mqttServer

        self.client = MQTTClient(self.CLIENT_ID, self.server, port, user, password, keepalive,
                 ssl, ssl_params)
        self.client.set_callback(self.subscriptionCallback)

        self.client.connect()
        self.client.subscribe(self.REQUEST_TOPIC)

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

        # Detect if we are in mode like jsonrpc with id for each message
        msgId = None
        if ("id" in data):
            msgId = data["id"]

        #print(method, params)

        # Try to execute function by calling directly callbacks dictionary
        try:
            # direct call here
            response = self.callbacks[method]["call"](params)

            # If there is value that was returned from the function then reply and copy requested parameters
            # Copying parameters is important so receiver can match it's call back function
            if not(response is None):
                p = {"requested":method, "params":params, "value":response} #pass back params to client
                if not(msgId is None):
                    p["id"] = msgId
                out = dumps(p)
                self.client.publish(self.ANSWER_TOPIC, out)
            else :
                if (self.ackReceipt is True):
                    p = {"requested":method, "params":params, "value":"OK"} #pass back params to client
                    if not(msgId is None):
                        p["id"] = msgId
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
        # All other unpredictible or personalized errors should be risen here
        # To rise your own exceptions do : rise Exception("My nasty error")
        except Exception as err:
            p = {"rawMessageReceived":[topic,msg], "error":str(err)}
            out = dumps(p)
            self.client.publish(self.ERROR_TOPIC, out)

    # Extend with new function calls
    def addCallbacks(self, newCallbacks):
        self.callbacks.update(newCallbacks)

    # Returns list of available functions that can be called
    def getCallbacks(self, arg):
        # Ignore call from the dictionary when sending
        # It's not trivial to make copy of dictionary in micropython
        # This is manual method
        keyCallbacks = list(self.callbacks)
        spl = {}
        for key in keyCallbacks:
            line = self.callbacks[key]
            spl[key] = {"parameters":line["parameters"], "description":line["description"]}
        return spl

    # Acknowledge receipt - avis de reception, each message will respond with OK if no return
    # message or with it's message
    def setAckReceipt(self, arg):
        val = arg[0]
        if ((val == "true") or (val == "True")): 
            self.ackReceipt = True
        elif ((val == "false") or (val == "False")):
            self.ackReceipt = False
        else :
            raise Exception("Bad parameter. Only 'true' or 'false' accepted")

    # Get info for the board
    def getInfo(self,arg):
        return self.info

    # Returns number 1 to show that he is alive
    def ping(self, arg):
        return 1

    def reset(self, arg):
        import machine
        machine.reset()
