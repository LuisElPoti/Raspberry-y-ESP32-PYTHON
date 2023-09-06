from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')  # Crea un archivo HTML para mostrar los datos en la página web

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

@socketio.on('send_data')
def handle_data(data):
    print('Datos recibidos:', data)
    emit('update_data', data, broadcast=True)  # Emitir datos a todos los clientes conectados

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
