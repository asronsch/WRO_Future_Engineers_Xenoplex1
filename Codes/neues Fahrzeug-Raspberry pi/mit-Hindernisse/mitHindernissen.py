import RPi.GPIO as GPIO
from sensor_node import Ultraschall, Compass, Taster
from control_node import Motor, Servo
from videoStream import VideoStream
from threading import Thread
import cv2
import time
from camera_node import node, start_node

global forceQuit
forceQuit = False
global obj
obj = {"fps": 0, "objects": []}
global starter
starter = False

try:
    GPIO.cleanup()
    
except:
    print("nothing to clean")

def biggest():
    big = {"sx": 0}
    if len(obj["objects"]) == 0:
        return big
    for o in obj["objects"]:
        if o["sx"] > big["sx"]:
            big = o
    return big
        

def fahren():
    global obj
    global starter
    # global servo

    ultraR = Ultraschall(16, 13)  # rechts
    ultraL = Ultraschall(21, 26)  # links
    ultraV = Ultraschall(20, 19)  # vorne
    servo = Servo(12)
    servo.setAngle(90)
    motor = Motor(7, 1, 8)
    motor.drive(0)
    taster1 = Taster(24)  # rechts
    taster2 = Taster(23)  # links
    kompass = Compass(1, 0x60)
    kompass.setStartPosition()

    runde = 0
    rundenCache = 0
    rundenSperre = False
    rundenToleranz = 33  # toleranz, ab wann runde + 1
    final = 0

    wasObj = False

    ultraFLag = 0

    uhrzeigersinn = None
    print("Warte auf Kamera...")
    while not starter:
        continue
    print("Kamera initialisiert")
    print(2*"\n")

    print(5*"\n")

    print("Warter auf Start...")
    print()
    while uhrzeigersinn == None:
        print("-> Distanz:", ultraR.getDistance(), "\tKompass:", kompass.getDriveRotation(), "\t      ")
        print()
        print("<- Distanz:", ultraL.getDistance(), "\tKompass:", kompass.getAntiDriveRotation(), "\t      ")
        print("\n")
        print(end = "\033[F\033[A\033[A\033[A\033[A")

        if taster1.isPressed():
            uhrzeigersinn = True
        if taster2.isPressed():
            uhrzeigersinn = False
        time.sleep(0.05)
    kompass.setStartPosition()
    
    print("Starte!")
    print(3*"\n")

    motor.drive(25)
    #time.sleep(0.15)
    #motor.drive(50)
    #time.sleep(0.15)
    #motor.drive(75)
    #time.sleep(0.15)
    #motor.drive(100)

    while True:

        if uhrzeigersinn:
            dist = ultraR.getDistance()
            grad = kompass.getDriveRotation()
        else:
            dist = ultraL.getDistance()
            grad = kompass.getAntiDriveRotation()
        
        time.sleep(0.05)
        
        if (grad > rundenCache) and (grad - 4 < rundenCache):
            rundenCache = grad

        if rundenSperre and grad > 4:
            rundenSperre = False

        if (rundenCache > rundenToleranz) and (not rundenSperre):
            runde += 1
            rundenCache = 0
            rundenSperre = True

        if runde == 3:
            if ultraV.getDistance() <= 150:
                break
        #print("Distanz:", dist, "\t    ")
        #print("Kompass:", grad, "\t    ")
        #print("RundenCache:", rundenCache, "\t    ")
        #print("Runde:", runde*"#", "\t    ")
        #print("\n")
        #print(end = "\033[F\033[A\033[A\033[A\033[A\033[A")
        big = biggest()
        """if uhrzeigersinn:
            print(obj)
            if dist == None:
                continue
                 
            if big["sx"] > 90:
                wasObj = True
                if big["id"] == "red":
                    print(big["sx"])
                    servo.setAngle(110)
            elif wasObj:
                ausr = kompass.getDriveRotation()%9
                if ausr == 0:
                    servo.setAngle(90)
                    wasObj = False
                elif 5 < ausr < 9:
                    servo.setAngle(100)
                else:
                    servo.setAngle(80)
            if len(obj["objects"]) == 0:
                print("gfsadfgsdfh")
                if 95 < ultraR.getDistance() < 300:
                    print(ultraR.getDistance())
                    servo.setAngle(120)
                    time.sleep(0.1)
            if dist < 50:
                servo.setAngle(80)
            elif 50 <= dist < 100:
                servo.setAngle(100)
        else:
            if dist == None:
                continue
            if 100 < dist < 300:
                servo.setAngle(80)
                time.sleep(0.25)
            elif dist < 50:
                servo.setAngle(100)
            else:
                servo.setAngle(80)"""
        print(obj["objects"])
        
        if uhrzeigersinn:
            
            dist = ultraR.getDistance()
            rot = kompass.getDriveRotation()

            if big["sx"] > 100:
                print("     case0")
                wasObj = True
                if big["id"] == "red":
                    servo.setAngle(115)
                elif big["id"] == "green":
                    servo.setAngle(65)
                else:
                    print("     case00000000000000000000")

            elif 90 < dist < 450:        #kurve
                wasObj = False
                servo.setAngle(120)
                print("     case1")
            elif big["sx"] > 70:
                print("     case22")
                wasObj = True
                if big["id"] == "red":
                    servo.setAngle(115)
                elif big["id"] == "green":
                    servo.setAngle(65)
                else:
                    print("     case2.3.4.5")
            elif wasObj:
                ausr = rot % 9
                if ausr == 0:
                    servo.setAngle(90)
                    wasObj = False
                    print("     case ausrichtung comp")
                elif 5 < ausr < 9:
                    servo.setAngle(100)
                else:
                    servo.setAngle(80)
                print("     case333 ")
            elif dist < 50:
                servo.setAngle(80)
                print("     case4444")
            elif 50 <= dist < 80:
                servo.setAngle(110)
                print("     case55555")
            elif 100 < dist < 450:        #kurve 2 backup
                wasObj = False
                servo.setAngle(120)
                print("     case1")
            else:
                print(dist)
                print(rot)
                print(10*"HOLLLLYYYY")
        
        else: # gegen Uhrzeiger

            dist = ultraL.getDistance()
            rot = kompass.getAntiDriveRotation()
                
            if big["sx"] > 100:
                print("     case0")
                wasObj = True
                if big["id"] == "red":
                    servo.setAngle(115)
                elif big["id"] == "green":
                    servo.setAngle(65)
                else:
                    print("     case00000000000000000000")

            elif 90 < dist < 450:        #kurve
                wasObj = False
                servo.setAngle(80)
                print("     case1")
            elif big["sx"] > 70:
                print("     case22")
                wasObj = True
                if big["id"] == "red":
                    servo.setAngle(115)
                elif big["id"] == "green":
                    servo.setAngle(65)
                else:
                    print("     case2.3.4.5")
            elif wasObj:
                ausr = rot % 9
                if ausr == 0:
                    servo.setAngle(90)
                    wasObj = False
                    print("     case ausrichtung comp")
                elif 5 < ausr < 9:
                    servo.setAngle(100)
                else:
                    servo.setAngle(80)
                print("     case333 ")
            elif dist < 50:
                servo.setAngle(110)
                print("     case4444")
            elif 50 <= dist < 80:
                servo.setAngle(80)
                print("     case55555")
            elif 100 < dist < 450:        #kurve 2 backup
                wasObj = False
                servo.setAngle(80)
                print("     case1")
            else:
                print(dist)
                print(rot)
                print(10*"HOLLLLYYYY")
            

    print()
    motor.drive(0)
    servo.reset()
    motor.reset()
    GPIO.cleanup()

def objekte():
    global obj
    global starter
    imW = 640
    imH = 360

    winW = 400
    winH = 240

    stream = VideoStream(resolution=(imW, imH), framerate=30).start()
    while not forceQuit:
        frame = stream.read()
        obj = node(frame, imW, imH)
        if not starter:
            starter = True


try:
    print("Starting Node")
    start_node()
    print("Starting Threads")
    objektThread = Thread(target=objekte)
    objektThread.start()
    fahren()
except Exception as exc:
    print(exc)
    print("obj: ", obj)
    GPIO.cleanup()
    ultra1 = Ultraschall(16, 13)
    servo = Servo(12)
    motor = Motor(7, 1, 8)
    motor.drive(0)
    servo.reset()
    motor.reset()
    GPIO.cleanup()