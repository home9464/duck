"""The Xbox controller

1. it was not started
2. powered off after connection

devadm info --query=property --name=/dev/input/event4 | grep "ID_INPUT_JOYSTICK=1"


DEVPATH=/devices/platform/soc/fe201000.serial/tty/ttyAMA0/hci0/hci0:11/0005:045E:02E0.000A/input/input11/event4
DEVNAME=/dev/input/event4
MAJOR=13
MINOR=68
SUBSYSTEM=input
USEC_INITIALIZED=6836871854
ID_INPUT=1
ID_INPUT_JOYSTICK=1
ID_INPUT_KEY=1
ID_BUS=bluetooth
XKBMODEL=pc105
XKBLAYOUT=us
BACKSPACE=guess
ID_INPUT_JOYSTICK_INTEGRATION=external
ID_PATH=platform-soc
ID_PATH_TAG=platform-soc
ID_FOR_SEAT=input-platform-soc
LIBINPUT_DEVICE_GROUP=5/45e/2e0:dc:a6:32:65:d4:45
LIBINPUT_FUZZ_00=255
LIBINPUT_FUZZ_01=255
TAGS=:uaccess:power-switch:seat:


"""
import asyncio
import random
import math
from typing import AnyStr, Callable

from evdev import  InputDevice
from transmiter import transmit


STICK_OR_PAD_TYPE = 3
CODE_LEFT_STICK_VERTICAL = 0
CODE_LEFT_STICK_HORIZONTAL = 1

CODE_RIGHT_STICK_VERTICAL = 3
CODE_RIGHT_STICK_HORIZONTAL = 4

CODE_PAD_HORIZONTAL = 16
CODE_PAD_VERTICAL = 17

CODE_BUTTON_A = 304  # value 0 or 1
CODE_BUTTON_B = 305  # value 0 or 1
CODE_BUTTON_X = 306  # value 0 or 1
CODE_BUTTON_Y = 307  # value 0 or 1

CODE_BUTTON_LEFT_BUMPER = 308
CODE_BUTTON_RIGHT_BUMPER = 309
CODE_BUTTON_LEFT_BUMPER = 308
CODE_BUTTON_RIGHT_BUMPER = 309

CODE_BUTTON_LEFT_SHOULDER = 310  # value 0 or 1
CODE_BUTTON_RIGHT_SHOULDER = 311  # value 0 or 1

CODE_LEFT_TRIGGER = 2  # value 0-1023
CODE_RIGHT_TRIGGER = 5  # value 0-1023


class Controller:
    def __init__(self, debug=True):
        self._wait_until_connected()
        #self.events_callback = {'drive':[], 'servo0':[], 'servo1':[]}
        self.events_callback = {'stick':[], 'button':[]}
        self.events_value = {'stick':0, 'button': 0}
        self.debug = debug
        self.is_deployed = False

    def _find_input_device(self):
        """
        multiple devices may present. e.g. a wireless mouse receiver.
        find the correct device.

        udevadm info --query=property --name=/dev/input/event4 | grep "ID_INPUT_JOYSTICK=1"
        """

    def _wait_until_connected(self):
        self.controller = None
        while self.controller is None:
            try:
                self.controller = InputDevice('/dev/input/event2')
            except OSError as e:
                self.controller = None
        print(f'Controller connected: {self.controller}')

    def move(self, direction):
        transmit(f'D:{direction}')
        print(f'move: {direction}')

    def deploy(self, flag):
        angle = 180 if flag == 1 else 0
        transmit(f'A:{angle}')
        print(f'deploy: {angle}')


    def register(self, event:str, callback:Callable):
        """
        run callback() when event happens.
        """
        if event in self.events_callback and callback not in self.events_callback[event]:
            self.events_callback[event].append(callback)

    def unregister(self, event, callback):
        """
        remove callback()
        """
        if event in self.events_callback and callback in self.events_callback[event]:
            self.events_callback[event].remove(callback)

    async def start(self):
        # non-blocking
        while True:
            try:
                async for event in self.controller.async_read_loop():
                    if event.code == 0 and event.type == 0 and event.value== 0:
                        continue
                    if self.debug:
                        print(f'code: {event.code}, type: {event.type}, value: {event.value}')

                    #if  event.code == CODE_LEFT_STICK_VERTICAL or event.code == CODE_LEFT_STICK_HORIZONTAL:
                    if  event.code == CODE_RIGHT_STICK_VERTICAL or event.code == CODE_RIGHT_STICK_HORIZONTAL:
                        intval = int(event.value)
                        absval = abs(intval) + 1
                        logval = round(-math.log(absval) if intval < 0 else math.log(absval), 2)
                        print(f'code: {event.code}, value: {logval}')

                    if  event.code == CODE_PAD_HORIZONTAL or event.code == CODE_PAD_VERTICAL:
                        # either x!=0 or y!=0 or both != 0
                        x = event.value if event.code == CODE_PAD_HORIZONTAL else 0
                        y = event.value if event.code == CODE_PAD_VERTICAL else 0
                        direction = 0
                        if x == 0:  # y != 0
                            if y == -1:
                                direction = 1  # 'up'
                            elif y == 1:
                                direction = 2  # 'down'
                            else:
                                pass
                        elif y == 0:  # x != 0
                            if x == -1:
                                direction = 3  # 'left'
                            elif x == 1:
                                direction = 4  # 'right'
                            else:
                                pass
                        else:  # x != 0 and y != 0
                            if x == -1 and y == -1:  # up-left
                                direction = 5  # 'up-left'
                            elif x == -1 and y == 1:  # up-right
                                direction = 6  # 'up-right'
                            elif x == 1 and y == -1:  # down-left
                                direction = 7  # 'down-left'
                            else:
                                direction = 8  # 'down-right'
                        #driver.drive(direction)
                        #print('Direction:', direction)
                        #self.events_value['stick'] = direction
                        self.move(direction)

                    if  event.code == CODE_BUTTON_A and event.value == 1:  # A button is pressed
                        self.is_deployed = 1 - self.is_deployed
                        self.deploy(self.is_deployed)
                    '''
                    for evt, callbacks in self.events_callback.items():
                        for cb in callbacks:
                            if self.events_value[evt] != 0:
                                cb(self.events_value[evt])
                                self.events_value[evt] = 0
                    '''
                await asyncio.sleep(0)
            except OSError as e:  # when controller was poweroff
                print('Controller not connected')
                self._wait_until_connected()
        def close(self):
            pass

async def main():
    controller = Controller()
    #controller.register('stick', drive)
    #controller.register('button', deploy)
    try:
        await asyncio.gather(await controller.start())
    except Exception as e:
        print(e)
    finally:
        pass

if __name__ == '__main__':
    asyncio.run(main())