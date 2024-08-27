import cv2
import mediapipe as mp
import math
import base64
import io
import sys
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from ultralytics import YOLO
from starlette.websockets import WebSocketState
import time

# Funções para cálculo da postura
def calculate_angle(a, b, c):
    ab = [a[0] - b[0], a[1] - b[1]]
    bc = [c[0] - b[0], c[1] - b[1]]
    
    dot_product = ab[0] * bc[0] + ab[1] * bc[1]
    magnitude_ab = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
    magnitude_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)
    
    angle = math.degrees(math.acos(dot_product / (magnitude_ab * magnitude_bc)))
    return angle

def calculate_head_angle(head, left_shoulder, right_shoulder):
    shoulder_line = [right_shoulder[0] - left_shoulder[0], right_shoulder[1] - left_shoulder[1]]
    head_vector = [head[0] - left_shoulder[0], head[1] - left_shoulder[1]]
    
    dot_product = shoulder_line[0] * head_vector[0] + shoulder_line[1] * head_vector[1]
    magnitude_shoulder_line = math.sqrt(shoulder_line[0] ** 2 + shoulder_line[1] ** 2)
    magnitude_head_vector = math.sqrt(head_vector[0] ** 2 + head_vector[1] ** 2)
    
    angle = math.degrees(math.acos(dot_product / (magnitude_shoulder_line * magnitude_head_vector)))
    return angle

# YOLO model
model = YOLO("model.pt")

# Inicializar o MediaPipe para detecção de múltiplas poses (BlazePose)
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

app = FastAPI()

async def capture_logs(frame):
    log_capture_string = io.StringIO()
    sys.stdout = log_capture_string
    results = model.predict(source=frame)
    sys.stdout = sys.__stdout__
    logs = log_capture_string.getvalue()
    return logs, results

async def generate_video_feed(websocket: WebSocket):
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Fazer a predição YOLO
            logs, results = await capture_logs(frame)
            
            # Converter a imagem para RGB e detectar poses com MediaPipe
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pose_results = pose.process(rgb_image)
            
            num_people = sum([1 for r in results[0].boxes.data if int(r[-1]) == 0])  # Classe 'person' tem o ID 0
            posture = "No data"

            # Verificar se há poses detectadas
            if pose_results.pose_landmarks:
                h, w, _ = frame.shape
                landmarks = pose_results.pose_landmarks.landmark
                left_shoulder = (int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w),
                                 int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h))
                right_shoulder = (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * w),
                                  int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * h))
                left_elbow = (int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * w),
                              int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * h))
                left_wrist = (int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * w),
                              int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * h))
                head = (int(landmarks[mp_pose.PoseLandmark.NOSE.value].x * w),
                        int(landmarks[mp_pose.PoseLandmark.NOSE.value].y * h))
                
                arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                head_angle = calculate_head_angle(head, left_shoulder, right_shoulder)
                shoulder_line_angle = calculate_angle(left_shoulder, right_shoulder, (left_shoulder[0] + 1, left_shoulder[1]))
                head_posture = abs(head_angle - shoulder_line_angle)
                
                if 120 <= arm_angle <= 180 and head_posture < 40:
                    posture = "Good posture"
                else:
                    posture = "Bad posture"

            # Desenhar as detecções no frame
            annotated_frame = results[0].plot()
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()
            frame_base64 = base64.b64encode(frame).decode('utf-8')

            # Enviar o frame, número de pessoas e postura via WebSocket
            await websocket.send_json({
                'frame': frame_base64,
                'num_people': num_people,
                'head_angle': head_angle,
                'arm_angle': arm_angle,
                'posture': posture
            })

            await asyncio.sleep(1)

    cap.release()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await generate_video_feed(websocket)
    except WebSocketDisconnect:
        print("Client disconnected")
