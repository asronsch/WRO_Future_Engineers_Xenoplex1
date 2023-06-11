#include <Pixy2.h>
#include <Pixy2I2C.h>


// https://docs.pixycam.com/wiki/doku.php?id=wiki:v2:hooking_up_pixy_to_a_microcontroller_-28like_an_arduino-29
#include <Servo.h>
#include <Wire.h>
// This is the main Pixy object 
Pixy2 pixy;
Servo myservo;
int Xgrun;
int Xrot;
int Xg;
int X2;
int X3;
int Xr;
int Xr2;

  int i =0;
  int signature = 0;
  int x = 0;
  int y = 0;
  int width = 0;
  int height = 0;
  //int index = 0;
  int age = 0;

int Ultraschaltrigger1 = 22; //rechts
int Ultraschalecho1 = 24;
int Ultraschaltrigger2 = 30; //links
int Ultraschalecho2 = 32;
int Ultraschaltrigger3 = 26; //vorne
int Ultraschalecho3 = 28; 

int Objektrot;
bool Kurve = false;

int servo_middle = 90;

int Scompass = 0;
int runde = 0;
bool rundensperre = false;
int compassWerte = 0;

int Stoppdelay = 2000;      // Zeit in ms nach der 3 Runde bis das Auto anhält
int Startsec = 0;
bool Anhalten = false;
bool sperre = true;

int ComEndWert = 0;


void setup()
{
  pinMode(Ultraschaltrigger1, OUTPUT);
  pinMode(Ultraschalecho1, INPUT);
  pinMode(Ultraschaltrigger2, OUTPUT);
  pinMode(Ultraschalecho2, INPUT);
  pinMode(Ultraschaltrigger3, OUTPUT);
  pinMode(Ultraschalecho3, INPUT);
  Serial.begin(115200);
  Serial.print("Starting...\n");
  myservo.attach(23);
  myservo.write(90);
  delay(1000);
  pixy.init();
}

void loop(){



  // grab blocks!
  pixy.ccc.getBlocks();

  
  signature = pixy.ccc.blocks[i].m_signature;
  x = pixy.ccc.blocks[i].m_x;
  y = pixy.ccc.blocks[i].m_y;
  width = pixy.ccc.blocks[i].m_width;
  height = pixy.ccc.blocks[i].m_height;
  //index = pixy.ccc.blocks[i].m_index;
  age = pixy.ccc.blocks[i].m_age;
  //i = signature;

  /*Ultraschal();
  digitalWrite(2, HIGH);
  digitalWrite(3, LOW);
  Serial.println(Ultraschal());
  Ultraschal();
  
  if(Ultraschal() < 50){
   myservo.write(110);
  }
  if(Ultraschal() == 50){
     myservo.write(90);
  }
  if(Ultraschal() > 50){
      myservo.write(70);
      }*/
  digitalWrite(2, HIGH);
  digitalWrite(3, LOW);
  
  if(pixy.ccc.getBlocks() ){
   /*if(pixy.ccc.getBlocks() ){

   }else{
    if(Objektrot == true){
      if(Ultraschal2() < 50){
        myservo.write(65);
      }
      if(Ultraschal2() >= 20){
        myservo.write(115);
        Objektrot = true;
        }
      }
    } */
    SignatureGreen();   //Wenn grüne Signatur erkannt dann wird links daran durchgefahren.  Siehe Unterprogramm. 
    SignatureRed();     //Wenn Rote Signatur erkannt dann wird rechts daran durchgefahren.  Siehe Unterprogramm. 
  
  }else{
    Ultraschal();
    if(Ultraschal() >= 180){
      CompassKurve();
      Serial.println(Kurve);
    }else{
      if(Ultraschal() < 65){
        myservo.write(110);
      }else{
        if(Ultraschal() == 65){
          myservo.write(90);
        }else{
          if(Ultraschal() > 65){
            myservo.write(70);
          }
        }  
    	}
    }
    if(Kurve == true){
      Serial.println("Kurve außen Ultraschall");
      Ultraschal2();
      if (Ultraschal2() + Ultraschal() >= 100){
        Kurve == false;
      }else{
        if (Ultraschal2() < 65){
          myservo.write(70);
        }else{
          if (Ultraschal2() == 65){
            myservo.write(90);
          }else{
            if (Ultraschal2() > 65){
              myservo.write(110);
            }else{}
          }
        }
      }
      if(pixy.ccc.getBlocks() ){
        SignatureGreen();   //Wenn grüne Signatur erkannt dann wird links daran durchgefahren.  Siehe Unterprogramm. 
        SignatureRed();     //Wenn Rote Signatur erkannt dann wird rechts daran durchgefahren.  Siehe Unterprogramm.   
      }
    }
  }
}



















int SignatureGreen(){
  pixy.ccc.getBlocks();
  Serial.print(y);
  if(signature == 2){ // Signatur 2 in der Pixi ist der Grüne Block
    if(y >= 40){
      Serial.print(" Grün ");
      Xgrun = x * 0.095;// Bei Grünem Block muss links vorbeigefahren werden
      X3 = Xgrun + 55;
      Serial.println(X3);
      myservo.write(X3);
      digitalWrite(2, HIGH);
      pixy.ccc.getBlocks();
    }  
  }
}

int SignatureRed(){
  pixy.ccc.getBlocks();
  if(signature == 3){ // Signatur 3 in der Pixi ist der Roter Block
    if(y >= 40){
      Objektrot = true;
      Serial.print(" Rot ");
      Xrot = x * 0.095;
      Xr2 = Xrot + 95;
      myservo.write(Xr2);
      digitalWrite(2, HIGH);
      pixy.ccc.getBlocks();
    }
  }
}

int Ultraschal(){
  digitalWrite(Ultraschaltrigger1, LOW);
  delay(5);
  digitalWrite(Ultraschaltrigger1, HIGH);
  delay(10);
  digitalWrite(Ultraschaltrigger1, LOW);

  float abstand1 = pulseIn(Ultraschalecho1, HIGH);
  int abstand_cm1 = 0.017 * abstand1;
  return abstand_cm1;
}

int Ultraschal2(){
  
  digitalWrite(Ultraschaltrigger2, LOW);
  delay(5);
  digitalWrite(Ultraschaltrigger2, HIGH);
  delay(10);
  digitalWrite(Ultraschaltrigger2, LOW);

  float abstand2 = pulseIn(Ultraschalecho2, HIGH);
  int abstand_cm2 = 0.017 * abstand2;
  return abstand_cm2;
}


int Ultraschallvorne(){
  
  digitalWrite(Ultraschaltrigger3, LOW);
  delay(5);
  digitalWrite(Ultraschaltrigger3, HIGH);
  delay(10);
  digitalWrite(Ultraschaltrigger3, LOW);

  float abstandvorne = pulseIn(Ultraschalecho3, HIGH);
  int abstand_cmvorne = 0.017 * abstandvorne;
  return abstand_cmvorne;
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

void CompassKurve(){
  
  compass();
  if (compass()< 3 || compass() > 34){
    ComEndWert = 9;
  }
  if (compass()< 12){
    ComEndWert = 18;
  }
  if (compass()< 21){
    ComEndWert = 27;
  }
  if (compass()< 30){
    ComEndWert = 0;
  }
  while(compass() < ComEndWert){
    myservo.write(servo_middle - 40);
    Kurve = true;
  }
}