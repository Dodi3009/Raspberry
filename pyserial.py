import serial
import time

ser=serial.Serial('/dev/ttyS0',9600, timeout=1)
ser.flush

while True:
	data=ser.readline().decode('utf-8').rstrip()
	print(f"Ricevuto: {data}")
	ser.write(b"Ciao Arduino!\n")
	time.sleep(1)
