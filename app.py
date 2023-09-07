import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_rfm9x
import socketio
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Configurar RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 868.2)
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

@socketio.on('send_data')
def handle_data(data):
    print('Datos recibidos:', data)
    emit('update_data', data, broadcast=True)

def obtain_and_emit_sensor_data():
    while True:
        packet = rfm9x.receive()
        if packet:
            temp = int.from_bytes(packet[2:4], byteorder='little') / 10.0
            humd = int.from_bytes(packet[4:6], byteorder='little') / 10.0

            print("Received temperature:", temp, "C")
            print("Received humidity:", humd, "%")
            
            socketio.emit('send_data', {'temp': temp, 'humd': humd})
            
        time.sleep(6)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    obtain_and_emit_sensor_data()