#include <Servo.h>
#include "StringSplitter.h"

Servo pinky;
Servo ring;
Servo middle;
Servo index;
Servo thumb;
Servo wrist;

float coeff;
int pos = 0;
int cr = 1;

void setup()
{
    Serial.begin(115200);
    // Attach servos
    pinky.attach(11);
    ring.attach(5);
    middle.attach(6);
    index.attach(9);
    wrist.attach(3);
    thumb.attach(10);
}

void moveFinger(Servo finger, int idx, float coefficient)
{
    int current = finger.read();
    int final = 180 * coeff;
    float diff = abs(current - final) / 180;
    int cr = (pos - final) > 0 ? -1 : 1;
    finger.write(pos + diff);
    // Serial.println("pos: ");
    // Serial.println(pos + diff);
}

void loop()
{
    while (Serial.available() == 0)
    {
        pinMode(13, OUTPUT);
    }

    String myCmd = Serial.readStringUntil('\r');
    StringSplitter *splitter = new StringSplitter(myCmd, '|', 6);

    index.write(180 * splitter->getItemAtIndex(0).toFloat());
    middle.write(180 * splitter->getItemAtIndex(1).toFloat());
    ring.write(180 * splitter->getItemAtIndex(2).toFloat());

    Serial.println("DONE\n");
}
