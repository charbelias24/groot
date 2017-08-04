import RPi.GPIO as GPIO
#from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 

#initializing the used GPIO's
valve1E = 16
valve1A = 12

valve2E = 4
valve2A = 3

pumpE = 13
pumpA = 6

fan1E = 20
fan1A = 21

fan2E = 7
fan2A = 8

#setting up the useed GPIO's
GPIO.setup(valve1E,GPIO.OUT)
GPIO.setup(valve1A,GPIO.OUT)

GPIO.setup(valve2E,GPIO.OUT)
GPIO.setup(valve2A,GPIO.OUT)

GPIO.setup(pumpE,GPIO.OUT)
GPIO.setup(pumpA,GPIO.OUT)

GPIO.setup(fan1E,GPIO.OUT)
GPIO.setup(fan1A,GPIO.OUT)

GPIO.setup(fan2E,GPIO.OUT)
GPIO.setup(fan2A,GPIO.OUT)


def valve1_on():
    GPIO.output(valve1A,GPIO.HIGH)
    GPIO.output(valve1E,GPIO.HIGH)
    print ("Valve 1: ON")

def valve1_off():
    GPIO.output(valve1E,GPIO.LOW)
    print ("Valve 1: OFF")

def valve2_on():
    GPIO.output(valve2A,GPIO.HIGH)
    GPIO.output(valve2E,GPIO.HIGH)
    print ("Valve 2: ON")

def valve2_off():
    GPIO.output(valve2E,GPIO.LOW)
    print ("Valve 2: OFF")


def pump_on():
    GPIO.output(pumpA,GPIO.HIGH)
    GPIO.output(pumpE,GPIO.HIGH)
    print("Pump: ON")

def pump_off():
    GPIO.output(pumpE,GPIO.LOW)
    print("Pump: OFF")

def fan1_on():
    GPIO.output(fan1E,GPIO.HIGH)
    GPIO.output(fan1A,GPIO.HIGH)
    print("Fan 1: ON")

def fan1_off():
    GPIO.output(fan1E,GPIO.LOW)
    print("Fan 1: OFF")    

def fan2_on():
    GPIO.output(fan2E,GPIO.HIGH)
    GPIO.output(fan2A,GPIO.HIGH)
    print("Fan 2: ON")

def fan2_off():
    GPIO.output(fan2E,GPIO.LOW)
    print("Fan 2: OFF")
'''
valve2_on()
sleep(2)
valve2_off()
sleep(2)
valve1_on()
sleep(2)
valve1_off()
sleep(2)
pump_on()
sleep(2)
pump_off()
sleep(2)
fan1_on()
sleep(2)
fan1_off()
sleep(2)
fan2_on()
sleep(2)
fan2_off()'''

