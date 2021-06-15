#include <IBusBM.h>
#include "BTS7960.h"
  
const uint8_t LEFT_FORWARD_PIN = 10; // 19 # (LEFT LPWM)  
const uint8_t LEFT_REVERSE_PIN = 11; // 21 # (LEFT RPWM)
const uint8_t RIGHT_FORWARD_PIN = 6; // 20 # (RIGHT LPWM)
const uint8_t RIGHT_REVERSE_PIN = 7; // 18 # (RIGHT RPWM)
const uint8_t EN = 46; // Never connect anything to it.
const uint8_t BRAKE_PIN = 36;
const uint8_t LIGHT_PIN = 37;

BTS7960 LeftMotor(EN, LEFT_FORWARD_PIN, LEFT_REVERSE_PIN);
BTS7960 RightMotor(EN, RIGHT_FORWARD_PIN, RIGHT_REVERSE_PIN);

IBusBM IBusServo;

int leftThrottle,rightThrottle;
int forwardThrottle,backwardThrottle;
int speed;
int forwardLeft,forwardRight,backwardLeft,backwardRight,spinLeft,spinRight;
int brake,light;

void setup() {
  digitalWrite(BRAKE_PIN, HIGH); // do this first
  pinMode(BRAKE_PIN, OUTPUT);
  digitalWrite(LIGHT_PIN, HIGH); // do this first
  pinMode(LIGHT_PIN, OUTPUT);

  // initialize serial port for debug
  Serial.begin(115200);

  // iBUS setup
  IBusServo.begin(Serial1);
  Serial.println("Starting Wariatuncio... Dawid Szymanski 2021");
}

void loop() {
  brake=constrain(map(IBusServo.readChannel(6),1000,2000,0,1),0,1);
  light=constrain(map(IBusServo.readChannel(7),1000,2000,0,1),0,1);
  speed=constrain(map(IBusServo.readChannel(2),1000,2000,0,100),0,100)*brake;
  
  forwardThrottle=constrain(map(IBusServo.readChannel(1),1500,2000,0,100),0,100);
  backwardThrottle=constrain(map(IBusServo.readChannel(1),1500,1000,0,100),0,100);
    
  leftThrottle=constrain(map(IBusServo.readChannel(0),1000,1500,0,100),0,100);
  rightThrottle=constrain(map(IBusServo.readChannel(0),1500,2000,100,0),0,100);

  forwardLeft=speed*forwardThrottle/100*leftThrottle/100;
  forwardRight=speed*forwardThrottle/100*rightThrottle/100;
  backwardLeft=speed*backwardThrottle/100*leftThrottle/100;
  backwardRight=speed*backwardThrottle/100*rightThrottle/100;

  if(brake == 1) { digitalWrite(BRAKE_PIN, LOW); delay(10); } else { digitalWrite(BRAKE_PIN, HIGH); delay(10); }
  if(light == 1) { digitalWrite(LIGHT_PIN, LOW); } else { digitalWrite(LIGHT_PIN, HIGH); }

  if(forwardLeft == 0 && backwardLeft == 0 && forwardRight == 0 && backwardRight == 0) {
    
    if (leftThrottle < 100 && rightThrottle == 100) {
      LeftMotor.TurnRight(map((100-leftThrottle)*speed/100,0,100,0,255));
      RightMotor.TurnLeft(map((100-leftThrottle)*speed/100,0,100,0,255));
    } else if (rightThrottle < 100 && leftThrottle == 100) {
      LeftMotor.TurnLeft(map((100-rightThrottle)*speed/100,0,100,0,255));
      RightMotor.TurnRight(map((100-rightThrottle)*speed/100,0,100,0,255));        
    } else {
      LeftMotor.Stop();
      RightMotor.Stop();
    }
    
  } else {
    
    if(forwardLeft == 0 && backwardLeft == 0) {
      LeftMotor.Stop();
    } else if (forwardLeft > 0 && backwardLeft == 0) {
      LeftMotor.TurnLeft(map(forwardLeft,0,100,0,255));
    } else if (forwardLeft == 0 && backwardLeft > 0) {
      LeftMotor.TurnRight(map(backwardLeft,0,100,0,255));
    };

    if(forwardRight == 0 && backwardRight == 0) {
      RightMotor.Stop();
    } else if (forwardRight > 0 && backwardRight == 0) {
      RightMotor.TurnLeft(map(forwardRight,0,100,0,255));
    } else if (forwardRight == 0 && backwardRight > 0) {
      RightMotor.TurnRight(map(backwardRight,0,100,0,255));
    };
  };

  Serial.print(forwardLeft);
  Serial.print(" ");
  Serial.print(forwardRight);
  Serial.print(" ");
  Serial.print(backwardLeft);
  Serial.print(" ");
  Serial.print(backwardRight);
  Serial.print(" ");
  Serial.print(brake);
  Serial.print(" ");
  Serial.print(light);
  Serial.println();
}
