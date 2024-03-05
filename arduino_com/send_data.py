# Python program to translate
# speech to text and text to speech

import serial
import time

# Init arduino
# arduinoData = serial.Serial(write_timeout=None, timeout=None)
arduinoData = serial.Serial("COM7", 115200, write_timeout=None, timeout=None)


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
    time.sleep(1.5)


# send_coeffs([0, 0, 0, 0, 0, 0])
# send_coeffs([1, 0, 0, 0, 0, 0])
# send_coeffs([0, 1, 0, 0, 0, 0])
# send_coeffs([0, 0, 1, 0, 0, 0])
# send_coeffs([0, 0, 0, 1, 0, 0])
# send_coeffs([0, 0, 0, 0, 1, 0])
