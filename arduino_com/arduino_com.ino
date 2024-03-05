#include <Servo.h>
#include "StringSplitter.h"

Servo pinky;
Servo ring;
Servo middle;
Servo index;
Servo thumb;
Servo wrist;

void setup()
{
    Serial.begin(115200);
    // Attach servos
    index.attach(5);
    middle.attach(6);
    ring.attach(10);
    pinky.attach(11);
    thumb.attach(9);
    wrist.attach(3);

    // init
    // index.write(0);
    // middle.write(0);
    // // ring.write(0);
    // pinky.write(0);
    // thumb.write(0);
    // wrist.write(0);
}

float rad_to_deg(float rad)
{
    return (180 * rad) / PI;
}

void loop()
{
    while (Serial.available() == 0)
    {
        pinMode(13, OUTPUT);
    }

    String myCmd = Serial.readStringUntil('\r');
    StringSplitter splitter(myCmd, '|', 6);

    index.write(2 * rad_to_deg(asin(splitter.getItemAtIndex(0).toFloat())));
    middle.write(2 * rad_to_deg(asin(splitter.getItemAtIndex(1).toFloat())));
    ring.write(2 * rad_to_deg(asin(splitter.getItemAtIndex(2).toFloat())));
    pinky.write(2 * rad_to_deg(asin(splitter.getItemAtIndex(3).toFloat())));
    thumb.write(2 * rad_to_deg(asin(splitter.getItemAtIndex(4).toFloat())));
    wrist.write(2 * rad_to_deg(asin(splitter.getItemAtIndex(5).toFloat())));
}
