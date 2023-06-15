import RPi.GPIO as GPIO

from sensor_node import Ultraschall, Compass, Taster
from control_node import Motor, Servo

import time



def fahren():
    try:
        GPIO.cleanup()
    except:
        print("nothing to clean")
    
    ultra1 = Ultraschall(16, 13)    # rechts
    ultra2 = Ultraschall(21, 26)    # links
    ultra3 = Ultraschall(20, 19)    # vorne
    servo = Servo(12)
    motor = Motor(7, 1, 8)
    taster1 = Taster(24)            # rechts
    taster2 = Taster(23)            # links
    kompass = Compass(1, 0x60)
    kompass.setStartPosition()

    runde = 0
    rundenCache = 0
    rundenSperre = False
    rundenToleranz = 33     # toleranz, ab wann runde + 1
    final = 0

    uhrzeigersinn = None

    endDelay = 0        # in sekunden
    endDistance = 150   # in cm

    print(5*"\n")

    print("Warter auf Start...")
    print()
    while uhrzeigersinn == None:
        print("-> Distanz:", ultra1.getDistance(), "\tKompass:", kompass.getDriveRotation(), "\t      ")
        print()
        print("<- Distanz:", ultra2.getDistance(), "\tKompass:", kompass.getAntiDriveRotation(), "\t      ")
        print("\n")
        print(end = "\033[F\033[A\033[A\033[A\033[A")

        if taster1.isPressed():
            uhrzeigersinn = True
        if taster2.isPressed():
            uhrzeigersinn = False

    kompass.setStartPosition()
    
    print("Starte!")
    print(3*"\n")

    motor.drive(25)
    time.sleep(0.15)
    motor.drive(50)
    #time.sleep(0.15)
    #motor.drive(75)
    #time.sleep(0.15)
    # motor.drive(100)

    while (runde < 3) or (final > time.time()) or (ultra3.getDistance() <= endDistance):

        if uhrzeigersinn:
            dist = ultra1.getDistance()
            grad = kompass.getDriveRotation()
        else:
            dist = ultra2.getDistance()
            grad = kompass.getAntiDriveRotation()
            
        
        if (grad > rundenCache) and (grad - 4 < rundenCache):
            rundenCache = grad

        if rundenSperre and grad > 4:
            rundenSperre = False

        if (rundenCache > rundenToleranz) and (not rundenSperre):
            runde += 1
            rundenCache = 0
            rundenSperre = True

        if runde == 3 and final == 0:
            final = time.time() + endDelay

        print("Distanz:", dist, "\t    ")
        print("Kompass:", grad, "\t    ")
        print("RundenCache:", rundenCache, "\t    ")
        print("Runde:", runde*"#", "\t    ")
        print("\n")
        print(end = "\033[F\033[A\033[A\033[A\033[A\033[A")
        if uhrzeigersinn:
            if dist == None:
                continue
            if 100 < dist < 300:
                servo.setAngle(110)
                time.sleep(0.25)
            elif dist < 30:
                servo.setAngle(80)
            else:
                servo.setAngle(100)
        else:
            if dist == None:
                continue
            if 100 < dist < 300:
                servo.setAngle(70)
                time.sleep(0.25)
            elif dist < 30:
                servo.setAngle(100)
            else:
                servo.setAngle(80)
    print()
    motor.drive(0)
    servo.reset()
    motor.reset()
    GPIO.cleanup()


try:
    fahren()
except:
    print()
    print("Interrupt")
    ultra1 = Ultraschall(16, 13)
    servo = Servo(12)
    motor = Motor(7, 1, 8)
    motor.drive(0)
    servo.reset()
    motor.reset()
    GPIO.cleanup()


    