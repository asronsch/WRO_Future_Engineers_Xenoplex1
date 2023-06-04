
ultraschaltrigger1 = 22  # rechts
ultraschalecho1 = 24
ultraschaltrigger2 = 30  # links
ultraschalecho2 = 32
ultraschaltrigger3 = 26  # vorne
ultraschalecho3 = 28

servo_middle = 90

scompass = 0
runde = 0
rundensperre = False
compassWerte = 0

stoppdelay = 500
startsec = 0
anhalten = False
sperre = True

GPIO.setmode(GPIO.BOARD)
GPIO.setup(ultraschaltrigger1, GPIO.OUT)
GPIO.setup(ultraschalecho1, GPIO.IN)
GPIO.setup(ultraschaltrigger2, GPIO.OUT)
GPIO.setup(ultraschalecho2, GPIO.IN)
GPIO.output(ultraschaltrigger1, GPIO.LOW)
GPIO.output(ultraschaltrigger2, GPIO.LOW)
GPIO.setup(4, GPIO.IN)
GPIO.setup(5, GPIO.IN)
print("Waiting...")
check = False
while not check:
    if GPIO.input(4) == GPIO.HIGH:
        gegenUhrzeigersin = True
        check = True
    elif GPIO.input(5) == GPIO.HIGH:
        gegenUhrzeigersin = False
        check = True
print("Beginning!")


def ultraschall(trigger, echo):
    GPIO.output(trigger, GPIO.LOW)
    time.sleep(0.005)
    GPIO.output(trigger, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(trigger, GPIO.LOW)

    abstand = GPIO.pulseIn(echo, GPIO.HIGH)
    abstand_cm = 0.017 * abstand
    return abstand_cm


def setup():
    # Motor starten
    GPIO.output(3, GPIO.LOW)
    GPIO.output(2, GPIO.LOW)
    # myservo.attach(23)  # Attach the servo to a pin


def loop():
    GPIO.output(2, GPIO.HIGH)
    GPIO.output(3, GPIO.LOW)

    # Ultraschall abfragen
    ultraschall(ultraschaltrigger1, ultraschalecho1)
    ultraschall(ultraschaltrigger2, ultraschalecho2)


    if gegenUhrzeigersin:
        print("Gegen Uhrzeiger")
        while True:
            compass()
            compassWerte = (compass() - 36) * (-1)
            print(compass())
            rundenzaehler()
            ultraschall(ultraschaltrigger2, ultraschalecho2)
            stopp()

            if ultraschall(ultraschaltrigger2, ultraschalecho2) > 500:
                time.sleep(0.01)
            elif ultraschall(ultraschaltrigger2, ultraschalecho2) > 80:
                myservo.write(servo_middle + 35)
                time.sleep(0.01)
            else:
                if ultraschall(ultraschaltrigger2, ultraschalecho2) > 25:
                    myservo.write(servo_middle + 10)
                    time.sleep(0.01)
                else:
                    if ultraschall(ultraschaltrigger2, ultraschalecho2) == 26:
                        myservo.write(servo_middle)
                        time.sleep(0.01)
                    else:
                        if ultraschall(ultraschaltrigger2, ultraschalecho2) < 26:
                            myservo.write(servo_middle - 20)
                            time.sleep(0.01)
            while anhalten:
                print("HAALLLLTTT")
                GPIO.output(2, GPIO.LOW)
                GPIO.output(3, GPIO.LOW)
                myservo.write(servo_middle)
    else:
        print("Im Uhrzeigersinn")
        while True:
            ultraschall(ultraschaltrigger1, ultraschalecho1)
            compass()
            compassWerte = compass()
            rundenzaehler()
            stopp()

            if ultraschall(ultraschaltrigger1, ultraschalecho1) > 500:
                time.sleep(0.01)
            else:
                if ultraschall(ultraschaltrigger1, ultraschalecho1) > 80:
                    time.sleep(0.01)
                    myservo.write(servo_middle - 35)
                else:
                    if ultraschall(ultraschaltrigger1, ultraschalecho1) > 25:
                        myservo.write(servo_middle - 10)
                        time.sleep(0.01)
                    else:
                        if ultraschall(ultraschaltrigger1, ultraschalecho1) == 25:
                            myservo.write(servo_middle)
                            time.sleep(0.01)
                        else:
                            if ultraschall(ultraschaltrigger1, ultraschalecho1) < 25:
                                myservo.write(servo_middle + 10)
                                time.sleep(0.01)
                            else:
                                return
            while anhalten:
                print("HAALLLLTTT")
                GPIO.output(2, GPIO.LOW)
                GPIO.output(3, GPIO.LOW)
                myservo.write(servo_middle)


def compass():
    # Wire.beginTransmission(0x3B)
    # Wire.write(byte(0x21))
    # Wire.endTransmission()
    # byte high, low

    # Wire.requestFrom(0x3B, 2)
    # if (2 <= Wire.available()):
    #     high = Wire.read()
    #     low = Wire.read()

    # val = 0
    # val = (high << 8) + low
    # val = val / 10

    # Serial.print("Comp: ");
    # Serial.println(val);
    # return val
    return 0  # Replace with actual compass reading


def rundenzaehler():
    print(scompass)
    # Serial.println(rundensperre)
    if compassWerte >= scompass:
        if (scompass <= 5) and (compassWerte < 27):
            scompass = compassWerte
        elif scompass > 5:
            scompass = compassWerte
            rundensperre = False
        else:
            pass
    elif compassWerte < scompass:
        if (scompass >= 34) and (rundensperre == False):
            runde += 1
            scompass = 0
            rundensperre = True
            print("Runde:", runde)
            return runde
        else:
            pass
    else:
        pass


def stopp():
    global anhalten, sperre, startsec
    if runde >= 3:
        while sperre:
            startsec = time.time() * 1000
            sperre = False
        if (time.time() * 1000) >= (startsec + stoppdelay):
            anhalten = True
        else:
            pass
    else:
        anhalten = False


if __name__ == '__main__':
    setup()
    while True:
        loop()
