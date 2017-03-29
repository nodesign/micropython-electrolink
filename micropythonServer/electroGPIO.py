# This is port of Electrolink for micropython for ESP8266 processor
# This is board specific file that has to be edited to support board native functions
from machine import Pin, PWM

# 16 GPIO of ESP board
# Pin objects are stored here once they have been initialized
pins = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]

def pwmStart(arg):
    pwmNb = arg[0]
    frequence = arg[1]

    pwm = PWM(Pin(pwmNb))
    pwm.freq(frequence)
    pins[pwmNb] = pwm

def pwmSet(arg):
    pwmNb = arg[0]
    duty = arg[1]
    
    pins[pwmNb].duty(duty)

def pwmStop(arg):
    pwmNb = arg[0]
    
    pins[pwmNb].deinit()
    pins[pwmNb] = None


# digital GPIO
def pinMode(arg):
    pinId = arg[0]
    mode = arg[1]
    
    gpio = None
    if (mode is 0):
        mode = Pin.OUT
        gpio = Pin(pinId, mode)
    elif(mode is 1):
        mode = Pin.IN
        gpio = Pin(pinId, mode)
    elif(mode is 2):
        mode = Pin.PULL_UP
        gpio = Pin(pinId, Pin.IN, Pin.PULL_UP)
    else:
        print("Mode not supported in hardware")
    pins[pinId] = gpio

def digitalWrite(arg):
    pinId = arg[0]
    value = arg[1]
    
    pins[pinId].value(value)

def digitalRead(arg):
    pinId = arg[0]
    return pins[pinId].value()

callbacks = {
      "pwmStart":     {"call": pwmStart,     "parameters": "pinNumber, frequency",  "description": "Start PWM signal on pin with frequency"},
      "pwmSet":       {"call": pwmSet,       "parameters": "pinNumber, duty",       "description": "Set PWM duty cycle 0-1023"}, 
      "pwmStop":      {"call": pwmStop,      "parameters": None,                    "description": "Stop PWM signal"},
      "pinMode":      {"call": pinMode,      "parameters": "pinNumber, mode",       "description": "Set pin to IN/OUT and PULL_UP/DOWN modes"},
      "digitalWrite": {"call": digitalWrite, "parameters": "pinNumber, value",      "description": "Set voltage level on pin, 1 -> 3.3V, 0 -> 0V"},
      "digitalRead":  {"call": digitalRead,  "parameters": "pinNumber, callbackId", "description": "Read digital value from pin. Callback Id will be mirrored"}
      }