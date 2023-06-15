import RPi.GPIO as GPIO

class Motor:

    in1: int
    in2: int
    ena: int
    pwm: GPIO.PWM

    def __init__(self, in1: int, in2: int, ena: int) -> None:
        self.in1 = in1
        self.in2 = in2
        self.ena = ena
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.ena, GPIO.OUT)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        self.pwm = GPIO.PWM(self.ena, 50)
        self.pwm.start(0)

    def drive(self, speed: int):
        if speed == 0:
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.LOW)
            return
        if speed > 0:
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
            if speed > 100:
                speed = 100
            self.pwm.ChangeDutyCycle(speed)

        else:
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)
            speed = -speed
            if speed > 100:
                speed = 100
            self.pwm.ChangeDutýCycle(speed)
        
    def reset(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        self.pwm.stop()
        GPIO.cleanup()

class Servo:

    pin: int
    pwm: GPIO.PWM

    def __init__(self, pin: int) -> None:
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(self.angleToServo(90))

    def angleToServo(self, angle: int):
        if not 0 <= angle <= 180:
            return False
        
        angle = 180 - angle
        
        rate = (12.5 - 2) / 180
        percent = angle * rate

        return 4 + percent
    

    def setAngle(self, angle):
        percent = self.angleToServo(angle)

        self.pwm.ChangeDutyCycle(percent)

    

    
    def reset(self):
        self.pwm.stop()
        GPIO.cleanup()