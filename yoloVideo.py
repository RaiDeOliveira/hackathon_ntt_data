from flask import Flask
from flask_socketio import SocketIO, emit
from ultralytics import YOLO
import cv2
import base64
import io
import sys

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Carregue o modelo YOLO
model = YOLO("model.pt")

def capture_logs(frame):
    # Crie um buffer de StringIO para capturar stdout
    log_capture_string = io.StringIO()
    sys.stdout = log_capture_string
    
    # Fazer a predição com o YOLO (isto vai gerar logs no stdout)
    results = model.predict(source=frame)
    
    # Restaurar stdout original
    sys.stdout = sys.__stdout__

    # Capturar o conteúdo dos logs
    logs = log_capture_string.getvalue()

    return logs, results

def generate_video_feed():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Capture os logs e obtenha os resultados da predição
        logs, results = capture_logs(frame)

        # Desenhar as detecções no frame
        annotated_frame = results[0].plot()

        # Converter o frame para JPEG
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        # Codificar o frame em base64 para enviar via WebSocket
        frame_base64 = base64.b64encode(frame).decode('utf-8')

        # Contar o número de pessoas
        num_people = sum([1 for r in results[0].boxes.data if int(r[-1]) == 0])  # Classe 'person' tem o ID 0

        # Enviar o frame e o número de pessoas via WebSocket
        socketio.emit('video_feed', {'frame': frame_base64, 'num_people': num_people})

    cap.release()

@socketio.on('connect')
def handle_connect():
    # Inicia o envio do feed de vídeo quando o cliente se conecta
    socketio.start_background_task(generate_video_feed)

if __name__ == '__main__':
    socketio.run(app, debug=True)
