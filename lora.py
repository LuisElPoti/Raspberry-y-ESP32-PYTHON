import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_rfm9x
import socketio

sio = socketio.Client()

# Configure RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Attempt to set up the RFM9x module
try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 868.2)
    print('RFM9x detected')
except RuntimeError:
    print('RFM9x error')

# ... (Configuración del RFM9x y otros códigos previos)

@sio.event
def connect():
    print('Conectado al servidor WebSocket')

@sio.event
def disconnect():
    print('Desconectado del servidor WebSocket') 

sio.connect('http://10.0.0.163:5000')  # Reemplaza 'tu_raspberry_pi_ip' con la dirección IP de tu Raspberry Pi

# Bucle para recibir datos LoRa y enviar al servidor WebSocket
while True:
    packet = None
    packet = rfm9x.receive()
    if packet is not None:
        # Split packet y obtener datos (temp y humd)
        temp = int.from_bytes(packet[2:4], byteorder='little') / 10.0
        humd = int.from_bytes(packet[4:6], byteorder='little') / 10.0
        
        # Imprimir los valores recibidos en la consola
        print("Received temperature:", temp, "C")
        print("Received humidity:", humd, "%")

        # Enviar datos al servidor WebSocket
        sio.emit('send_data', {'temp': temp, 'humd': humd})

    # Resto del código para procesamiento si es necesario

    time.sleep(1)  # Pausa para evitar un ciclo de CPU continuo
