# 16 GPIO of ESP board
# Pin objects are stored here once they have been initialized
pins = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]

def pwmStart(arg):
    pwmNb = arg[0]
    frequence = arg[1]
    print("pwmStart", pwmNb, frequence)

def pwmSet(arg):
    pwmNb = arg[0]
    duty = arg[1]
    print("pwmSet",pwmNb, duty)

def pwmStop(arg):
    pwmNb = arg[0]
    print("pwmStop",pwmNb)

# digital GPIO
def pinMode(arg):
    pinId = arg[0]
    mode = arg[1]
    print("pinMode",pinId, mode)

def digitalWrite(arg):
    pinId = arg[0]
    value = arg[1]
    print("digitalWrite",pinId, value)

def digitalRead(arg):
    pinId = arg[0]
    print("digitalRead", pinId, "returns 1")
    return 1

spells = {
      "pwmStart": pwmStart, 
      "pwmSet": pwmSet, 
      "pwmStop": pwmStop,
      "pinMode": pinMode,
      "digitalWrite": digitalWrite,
      "digitalRead": digitalRead}