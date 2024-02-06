# Python program to translate
# speech to text and text to speech


import speech_recognition as sr
import pyttsx3
import serial
from time import sleep

# Init arduino
arduinoData = serial.Serial("COM7", 115200, write_timeout=None, timeout=None)
# Initialize the recognizer
r = sr.Recognizer()


def refine_coeff(coeff: float):
    if coeff > 1:
        coeff = 1
    elif coeff < 0:
        coeff = 0
    return coeff


def send_coeff(text: str):
    coeff = (
        0 if text == "down" else 1 if text == "up" else 0.6 if text == "middle" else 0
    )
    coeff = refine_coeff(coeff)
    coeff = f"{coeff:.3f}\r"
    print(coeff)
    arduinoData.write(coeff.encode())


# Function to convert text to
# speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


# Loop infinitely for user to
# speak

while 1:
    # Exception handling to handle
    # exceptions at the runtime
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            print("Speak Anything :\n")
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # listens for the user's input
            audio2 = r.listen(source2)

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)

            for split_text in str(MyText).split(" "):
                split_text = split_text.lower()
                send_coeff(split_text)
                print(split_text)
                SpeakText(split_text)
                sleep(0.5)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")
