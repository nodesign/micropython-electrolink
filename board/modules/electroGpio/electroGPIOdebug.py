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

callbacks = {
      "pwmStart":     {"call": pwmStart,     "parameters": "pinNumber, frequency",  "description": "Start PWM signal on pin with frequency"},
      "pwmSet":       {"call": pwmSet,       "parameters": "pinNumber, duty",       "description": "Set PWM duty cycle 0-1023"}, 
      "pwmStop":      {"call": pwmStop,      "parameters": None,                    "description": "Stop PWM signal"},
      "pinMode":      {"call": pinMode,      "parameters": "pinNumber, mode",       "description": "Set pin to IN/OUT and PULL_UP/DOWN modes"},
      "digitalWrite": {"call": digitalWrite, "parameters": "pinNumber, value",      "description": "Set voltage level on pin, 1 -> 3.3V, 0 -> 0V"},
      "digitalRead":  {"call": digitalRead,  "parameters": "pinNumber, callbackId", "description": "Read digital value from pin. Callback Id will be mirrored"}
      }