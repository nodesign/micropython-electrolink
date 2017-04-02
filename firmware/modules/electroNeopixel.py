from machine import Pin, PWM
from neopixel import NeoPixel
from time import sleep, sleep_ms


class Lamp:

    def __init__(self, n_pin, n_leds):
        self.LEDS = n_leds
        self.LED_MIDDLE = self.LEDS/2

        # NEOPIXEL output pin
        pin = Pin(n_pin, Pin.OUT, Pin.PULL_UP)
        self.np = NeoPixel(pin, LEDS)

        for i in range(LEDS):
            self.np[i] = (0,0,0)
            self.np.write()

        self.eyeCorrection = [  0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 
                                2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 
                                4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 
                                7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 10, 10, 10, 10, 11, 11, 
                                11, 12, 12, 12, 13, 13, 13, 14, 14, 15, 15, 15, 16, 16, 17, 17, 
                                17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 23, 24, 24, 25, 
                                25, 26, 26, 27, 28, 28, 29, 29, 30, 31, 31, 32, 32, 33, 34, 34, 
                                35, 36, 37, 37, 38, 39, 39, 40, 41, 42, 43, 43, 44, 45, 46, 47, 
                                47, 48, 49, 50, 51, 52, 53, 54, 54, 55, 56, 57, 58, 59, 60, 61, 
                                62, 63, 64, 65, 66, 67, 68, 70, 71, 72, 73, 74, 75, 76, 77, 79, 
                                80, 81, 82, 83, 85, 86, 87, 88, 90, 91, 92, 94, 95, 96, 98, 99, 
                                100, 102, 103, 105, 106, 108, 109, 110, 112, 113, 115, 116, 118, 120, 121, 123, 
                                124, 126, 128, 129, 131, 132, 134, 136, 138, 139, 141, 143, 145, 146, 148, 150, 
                                152, 154, 155, 157, 159, 161, 163, 165, 167, 169, 171, 173, 175, 177, 179, 181, 
                                183, 185, 187, 189, 191, 193, 196, 198, 200, 202, 204, 207, 209, 211, 214, 216, 
                                218, 220, 223, 225, 228, 230, 232, 235, 237, 240, 242, 245, 247, 250, 252, 255]
    self.callbacks = {
          "setPixelColor":     {"call": self.setPixelColor,     "parameters": "nLed, #hexColor",                               "description": "Set one pixel color (hex format)"},
          "setAllPixelsColor": {"call": self.setAllPixelsColor, "parameters": "#hexColor",                                     "description": "Set all pixel colors (hex format)"}, 
          "morphColors":       {"call": self.morphColors,       "parameters": "#hexColor, delay_ms",                           "description": "Morph each pixel to target color (hex format). Set delay between steps"},
          "fadeinFromMiddle":  {"call": self.fadeinFromMiddle,  "parameters": "delay_ms, #hexColor=#FFFFFF",                   "description": "Fade in animation, Set delay between steps, target color is white by default, can be overriden"},
          "fadeoutFromMiddle": {"call": self.fadeoutFromMiddle, "parameters": "delay_ms",                                      "description": "Fade out animation"},
          "gradientSimple":    {"call": self.gradientSimple,    "parameters": "#fromHexColor, #toHexColor",                    "description": "Set gradient from one color (hex format) to another"},
          "gradient":          {"call": self.gradient,          "parameters": "#startHexColor, #targetHexColor, #endHexColor", "description": "Set complex gradient from one color (hex format) to target color to end color. Position of middle target color is expressed in percents"}
          }

    def setPixelColor(self, arg):
        n = arg[0]
        hexy = arg[1]
        rgb = self.hex_to_rgb(hexy)
        self.np[n] = self.eyeCorrectRgb(rgb)

    def setAllPixelsColor(self, arg):
        hexy = arg[0]
        rgb = self.hex_to_rgb(hexy)
        t_color = self.eyeCorrectRgb(rgb)
        for a in range(self.LEDS):
            self.np[a] = t_color
        self.np.write()

    def morphColors(self, arg):
        tC = arg[0]
        delay_ms = arg[1]
        step = 1
        if (len(arg)>2):
            step = arg[2]

        targetColor = self.hex_to_rgb(tC)
        for a in range(0, 101, step):
            t = a/100.0
            for i in range(self.LEDS):
                c = self.lerpColor(self.np[i], targetColor, t)
                self.np[i] = self.eyeCorrectRgb(c)
            self.np.write()
            sleep_ms(delay_ms)

    def fadeinFromMiddle(self, arg):
        delay_ms = arg[0]
        color = "#FFFFFF"
        if (len(arg)>1):
            color = arg[1]

        c = self.hex_to_rgb(color)
        cc = self.eyeCorrectRgb(c)
        for a in range(self.LED_MIDDLE+1):
            self.np[21-a] = cc
            self.np[20+a] = cc
            self.np.write()
            sleep_ms(delay_ms)

    def fadeoutFromMiddle(self, arg):
        delay_ms = arg[0]

        for a in range(self.LED_MIDDLE+1):
            self.np[a] = (0, 0, 0)
            self.np[(self.LEDS-1)-a] = (0, 0, 0)
            self.np.write()
            sleep_ms(delay_ms)

    def gradientSimple(self, arg):
        c1hex = arg[0]
        c2hex = arg[1]
        c1 = self.hex_to_rgb(c1hex)
        c2 = self.hex_to_rgb(c2hex)

        for a in range(self.LEDS):
            t = (1.0/self.LEDS)*a
            color = self.lerpColor(c1,c2,t)
            self.np[a] = self.eyeCorrectRgb(color)
        self.np.write()


    def gradient(self, arg):

        startColor =     arg[0]
        targetColor =    arg[1]
        endColor =       arg[2]
        targetPosition = arg[3] # position in %

        startC = self.hex_to_rgb(startColor)
        targetC = self.hex_to_rgb(targetColor)
        endC = self.hex_to_rgb(endColor)

        # start to target
        ledTargetPos = int((self.LEDS/100.0)*targetPosition)

        for a in range(ledTargetPos):
            t = (1.0/ledTargetPos)*a
            color = self.lerpColor(startC,targetC,t)
            self.np[a] = self.eyeCorrectRgb(color)

        deltaLed = self.LEDS-ledTargetPos
        for a in range(ledTargetPos, self.LEDS):
            t = (1.0/deltaLed)*(a-ledTargetPos)
            color = self.lerpColor(targetC,endC,t)
            self.np[a] = self.eyeCorrectRgb(color)
        self.np.write()

# PRIVATE FUNCTIONS
    def hex_to_rgb(self, value):
        """Return (red, green, blue) for the color given as #rrggbb."""
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def lerpColor(c1, c2, amt):
        """Return (red, green, blue) for two colors given as tuples and amt between 0.0 - 1.0"""
        if (amt < 0.0):
            amt = 0.0
        if (amt > 1.0):
            amt = 1.0

        r1 = c1[0]
        g1 = c1[1]
        b1 = c1[2]

        r2 = c2[0]
        g2 = c2[1]
        b2 = c2[2]

        r = int(r1 + (r2-r1)*amt)
        g = int(g1 + (g2-g1)*amt)
        b = int(b1 + (b2-b1)*amt)

        return (r,g,b)

    def eyeCorrectRgb(self, rgb_tuple):
        r = self.eyeCorrection[rgb_tuple[0]]
        g = self.eyeCorrection[rgb_tuple[1]]
        b = self.eyeCorrection[rgb_tuple[2]]
        return (r,g,b)

