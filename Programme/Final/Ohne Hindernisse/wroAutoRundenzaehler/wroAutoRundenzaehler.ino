
#include <Servo.h>
#include <Wire.h>
Servo myservo;

//Fahrt
bool Uhrzeigersin = false;
bool gegenUhrzeigersin = true;


//Ultraschallvariablen
int Ultraschaltrigger1 = 22; //rechts
int Ultraschalecho1 = 24;
int Ultraschaltrigger2 = 30; //links
int Ultraschalecho2 = 32;
int Ultraschaltrigger3 = 26; //vorne
int Ultraschalecho3 = 28;

int servo_middle = 90;

int Scompass = 0;
int runde = 0;
bool rundensperre = false;
int compassWerte = 0;

int Stoppdelay = 500;      // Zeit in ms nach der 3 Runde bis das Auto anhält
int Startsec = 0;
bool Anhalten = false;
bool sperre = true;
int Ultraschall(){
  digitalWrite(Ultraschaltrigger1, LOW);
  delay(5);
  digitalWrite(Ultraschaltrigger1, HIGH);
  delay(10);
  digitalWrite(Ultraschaltrigger1, LOW);

  float abstand1 = pulseIn(Ultraschalecho1, HIGH);
  int abstand_cm1 = 0.017 * abstand1;
  //Serial.println(abstand_cm1);
  return abstand_cm1;
}


int Ultraschall2(){
  digitalWrite(Ultraschaltrigger2, LOW);
  delay(5);
  digitalWrite(Ultraschaltrigger2, HIGH);
  delay(10);
  digitalWrite(Ultraschaltrigger2, LOW);

  float abstand2 = pulseIn(Ultraschalecho2, HIGH);
  int abstand_cm2 = 0.017 * abstand2;
  //Serial.println(abstand_cm2);
  return abstand_cm2;
}



void setup() {
// put your setup code here, to run once:
pinMode(Ultraschaltrigger1, OUTPUT);
pinMode(Ultraschalecho1, INPUT);
pinMode(Ultraschaltrigger2, OUTPUT);
pinMode(Ultraschalecho2, INPUT);
digitalWrite(Ultraschaltrigger1, LOW);
digitalWrite(Ultraschaltrigger2, LOW);
pinMode(4, INPUT);
pinMode(5, INPUT);
Serial.begin(9600);
myservo.attach(23);
//Motor Starten
digitalWrite(3, LOW);
digitalWrite(2, LOW);
myservo.write(servo_middle);
Serial.begin(115200);

Wire.begin();
Serial.println("Waiting...");
bool check = false;
  while(!check){
    if(digitalRead(4) == HIGH){
      gegenUhrzeigersin = true;
      check = true;
    } else 
    if(digitalRead(5) == HIGH){
      gegenUhrzeigersin = false;
      check = true;
    }
}
Serial.println("Beginning!");

}

void loop() {

digitalWrite(2, HIGH);
digitalWrite(3, LOW);

//Ultraschall Abfragen
Ultraschall();
Ultraschall2();
//Serial.println(Rundenzaehler);

//Fahrt

  if(gegenUhrzeigersin) {
    Serial.print("Gegen Uhrzeiger");
    while(true){
      compass();
      compassWerte = (compass()-36)*(-1);
      Serial.println(compass());
      rundenzaehler();
      Ultraschall2();
      Stopp();

      if(Ultraschall2() > 500){
        delay(10);
      } else 
      if(Ultraschall2() > 80){
        myservo.write(servo_middle + 35);
        delay(10);
      }else{
        if(Ultraschall2() > 25){
        myservo.write(servo_middle + 10);
        delay(10);
        }else{

          if(Ultraschall2() == 26){
          myservo.write(servo_middle);
          delay(10);
          } else{
            if(Ultraschall2() < 26){
            myservo.write(servo_middle - 20);
            delay(10);
            }
          }
        }
      }
      while(Anhalten == true){          // Stopp Schleife 
        Serial.println("HAALLLLTTT");
        digitalWrite(2, LOW);
        digitalWrite(3, LOW);
        myservo.write(servo_middle);
      }
     }
  } else {
    Serial.println("Im Uhrzeigersinn");
    while(true){
      //Serial.print("Runde:");
      //Serial.println(Ultraschal());
      Ultraschall();
      compass();
      compassWerte = compass();
      rundenzaehler();
      Stopp();

      if(Ultraschall() > 500){
        delay(10);
      }else{
        if(Ultraschall() > 80){
          delay(10);
          myservo.write(servo_middle - 35);
        } else{
          if(Ultraschall() > 25){
          myservo.write(servo_middle -10);
          delay(10);
          }else{
            if(Ultraschall() == 25){
            myservo.write(servo_middle);
            delay(10);
            } else{
              if(Ultraschall() < 25){
              myservo.write(servo_middle + 10);
              delay(10);
             }else {
             return;
             }
            }
          }
        }  
      } 
      while(Anhalten == true){          // Stopp Schleife 
        Serial.println("HAALLLLTTT");
        digitalWrite(2, LOW);
        digitalWrite(3, LOW);
        myservo.write(servo_middle);
      } 
     }
  }
}


int compass(){
  Wire.beginTransmission(0x3B);
  Wire.write(byte(0x21));
  Wire.endTransmission();
  byte high, low;
  
  Wire.requestFrom(0x3B, 2);
  if (2 <= Wire.available()) {
    
    high = Wire.read();
    low = Wire.read();
  }

  int val = 0;
  val = (high << 8) + low;
  val = val/10; 

  //Serial.print("Comp: ");
  //Serial.println(val);
  return val;
}
int rundenzaehler(){
  Serial.println(Scompass);
  //Serial.println(rundensperre);
  if(compassWerte >= Scompass){
    if ((Scompass <= 5) && (compassWerte < 27)){
      Scompass = compassWerte;
    }else if (Scompass > 5){
      Scompass = compassWerte;
      rundensperre = false;
    }else {}
  }else if (compassWerte < Scompass){
    if ((Scompass >= 34) && (rundensperre==false)){
      runde++;
      Scompass = 0;
      rundensperre = true;
      Serial.print("Runde:");
      Serial.println(runde);
      return runde;
    }else {}
  }else {}

}
bool Stopp() {
  if (runde >= 3){
    while(sperre==true){
    Startsec = millis();
    sperre=false;
    }
    if (millis() >= Startsec + Stoppdelay){
      Anhalten = true;
      return Anhalten;
    }else{}
  }else{
    Anhalten = false;
  }
  
}