from machine import Pin, PWM
from time import sleep_ms
#from math import exp
from machine import Timer

class Lamp:
    def __init__(self, pin_n, frequency = 120):
        pin = Pin(pin_n, Pin.OUT)
        self.pwm0 = PWM(pin)
        self.upperLimit = 1023
        self.pwm0.freq(frequency)
        self.fader = [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                        0,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  3,  3,
                        3,  3,  4,  4,  4,  5,  5,  5,  6,  6,  7,  7,  7,  8,  8,  9,
                        10, 10, 11, 11, 12, 13, 13, 14, 15, 15, 16, 17, 18, 19, 20, 20,
                        21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 35, 36, 37, 38,
                        40, 41, 43, 44, 46, 47, 49, 50, 52, 54, 55, 57, 59, 61, 63, 64,
                        66, 68, 70, 72, 74, 77, 79, 81, 83, 85, 88, 90, 92, 95, 97,100,
                        102,105,107,110,113,115,118,121,124,127,130,133,136,139,142,145,
                        149,152,155,158,162,165,169,172,176,180,183,187,191,195,199,203,
                        207,211,215,219,223,227,232,236,240,245,249,254,258,263,268,273,
                        277,282,287,292,297,302,308,313,318,323,329,334,340,345,351,357,
                        362,368,374,380,386,392,398,404,410,417,423,429,436,442,449,455,
                        462,469,476,483,490,497,504,511,518,525,533,540,548,555,563,571,
                        578,586,594,602,610,618,626,634,643,651,660,668,677,685,694,703,
                        712,721,730,739,748,757,766,776,785,795,804,814,824,833,843,853,
                        863,873,884,894,904,915,925,936,946,957,968,979,990,1001,1012,1023]

        self.current = 0 # 0-255
        self.target = 0

        self.permanentTimer = True
        self.timer = None

        self.callbacks = {
              "getLight":      {"call": self.getLight,     "parameters": None,                       "description": "Get current light intensity 0-255"},
              "setLight":      {"call": self.setLight,     "parameters": "value",                    "description": "Set current light intensity 0-255"}, 
              "fadeinLight":   {"call": self.fadeinLight,  "parameters": "delay_ms",                 "description": "Blocking function. Fade in light. Set delay between steps"},
              "fadeoutLight":  {"call": self.fadeoutLight, "parameters": "delay_ms",                 "description": "Blocking function. Fade out light. Set delay between steps"},
              "fade":          {"call": self.fade,         "parameters": "value, delay_ms",          "description": "Set fade to target value and delay between steps, Fade target 0-255"},
              "startTimer":    {"call": self.startTimer,   "parameters": "delay_ms, permanent=True", "description": "Set delay between steps, Permanent (optional) will it fade automaticaly for each new target. Non blocking fader"},
              "setTarget":     {"call": self.setTarget,    "parameters": "value",                    "description": "Set target to fade to. If start timer activated it will fade automaticaly"},
              "endTimer":      {"call": self.endTimer,     "parameters": None,                       "description": "Kill timer"},
              }

    def getLight(self, arg):
        return self.current

    def setLight(self, arg):
        value = arg[0]
        self.lighting = value
        self.current = value
        # force target to current value
        self.target = self.current

# SYNC BLOCKING FUCNTIONS
    def fadeinLight(self, arg):
        delay_ms = arg[0]
        for a in range(256):
            self.lighting(a)
            sleep_ms(delay_ms)

    def fadeoutLight(self, arg):
        delay_ms = arg[0]
        for a in range(256):
            self.lighting(255-a)
            sleep_ms(delay_ms)

    def fade(self,arg):
        val = arg[0]
        delay_ms = arg[1]

        delta = abs(val - self.current)
        if (val > self.current):
            for a in range(delta):
                self.lighting(self.current+1)
                sleep_ms(delay_ms)
        elif (val < self.current):
            for a in range(delta):
                self.lighting(self.current-1)
                sleep_ms(delay_ms)

# ASYNC FUCNTIONS

    def startTimer(self, arg):
        delay_ms = arg[0]
        permanent = True

        if (len(arg)>1):
            permanent = arg[1]

        self.timer = Timer(-1)
        self.timer.init(period=delay_ms, mode=Timer.PERIODIC, callback=lambda t:self.a_fade())
        self.permanentTimer = permanent

# a_fade is pricvate function
    def a_fade(self):
        if (self.target > self.current):
            self.lighting(self.current+1)
            return 0
        elif (self.target < self.current):
            self.lighting(self.current-1)
            return 0
        elif (self.target == self.current):
            if (self.permanentTimer == False):
                if not(self.timer is None):
                    self.timer.deinit()
                    self.timer = None
            return 1

    def setTarget(self, arg):
        t = arg[0]
        self.target = t

    def endTimer(self, arg):
        if not(self.timer is None):
            self.timer.deinit()

# LOW LEVEL PRIVATE FUNCTION
    def lighting(self, value): # 0-255 with curve correction
        self.pwm0.duty(self.fader[value]) # apply correction for humain eyes
        self.current = value

# Processing code to calculate gamma
# float gamma   = 2.8; // Correction factor
# int   max_in  = 255, // Top end of INPUT range
#       max_out = 1023; // Top end of OUTPUT range
# void setup() {
#   print("{");
#   for(int i=0; i<=max_in; i++) {
#     if(i > 0) print(',');
#     if((i & 15) == 0) print("\n  ");
#     System.out.format("%3d",
#       (int)(pow((float)i / (float)max_in, gamma) * max_out + 0.5));
#   }
#   println(" };");
#   exit();
# }