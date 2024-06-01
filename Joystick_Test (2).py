from smbus import SMBus
#from gpiozero import PWMLED
from gpiozero import Button
from time import sleep
from signal import signal, SIGTERM, SIGHUP, pause

bus = SMBus(1)
button1 = Button(27)
button2 = Button(22)
button3 = Button(5)
#ledX = PWMLED(26)
#ledY = PWMLED(20)
valueX = 128
valueY = 128

def giveCoords():
    return [(-read_ads7830(0) + 128) * bool(abs(-read_ads7830(0) + 128) > 10), (-read_ads7830(1) + 128) * bool(abs(-read_ads7830(1) + 128) > 10)]

ads7830_commands = [0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4]
def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    return bus.read_byte(0x4b)

def giveButton():
    return button1.is_pressed

def giveBackButton():
    return button3.is_pressed