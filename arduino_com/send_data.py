# Python program to translate
# speech to text and text to speech


import speech_recognition as sr
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


def send_coeffs(coeffs: tuple[float, float, float, float, float, float]):
    coeffs = [str(refine_coeff(coeff)) for coeff in coeffs]
    coeffs = "|".join(coeffs)
    coeffs = f"{coeffs}\r"
    print(coeffs)
    arduinoData.write(coeffs.encode())
