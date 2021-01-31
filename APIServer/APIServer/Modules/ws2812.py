import neopixel
import board

from .command_api import *
from .APIClasses import AbstractPeripheral, AbstractParameter
from time import sleep

import asyncio


class WS2812Strip(AbstractPeripheral):
    
    @classmethod
    async def Create(
        cls,
        pin_number,
        numleds: int,
        periph_name: str,
        periph_id: int,
        periph_type: int,
    ):

        self = WS2812Strip(periph_name, periph_id, periph_type)
        super().__init__(self, periph_name, periph_id, periph_type)
        self.numleds = numleds

        self.modes = [
            {
                "name": "all_off",
                "index": 0,
                "func": self.all_off,
                "refresh_t": 0,
                "async": 0,
            },
            {
                "name": "single_colour",
                "index": 1,
                "func": self.set_all_colour,
                "refresh_t": 0,
                "async": 0,
            },
            {
                "name": "rainbow",
                "index": 2,
                "func": self.rainbow_cycle,
                "refresh_t": 0.1,
                "async": 1,
            },
        ]

        self.pin_number = pin_number
        self.brightness = 0.1
        self.colour = 0xFF0000
        self.ORDER = neopixel.GRB
        self.mode = 0
        self.parameters = [
            {
                "name": "numleds",
                "param_id": 0x01,
                "data_type": PARAMTYPE_UINT16,
                "p_max": 0,
                "methods": (API_GET_MASK),
                "get_func": self.get_numleds,
                "set_func": None,
                "act_func": None,
            },
            {
                "name": "mode",
                "param_id": 0x02,
                "data_type": PARAMTYPE_UINT8,
                "p_max": len(self.modes),
                "methods": (API_GET_MASK | API_SET_MASK),
                "get_func": self.get_mode,
                "set_func": self.set_mode,
                "act_func": None,
            },
            {
                "name": "colour",
                "param_id": 0x03,
                "data_type": PARAMTYPE_UINT32,
                "p_max": 0xFFFFFF,
                "methods": (API_GET_MASK | API_SET_MASK),
                "get_func": self.get_colour,
                "set_func": self.set_colour,
                "act_func": None,
            },
            {
                "name": "brightness",
                "param_id": 0x04,
                "data_type": PARAMTYPE_UINT8,
                "p_max": 100,
                "methods": (API_GET_MASK | API_SET_MASK),
                "get_func": self.get_brightness,
                "set_func": self.set_brightness,
                "act_func": None,
            },
        ]


        self.num_params = len(self.parameters)
        self.update = asyncio.Event()
        self.strip = neopixel.NeoPixel(
            self.pin_number, self.numleds, brightness=0.1, auto_write=False
        )
        self.delay = 1
        self.task = self.run_task
        return self


    def update_leds(self):
        self.update.set()
        return

    async def run_task(self):
        """ this task runs in order to periodically refresh leds """
        """ can wait for a sync primitive?                       """
        print("Running Task...")
        try:
            while(1):
                ## get info
                func = self.modes[self.mode]["func"]
                self.delay = self.modes[self.mode]["refresh_t"]
                bright = self.brightness
                colour = self.colour
                asyn = self.modes[self.mode]["async"]
                has_run = 0

                ## animation loop
                while 1:
                    if asyn:
                        await func()
                    if has_run == 0:
                        if asyn:
                            await func()
                        else:
                            print("running new")
                            func()
                        has_run = 1                

                    if not asyn:                    
                        if self.delay:
                            await asyncio.sleep(self.delay)
                        else:
                            await asyncio.sleep(0.5)

                    if self.update.is_set():
                        # update: restart animation loop
                        print("updating")
                        self.update.clear()
                        break

        except asyncio.CancelledError:
            print("Task closing")
            return

    def get_colours(self):

        g = (self.colour & 0xff)
        r = (self.colour & 0xff00) >> 8
        b = (self.colour & 0xff0000) >> 16

        return (r, g, b)

    def set_all_colour(self):
        r,g,b = self.get_colours()
        self.strip.fill((r,g,b))
        self.strip.show()

    def all_off(self):
        for i in range(self.numleds):
            self.strip[i] = (0, 0, 0)
        self.strip.show()

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) if self.ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

    async def rainbow_cycle(self):
        for j in range(255):
            for i in range(self.numleds):
                pixel_index = (i * 256 // self.numleds) + j
                self.strip[i] = self.wheel(pixel_index & 255)
            self.strip.show()
            await asyncio.sleep(self.delay)

    def get_numleds(self):
        print("getting numleds")
        return 1, self.numleds

    def set_mode(self, mode):
        if mode > len(self.modes) - 1:
            return -1
        else:
            self.mode = mode
            print("updating leds")
            self.update_leds()
            return 1

    def get_mode(self):
        return 1, self.mode

    def get_brightness(self):
        return 1, self.brightness * 100

    def set_brightness(self, brt):
        if brt > 100:
            return -1
        else:
            self.strip.brightness = brt / 100
            self.update_leds()
            return 1

    def get_colour(self):
        return 1, self.colour

    def set_colour(self, colour):
        if colour > 0xFFFFFF:
            return -1
        else:
            self.colour = colour
            self.update_leds()
            return 1

# async def main():

#     leds = await WS2812Strip.Create(board.D18, 21, "leds", 0x0A, PTYPE_ADDR_LEDS)
#     leds.set_all_colour()

#     while(1):
#         await asyncio.sleep(1)

# if __name__ == "__main__":
#     asyncio.run(main())