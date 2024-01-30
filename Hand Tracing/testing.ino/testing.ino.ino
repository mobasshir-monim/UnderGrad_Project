#include <Servo.h>

Servo myservo;
float coeff;
int pos = 0;
int cr = 1;

void setup() {
  Serial.begin(115200);
  myservo.attach(9);
}
void loop() {
  while (Serial.available() == 0) {
    pinMode(13, OUTPUT);
  }

  pos = myservo.read();
  String myCmd = Serial.readStringUntil('\r');
  coeff = myCmd.toFloat();
  cr = (pos - coeff * 180) > 0 ? -1 : 1;
  Serial.println(cr);

  for (pos = myservo.read(); (cr == 1 && pos < coeff * 180) || (cr == -1 && pos > coeff * 180); pos += cr) {  // goes from 180 degrees to 0 degrees
    myservo.write(pos);                                                                                       // tell servo to go to position in variable 'pos'
    delay(5);
  }

  // Serial.flush();
  Serial.println("DONE\n");
}
