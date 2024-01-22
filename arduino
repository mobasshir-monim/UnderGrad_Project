#include <Servo.h>
Servo myservo;
String myCmd;
int pos = 0; 
void setup() { 
	Serial.begin(115200);
  myservo.attach(9);
} 
void loop() { 
	while(Serial.available()==0){
  pinMode(13,OUTPUT);
  }
  myCmd=Serial.readStringUntil('\r');
  if(myCmd=="ON"){
    for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15); 
    }
  }
   if(myCmd=="OFF"){
    for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);  
    }
  }
} 
