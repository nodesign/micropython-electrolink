import sys
import paho.mqtt.client as mqtt
import json
import pytoml as toml
import re
from termcolor import colored
import time

import readline
import rlcompleter

# import logging
#
# LOG_FILENAME = 'completer.log'
# logging.basicConfig(filename=LOG_FILENAME,
#                     level=logging.DEBUG,
#                     )

alive = False

wlcmMessage = True
welcome = "Welcome to Electrolink! Your board is connected\nType getSpells() to discover board capabilities\nOther instructions has to be sent in the format : digitalWrite(1,1)\nTo end program type exit"

spells = None
waitSpells = True

def on_connect(mqttc, obj, flags, rc):
    t = colored('\nConnected to broker', 'green', attrs=['reverse'])
    print(t)

def on_message(mqttc, obj, msg):
    global spells
    global waitSpells
    global alive
    a = json.loads(str(msg.payload))
    t = None
    topic = None
    if (msg.topic == thingName+"/reply"):
        topic = colored("\n"+msg.topic, 'green', attrs=['reverse'])
        if (a["requested"] == "ping"):
            alive = True
            t = colored(thingName +" is alive!", 'green',  attrs=['reverse', 'blink'])
        else :
            if (waitSpells is True):
                if (a["requested"] == "getSpells"):
                    spells = list(a["value"])
                    waitSpells = False
            else :
                t = colored(json.dumps(a["value"], indent=4, sort_keys=True), 'green')
    else :
        topic = colored("\n"+msg.topic, 'red', attrs=['reverse'])
        t = colored(a["error"], 'red')

    print(topic)
    print(t)
    #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

def on_publish(mqttc, obj, mid):
    #print("\ncommand sent")
    pass
def on_subscribe(mqttc, obj, mid, granted_qos):
    #print("Subscribed: "+str(mid)+" "+str(granted_qos))
    pass

def on_log(mqttc, obj, level, string):
    print(string)

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def extractBetween(start,end,data):
    return re.search(start+'(.*)'+end, data)

def parseInstruction(c):
    data = "".join(c.split())
    if ((data == "exit") or (data == "exit()")):
        print("Closing electrolink connexion")
        mqttc.loop_stop()
        exit()
    else:
        result = extractBetween("\(","\)", data)
        if not(result is None):
            method = data.split(result.group(0))[0]
            params = result.group(1).split(",")
            #print("method",method)
            #print("params", params)
            cnt = 0
            for p in params:
                res1 = extractBetween('"','"',p)
                res2 = extractBetween("'","'",p)
                #print(res1,res2)
                if not((res1 is None) and (res2 is None)):
                    if not(res1 is None):
                        params[cnt] = p.split('"')[1]
                        #print(params[cnt])
                    else:
                        params[cnt] = p.split("'")[1]
                    
                else :
                    if(p is ''):
                        params = []
                    else :
                        params[cnt] = num(p)
                cnt+=1
            if (method is ''):
                print("Bad command\n")
            else :
                out = {"method":method, "params":params}
                nogo = False
                # handle special case with files
                index = 0
                for a in out["params"]:
                    if ("file:" in a):
                        try :
                            f = open(a.split("file:")[1], "r")
                            fileData = f.read()
                            out["params"][index] = fileData
                        except:
                            print("File not found")
                            nogo = True
                    index+=1
                if (nogo is False):
                    mqttc.publish(thingName+"/command", json.dumps(out))
                #print(out)
        else:
            if (len(data)>0):
                print("Bad command\n")

class SimpleCompleter(object):
    
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                self.matches = [s 
                                for s in self.options
                                if s and s.startswith(text)]
#                logging.debug('%s matches: %s', repr(text), self.matches)
            else:
                self.matches = self.options[:]
#                logging.debug('(empty input) matches: %s', self.matches)
        
        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.matches[state]
        except IndexError:
            response = None
#        logging.debug('complete(%s, %s) => %s', 
#                      repr(text), state, repr(response))
        return response

def input_loop():
    global wlcmMessage
    global waitSpells
    global spells
    c = ''
    while True:
        if (alive == False):
            print("Pinging board with name : "+ thingName +"...")
            #print("No answer? Than your board is not connected")
            out = {"method":"ping", "params":[]}
            mqttc.publish(thingName+"/command", json.dumps(out))
            time.sleep(0.5)
            

        else :
            if (wlcmMessage == True):
                out = {"method":"getSpells", "params":[]}
                mqttc.publish(thingName+"/command", json.dumps(out))
                while(waitSpells is True):
                    time.sleep(0.1)

                spells.append("exit")
                spells.append("help")

                readline.set_completer(SimpleCompleter(spells).complete)
                print(welcome)

                wlcmMessage = False
            c = raw_input("electrolink > ")
            parseInstruction(c)

###########################################################################################################
# PROGRAM STARTS HERE
###########################################################################################################
# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client("electrolinkConsole")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log

print("Reading configuration from config.toml file")
config = ""
with open('config.toml', 'rb') as configFile:
    config = toml.load(configFile)

thingName = config["thing"]["targetName"]
server = config["server"]["ip"]
port = config["server"]["port"]
keepalive = config["server"]["keepalive"]
print("Connecting to :" + server + " on port " + str(port))
mqttc.connect(server, port, keepalive)
mqttc.subscribe(thingName+"/reply", 0)
mqttc.subscribe(thingName+"/error", 0)
mqttc.loop_start()


# Use the tab key for completion
if "libedit" in readline.__doc__: # FOR MAC OS X
    readline.parse_and_bind("bind ^I rl_complete")
else: # LINUX UNIX
    readline.parse_and_bind('tab: complete')

# Prompt the user for text
input_loop()

