from flask import Flask, Response, jsonify
from ultralytics import YOLO
import cv2

app = Flask(__name__)

# Carregue o modelo YOLO
model = YOLO("model.pt")

@app.route('/video')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Fazer a predição com o YOLO
        results = model.predict(source=frame)

        # Desenhar as detecções no frame
        annotated_frame = results[0].plot()

        # Converter o frame para JPEG
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        # Enviar o frame para o frontend
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

if __name__ == '__main__':
    app.run(debug=True)
