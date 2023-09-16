import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_rfm9x
import socketio
from flask import Flask, render_template
from flask_socketio import SocketIO, emit 
import threading
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

def receive_data():
    while True:
        packet = rfm9x.receive()
        if packet:
            temp = int.from_bytes(packet[2:4], byteorder='little') / 10.00
            humd = int.from_bytes(packet[4:6], byteorder='little') / 10.00
            
            # if((temp > 0 or temp < 50)  and (humd > 0 or humd < 100)):
                
            #     # Crear una referencia a la base de datos de Firebase
            #     ref = db.reference('/temperatura-humedad')

            #     # Crear un nuevo registro en la base de datos con la temperatura y humedad
            #     new_data = {
            #         'temperatura': temp,
            #         'humedad': humd
            #     }
            #     ref.push(new_data)
        
            socketio.emit('temp', temp)  
            socketio.emit('humd', humd)
           
            print("Received temperature:", temp, "C")
            print("Received humidity:", humd, "%")
            
        time.sleep(5)
           
            
       

if __name__ == '__main__':
    
    data_thread = threading.Thread(target=receive_data)
    data_thread.daemon = True
    data_thread.start()
    # Ejecutar el servidor Flask en el hilo principal
    socketio.run(app, host='0.0.0.0', port=3000, debug=True)