import cv2
import mediapipe as mp
import math

# Função para calcular o ângulo entre três pontos
def calculate_angle(a, b, c):
    ab = [a[0] - b[0], a[1] - b[1]]
    bc = [c[0] - b[0], c[1] - b[1]]
    
    dot_product = ab[0] * bc[0] + ab[1] * bc[1]
    magnitude_ab = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
    magnitude_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)
    
    angle = math.degrees(math.acos(dot_product / (magnitude_ab * magnitude_bc)))
    return angle

# Função para calcular o alinhamento da cabeça em relação aos ombros
def calculate_head_angle(head, left_shoulder, right_shoulder):
    shoulder_line = [right_shoulder[0] - left_shoulder[0], right_shoulder[1] - left_shoulder[1]]
    head_vector = [head[0] - left_shoulder[0], head[1] - left_shoulder[1]]
    
    dot_product = shoulder_line[0] * head_vector[0] + shoulder_line[1] * head_vector[1]
    magnitude_shoulder_line = math.sqrt(shoulder_line[0] ** 2 + shoulder_line[1] ** 2)
    magnitude_head_vector = math.sqrt(head_vector[0] ** 2 + head_vector[1] ** 2)
    
    angle = math.degrees(math.acos(dot_product / (magnitude_shoulder_line * magnitude_head_vector)))
    return angle

# Inicializar o MediaPipe para detecção de múltiplas poses (BlazePose)
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Iniciar captura de vídeo da webcam
cap = cv2.VideoCapture(1)

with mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar imagem")
            break

        # Converter a imagem para RGB
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Processar a imagem e detectar múltiplas poses
        results = pose.process(rgb_image)

        # Verificar se há poses detectadas
        if results.pose_landmarks:
            h, w, _ = frame.shape

            # Se houver apenas uma pessoa detectada
            landmarks = results.pose_landmarks.landmark
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Função auxiliar para converter coordenadas
            def get_coords(landmark, w, h):
                return int(landmark.x * w), int(landmark.y * h)

            # Coletar coordenadas de ombros, cotovelos, punho e cabeça
            try:
                left_shoulder = get_coords(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value], w, h)
                right_shoulder = get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value], w, h)
                left_elbow = get_coords(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value], w, h)
                left_wrist = get_coords(landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value], w, h)
                head = get_coords(landmarks[mp_pose.PoseLandmark.NOSE.value], w, h)

                # Calcular o ângulo do braço esquerdo (ombro-cotovelo-punho)
                arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

                # Calcular o alinhamento da cabeça em relação à linha dos ombros
                head_angle = calculate_head_angle(head, left_shoulder, right_shoulder)

                # Avaliar a postura com base nos ângulos calculados
                shoulder_line_angle = calculate_angle(left_shoulder, right_shoulder, (left_shoulder[0] + 1, left_shoulder[1]))
                head_posture = abs(head_angle - shoulder_line_angle)

                # Critérios para boa postura de ombros, cabeça e braço
                if 120 <= arm_angle <= 160 and head_posture < 70 and shoulder_line_angle < 10:
                    posture = "Good posture"
                else:
                    posture = "Bad posture"

                # Exibir ângulos e status da postura no frame
                cv2.putText(frame, f"Arm Angle: {arm_angle:.2f}", (left_shoulder[0] - 50, left_shoulder[1] - 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(frame, f"Head Angle: {head_angle:.2f}", (left_shoulder[0] - 50, left_shoulder[1] - 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(frame, posture, (left_shoulder[0] - 50, left_shoulder[1] - 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if posture == "Bad posture" else (0, 255, 0), 2, cv2.LINE_AA)
            except Exception as e:
                print(f"Error processing landmarks: {e}")

        # Mostrar o frame com os resultados
        cv2.imshow('Posture Detection - Multiple People', frame)

        # Pressione 'q' para sair do loop
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Liberar a captura de vídeo e fechar janelas
cap.release()
cv2.destroyAllWindows()
