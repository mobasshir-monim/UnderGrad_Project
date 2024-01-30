#include <Servo.h>
#include "StringSplitter.h"

Servo pinky;
Servo ring;
Servo middle;
Servo index;

float coeff;
int pos = 0;
int cr = 1;

void setup()
{
    Serial.begin(115200);
    // Attach servos
    pinky.attach(6);
    ring.attach(9);
    middle.attach(10);
    index.attach(11);
}

void moveFinger(Servo finger, int idx, float coefficient)
{
    int pos = finger.read();
    int cr = (pos - coeff * 180) > 0 ? -1 : 1;
    finger.write(pos + cr);
}

void loop()
{
    while (Serial.available() == 0)
    {
        pinMode(13, OUTPUT);
    }

    String myCmd = Serial.readStringUntil('\r');
    StringSplitter *splitter = new StringSplitter(myCmd, '|', 6);

    for (int i = 0; i <= 180; i++)
    {
        moveFinger(index, i, splitter->getItemAtIndex(0).toFloat());
        moveFinger(middle, i, splitter->getItemAtIndex(1).toFloat());
        moveFinger(ring, i, splitter->getItemAtIndex(2).toFloat());
        moveFinger(pinky, i, splitter->getItemAtIndex(3).toFloat());
        delay(5);
    }

    // Serial.flush();
    Serial.println("DONE\n");
}
