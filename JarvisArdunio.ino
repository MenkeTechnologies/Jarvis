#include <Wire.h>
#include <Servo.h>
const byte escPin = 9;
const byte steerPin = 8;
const byte i2cAddr = 0xA;
long lastCall = 0;
long currentTime = 0;
int dcMonitor = 1500;
byte turn = 90 ;
byte throttle = 90;
Servo steerServo, ESC;

bool reversed = false;


void setup() 
{
  Serial.begin(9600);
  ESC.attach(escPin);
  steerServo.attach(steerPin);
  Wire.begin(i2cAddr); 
  Wire.onReceive(receiveEvent);
}

void loop() 
{

currentTime = millis();
if (currentTime > lastCall + dcMonitor)
{
  //setTurn(90);
  //setThrottle(90);
  //delay(100);
}

}

void receiveEvent()
{
  byte recv = Wire.read();
  switch(recv)
  {
    case 01:
    
    turn = Wire.read();  
    throttle = Wire.read();
    setTurn(turn);
    setThrottle(throttle);
    break;
    case 02:
    lastCall = millis();
    Serial.println("Server talk");
    break;
    
    
  }
}

void setThrottle(byte setPnt)
{
  if (setPnt <80 && !reversed)
  {
    ESC.write(70);
    delay(100);
    ESC.write(85);
    delay(100);
    reversed = true;
  }
  if (setPnt > 90)
    reversed = false;
  ESC.write(setPnt);
  Serial.print("Throttle: ");
  Serial.print(setPnt);
  Serial.println();
}

void setTurn(byte setPnt)
{
  steerServo.write(-setPnt+180);
  Serial.print("Steering: ");
  Serial.print(-setPnt+180);
  Serial.println();
}

