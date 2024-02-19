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
<<<<<<< HEAD
# from gtts import gTTS
# import speech_recognition as sr


import firebase_admin 
from firebase_admin import credentials, db, auth


# Autenticar un usuario con correo y contraseña
email = "adames1601@gmail.com"
password = "Apolo27@"

try:
    # Intentar iniciar sesión con correo y contraseña
    user = auth.get_user_by_email(email)
except auth.AuthError:
    # Si el usuario no existe, crearlo
    user = auth.create_user(
        email=email,
        password=password
    )

# Crear un token personalizado
custom_token = auth.create_custom_token(user.uid)

# Inicializar Firebase Admin SDK con el token personalizado
cred = credentials.Certificate("credentials.json")  # Reemplaza con la ubicación de tu archivo JSON
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sensores-apolo-default-rtdb.firebaseio.com/'
}, name='sensores-apolo', options={
    'databaseAuthVariableOverride': {
        'uid': user.uid,
        'token': custom_token
    }
})

# ...

# Referencia a la base de datos en tiempo real con autenticación
ref = db.reference('/temperatura-humedad', app=firebase_admin.get_app(name='sensores-apolo'))
=======
from gtts import gTTS
import speech_recognition as sr


# import firebase_admin
# from firebase_admin import credentials, db


# Inicializar Firebase Admin SDK
# cred = credentials.Certificate("credentials.json")  # Reemplaza con la ubicación de tu archivo JSON
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://sensores-apolo-default-rtdb.firebaseio.com/'
# })

>>>>>>> f9d15f0c456c2f6ab410d32447294f888f282acc
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
        
<<<<<<< HEAD
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

def send_to_firebase(temp_celsius, humd):
    try:
        # Enviar datos a Firebase
        data = {
            'temperatura': temp_celsius,
            'humedad': humd,
            'timestamp': int(time.time() * 1000)  # Agregar un timestamp en milisegundos
        }
        ref.push(data)
        print("Datos enviados a Firebase con éxito")
    except Exception as e:
        print("Error al enviar datos a Firebase:", str(e))




def receive_data():
    #pygame.init()
=======
# Nueva función para reconocer voz desde el micrófono
def recognize_speech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Escuchando...")
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio, language="es-ES")
        return recognized_text
    except sr.UnknownValueError:
        return "No se pudo entender el audio"
    except sr.RequestError:
        return "No se pudo conectar con el servicio de reconocimiento de voz"


def send_audio_to_esp32():
    while True:
        # Reconocer voz desde el micrófono
        recognized_text = recognize_speech()
        rfm9x.send(recognized_text.encode('utf-8'))
        print("Enviado mensaje de voz: ", recognized_text)
        time.sleep(15)



def receive_data():
    pygame.init()
>>>>>>> f9d15f0c456c2f6ab410d32447294f888f282acc

    while True:
        
        packet = rfm9x.receive()
        if packet:
            temp_celsius = int.from_bytes(packet[2:4], byteorder='little') / 100.00
            temp_fahrenheit = int.from_bytes(packet[4:6], byteorder='little') / 100.00
            temp_kelvin = int.from_bytes(packet[6:8], byteorder='little') / 100.00
            humd = int.from_bytes(packet[8:10], byteorder='little') / 100.00

<<<<<<< HEAD
            # Emitir los valores a través de Socket.IO para que la página web los reciba
=======
            # Emitir los valores a través de Socket.IO como lo estabas haciendo
>>>>>>> f9d15f0c456c2f6ab410d32447294f888f282acc
            socketio.emit('temp_celsius', temp_celsius)
            socketio.emit('temp_fahrenheit', temp_fahrenheit)
            socketio.emit('temp_kelvin', temp_kelvin)
            socketio.emit('humd', humd)
<<<<<<< HEAD
            
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
=======

            # Crear y reproducir el mensaje de voz
            message = f"La temperatura actual es de {temp_celsius} grados Celsius."
            tts = gTTS(text=message, lang='es')
            tts.save('temperature.mp3')

            # Reproducir el archivo de sonido utilizando pygame.mixer
            pygame.mixer.init()
            pygame.mixer.music.load('temperature.mp3')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
>>>>>>> f9d15f0c456c2f6ab410d32447294f888f282acc

            print("Received temperature (Celsius):", temp_celsius, "C")
            print("Received temperature (Fahrenheit):", temp_fahrenheit, "F")
            print("Received temperature (Kelvin):", temp_kelvin, "K")
            print("Received humidity:", humd, "%")
<<<<<<< HEAD
            
            # Enviar datos a Firebase
            send_to_firebase(temp_celsius, humd)

        time.sleep(5)
        
# Iniciar el servidor Flask y los hilos de ejecución
=======

        time.sleep(5)
           
            
       
>>>>>>> f9d15f0c456c2f6ab410d32447294f888f282acc

if __name__ == '__main__':
    
    data_thread = threading.Thread(target=receive_data)
    data_thread.daemon = True
    data_thread.start()
    
    # send_thread = threading.Thread(target=send_message_to_esp32)
    # send_thread.daemon = True
    # send_thread.start()
    
<<<<<<< HEAD
    # FUNCIONALIDAD DEL AUDIO
    
    # send_audio_thread = threading.Thread(target=send_audio_to_esp32)
    # send_audio_thread.daemon = True
    #send_audio_thread.start()
    
=======
    send_audio_thread = threading.Thread(target=send_audio_to_esp32)
    send_audio_thread.daemon = True
    send_audio_thread.start()
>>>>>>> f9d15f0c456c2f6ab410d32447294f888f282acc
    # Ejecutar el servidor Flask en el hilo principal
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)