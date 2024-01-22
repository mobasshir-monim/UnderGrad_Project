import serial
from time import sleep
arduinoData=serial.Serial('COM5',115200, write_timeout=100)

while True:
    cmd=input('Command: ')
    # cmd=cmd
    print(cmd)
    arduinoData.write(cmd.encode())
    shit=arduinoData.read().decode()
    sleep(1)
    
    
    
    
    
    
    
    
    
    