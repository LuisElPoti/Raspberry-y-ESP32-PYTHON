import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_rfm9x
import socketio
from flask import Flask, render_template
from flask_socketio import SocketIO, emit 
import threading
import pygame
from gtts import gTTS

# import firebase_admin
# from firebase_admin import credentials, db


# Inicializar Firebase Admin SDK
# cred = credentials.Certificate("credentials.json")  # Reemplaza con la ubicación de tu archivo JSON
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://sensores-apolo-default-rtdb.firebaseio.com/'
# })

app = Flask(__name__)
socketio = SocketIO(app)



# Configurar RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 868)
    print('RFM9x detected')
except RuntimeError:
    print('RFM9x error')

# Rutas para la página web
@app.route('/')
def index():
    return render_template('index.html')

# Eventos de Socket.IO
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')
    

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')
    
def send_message_to_esp32():
    while True:
        time.sleep(15)
        message = "De aquí a la luna"
        rfm9x.send(message.encode('utf-8'))
        print("Sent message: ", message)


def receive_data():
    pygame.init()

    while True:
        packet = rfm9x.receive()
        if packet:
            temp_celsius = int.from_bytes(packet[2:4], byteorder='little') / 10.00
            temp_fahrenheit = int.from_bytes(packet[4:6], byteorder='little') / 10.00
            temp_kelvin = int.from_bytes(packet[6:8], byteorder='little') / 10.00
            humd = int.from_bytes(packet[8:10], byteorder='little') / 10.00

            # Emitir los valores a través de Socket.IO como lo estabas haciendo
            socketio.emit('temp_celsius', temp_celsius)
            socketio.emit('temp_fahrenheit', temp_fahrenheit)
            socketio.emit('temp_kelvin', temp_kelvin)
            socketio.emit('humd', humd)

            # # Crear y reproducir el mensaje de voz
            # message = f"La temperatura actual es de {temp_celsius} grados Celsius."
            # tts = gTTS(text=message, lang='es')
            # tts.save('temperature.mp3')

            # # Reproducir el archivo de sonido utilizando pygame.mixer
            # pygame.mixer.init()
            # pygame.mixer.music.load('temperature.mp3')
            # pygame.mixer.music.play()
            # while pygame.mixer.music.get_busy():
            #     pygame.time.Clock().tick(10)

            print("Received temperature (Celsius):", temp_celsius, "C")
            print("Received temperature (Fahrenheit):", temp_fahrenheit, "F")
            print("Received temperature (Kelvin):", temp_kelvin, "K")
            print("Received humidity:", humd, "%")

        time.sleep(5)
           
            
       

if __name__ == '__main__':
    
    data_thread = threading.Thread(target=receive_data)
    data_thread.daemon = True
    data_thread.start()
    
    send_thread = threading.Thread(target=send_message_to_esp32)
    send_thread.daemon = True
    send_thread.start()
    # Ejecutar el servidor Flask en el hilo principal
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)