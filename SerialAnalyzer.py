import serial
import time

ser = serial.Serial('COM1', baudrate=9600)
print("Analyzer mock started...")

while True:
    ser.write(b"ENQ\r\n")
    print("Sent: ENQ")
    time.sleep(5)
