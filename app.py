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
import requests
# from gtts import gTTS
# import speech_recognition as sr


import firebase_admin 
from firebase_admin import credentials, db, auth


# Inicializar Firebase Admin SDK
cred = credentials.Certificate("credentials.json")  # Reemplaza con la ubicación de tu archivo JSON
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sensores-apolo-default-rtdb.firebaseio.com/'
})

firebase_api_key = 'AIzaSyBq2szFMd4NMYOtl5hrtr6M0DzPNG3lbs8'

# ...

# Autenticar un usuario con correo y contraseña
email = "adames1601@gmail.com"
password = "Apolo27@"

url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"
data = {
    "email": email,
    "password": password,
    "returnSecureToken": True
}
response = requests.post(url, json=data)
print(response)
if response.status_code == 200:
    json_response = response.json()
    token = json_response['idToken']
    print(f"Token: {token}")
    verify = auth.verify_id_token(token)
    print(f"Verify: {verify}")
else:
    raise Exception(f"Error: {response.status_code} - {response.text}")

# try:
#     # Intentar iniciar sesión con correo y contraseña
#     user = auth.get_user_by_email(email)
# except Exception as e:
#     # Manejar cualquier excepción relacionada con la autenticación
#     print(f"Error de autenticación: {e}")
#     user = None

# Crear un token personalizado


# Referencia a la base de datos en tiempo real con autenticación
ref = db.reference('/temperatura-humedad')

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
        
# # Nueva función para reconocer voz desde el micrófono
# def recognize_speech():
#     recognizer = sr.Recognizer()
#     microphone = sr.Microphone()

#     with microphone as source:
#         print("Escuchando...")
#         audio = recognizer.listen(source)

#     try:
#         recognized_text = recognizer.recognize_google(audio, language="es-ES")
#         return recognized_text
#     except sr.UnknownValueError:
#         return "No se pudo entender el audio"
#     except sr.RequestError:
#         return "No se pudo conectar con el servicio de reconocimiento de voz"


# def send_audio_to_esp32():
#     while True:
#         # Reconocer voz desde el micrófono
#         recognized_text = recognize_speech()
#         rfm9x.send(recognized_text.encode('utf-8'))
#         print("Enviado mensaje de voz: ", recognized_text)
#         time.sleep(15)


# Función para enviar datos a Firebase

def send_to_firebase(temp_celsius, humd, presionAt, AlturaMar, temp_celsius2, humd_rel2, presionAt2, AlturaMar2):
    try:
        # Enviar datos a Firebase
        data = {
            'temperatura1': temp_celsius,
            'humedad1': humd,
            'presionAt1': presionAt,
            'AlturaMar1': AlturaMar,
            'temperatura2': temp_celsius2,
            'humedad2': humd_rel2,
            'presionAt2': presionAt2,
            'AlturaMar2': AlturaMar2,
            'timestamp': int(time.time() * 1000)  # Agregar un timestamp en milisegundos
        }
        ref.push(data)
        print("Datos enviados a Firebase con éxito")
    except Exception as e:
        print("Error al enviar datos a Firebase:", str(e))




def receive_data():
    #pygame.init()

    while True:
        
        packet = rfm9x.receive()
        print(packet)
        if packet:
            temp_celsius1 = int.from_bytes(packet[2:4], byteorder='little') / 100.00
            humd_rel1 = int.from_bytes(packet[4:6], byteorder='little') / 100.00
            presionAt1 = int.from_bytes(packet[6:8], byteorder='little') / 100.00
            AlturaMar1 = int.from_bytes(packet[8:10], byteorder='little') / 100.00
            temp_celsius2 = int.from_bytes(packet[10:12], byteorder='little') / 100.00
            humd_rel2 = int.from_bytes(packet[12:14], byteorder='little') / 100.00
            presionAt2 = int.from_bytes(packet[14:16], byteorder='little') / 100.00
            AlturaMar2 = int.from_bytes(packet[16:18], byteorder='little') / 100.00

            # Emitir los valores a través de Socket.IO para que la página web los reciba
            socketio.emit('temp_celsius', temp_celsius1)
            socketio.emit('humd_rel', humd_rel1)
            socketio.emit('presionAt', presionAt1)
            socketio.emit('AlturaMar', AlturaMar1)
            
            
            # FUNCIONALIDAD DEL AUDIO

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
            print("-------------------Piloto 1-------------------")
            print("Received temperatura relativa:", temp_celsius1, "C")
            print("Received humedad relativa:", humd_rel1, "F")
            print("Received presion atmosférica:", presionAt1, "hPa")
            print("Received Altura mar:", AlturaMar1, "m")
            print("")
            print("-------------------Piloto 2-------------------")
            print("Received temperatura relativa:", temp_celsius2, "C")
            print("Received humedad relativa:", humd_rel2, "F")
            print("Received presion atmosférica:", presionAt2, "hPa")
            print("Received Altura mar:", AlturaMar2, "m")
            print("")
            
            # Enviar datos a Firebase
            send_to_firebase(temp_celsius1, humd_rel1, presionAt1, AlturaMar1, temp_celsius2, humd_rel2, presionAt2, AlturaMar2)

        time.sleep(5)
        
# Iniciar el servidor Flask y los hilos de ejecución

if __name__ == '__main__':
    
    data_thread = threading.Thread(target=receive_data)
    data_thread.daemon = True
    data_thread.start()
    
    send_thread = threading.Thread(target=send_message_to_esp32)
    send_thread.daemon = True
    send_thread.start()
    
    # FUNCIONALIDAD DEL AUDIO
    
    # send_audio_thread = threading.Thread(target=send_audio_to_esp32)
    # send_audio_thread.daemon = True
    #send_audio_thread.start()
    
    # Ejecutar el servidor Flask en el hilo principal
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)