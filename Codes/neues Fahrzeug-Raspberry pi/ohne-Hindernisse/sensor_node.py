import RPi.GPIO as GPIO
from smbus2.smbus2 import SMBus
import time
import math


class Ultraschall:
    pinTrigger: int
    pinEcho: int

    def __init__(self, trigger: int, echo: int):
        self.pinTrigger = trigger
        self.pinEcho = echo
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pinTrigger, GPIO.OUT)
        GPIO.setup(self.pinEcho, GPIO.IN)

    def getDistance(self) -> float:
        GPIO.output(self.pinTrigger, True)
        time.sleep(0.00001)
        GPIO.output(self.pinTrigger, False)

        start = time.time()
        end = start

        backup = start + 0.25

        while (GPIO.input(self.pinEcho) == 0):
            if backup < start:
                return None
            start = time.time()

        backup = start + 0.25

        while (GPIO.input(self.pinEcho) == 1):
            if backup < end:
                return None
            end = time.time()

        diff = end - start

        distance = (diff * 34300) / 2

        distance = round(distance * 10) / 10

        return distance

    def reset(self):
        GPIO.cleanup()


class Compass:
    bus: SMBus
    address: int
    start_position: int

    def __init__(self, mode: int, address: int):
        self.bus = SMBus(mode)
        self.address = address

    def setStartPosition(self):
        self.start_position = self.getRotation(1)

    def calculateZero(self, rotation: int):
        rotation = (rotation - self.start_position) + 5400
        rotation = (rotation % 3600) - 1800
        return rotation

    def getRotation(self, factor: int):
        high = self.bus.read_byte_data(self.address, 2)
        low = self.bus.read_byte_data(self.address, 3)
        rotation = high
        rotation <<= 8
        rotation += low

        return int(rotation * factor)

    def getFixedRotation(self, factor: int = 1) -> int:
        return int(self.calculateZero(self.getRotation(1)) * factor)
    
    def getDriveRotation(self):
        rot = self.getFixedRotation(0.01)
        return rot % 36
    
    def getAntiDriveRotation(self):
        rot = self.getDriveRotation()
        if rot != 0:
                rot = 36 - rot
        return rot


class Taster:

    pin: int

    def __init__(self, pin: int) -> None:
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def isPressed(self):
        if GPIO.input(self.pin) == 1:
            return True
        return False