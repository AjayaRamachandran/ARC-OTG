from smbus import SMBus
#from gpiozero import PWMLED
from gpiozero import Button
from time import sleep
from signal import signal, SIGTERM, SIGHUP, pause

bus = SMBus(1)
button1 = Button(27)
button2 = Button(22)
#ledX = PWMLED(26)
#ledY = PWMLED(20)
valueX = 128
valueY = 128

def giveCoords():
    #global valueX, valueY
    #print(valueX)
    #print(valueY)
    #print(read_ads7830(0), read_ads7830(1))
    return [(read_ads7830(0) - 128) * bool(abs(read_ads7830(0) - 128) > 10), (-read_ads7830(1) + 128) * bool(abs(-read_ads7830(1) + 128) > 10)]
    #return [-(int(valueX) - 128), (int(valueY) - 128)]
    #return [0,0]

def giveButton():
    return False
    #return pygame.mouse.get_pressed()[0]

def safe_exit(signum, frame):
    exit(1)
    
ads7830_commands = [0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4]
def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    return bus.read_byte(0x4b)

def values(inputX, inputY):
    global valueX, valueY
    if button1.is_pressed:
        print("You hit the shut-down button")
        exit()
    if button2.is_pressed:
        print("2")
    '''if button.is_held:
        print("fortnite")'''
        
    valueX = read_ads7830(inputX)
    valueY = read_ads7830(inputY)
    
    #ledX.value = valueX/255
    #ledY.value = valueY/255
    
    sleep(0.05)
    
signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)
'''
def close_everything():
    ledX.close()
    ledY.close()'''

'''
try:
    #values(0, 1, ledX, ledY)
    #pause()
except KeyboardInterrupt:
    pass
finally:
    ledX.close()
    ledY.close()
    '''