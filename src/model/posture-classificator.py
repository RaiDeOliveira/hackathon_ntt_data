import cv2
import mediapipe as mp
import math

# Função para calcular ângulo entre três pontos
def calculate_angle(a, b, c):
    ab = [a[0] - b[0], a[1] - b[1]]
    bc = [c[0] - b[0], c[1] - b[1]]
    
    dot_product = ab[0] * bc[0] + ab[1] * bc[1]
    magnitude_ab = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
    magnitude_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)
    
    angle = math.degrees(math.acos(dot_product / (magnitude_ab * magnitude_bc)))
    return angle

# Função para calcular o ângulo da cabeça em relação à linha dos ombros
def calculate_head_angle(head, left_shoulder, right_shoulder):
    shoulder_line = [right_shoulder[0] - left_shoulder[0], right_shoulder[1] - left_shoulder[1]]
    head_vector = [head[0] - left_shoulder[0], head[1] - left_shoulder[1]]
    
    dot_product = shoulder_line[0] * head_vector[0] + shoulder_line[1] * head_vector[1]
    magnitude_shoulder_line = math.sqrt(shoulder_line[0] ** 2 + shoulder_line[1] ** 2)
    magnitude_head_vector = math.sqrt(head_vector[0] ** 2 + head_vector[1] ** 2)
    
    angle = math.degrees(math.acos(dot_product / (magnitude_shoulder_line * magnitude_head_vector)))
    return angle

# Configurar o MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Iniciar captura de vídeo da webcam
cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar imagem")
        break

    # Converter a imagem para RGB
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Processar a imagem para detectar a pose
    results = pose.process(rgb_image)

    # Checar se landmarks da pose foram detectados
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Converter coordenadas normalizadas em pixels
        def get_coords(landmark):
            return int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
        
        # Pegar os pontos relevantes: ombros, cotovelo, pulso e cabeça
        left_shoulder = get_coords(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER])
        right_shoulder = get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER])
        left_elbow = get_coords(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW])
        left_wrist = get_coords(landmarks[mp_pose.PoseLandmark.LEFT_WRIST])
        head = get_coords(landmarks[mp_pose.PoseLandmark.NOSE])  # Utilizando o nariz como referência para a cabeça

        # Calcular ângulo entre ombro, cotovelo e pulso
        arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        
        # Calcular o ângulo da cabeça em relação à linha dos ombros
        head_angle = calculate_head_angle(head, left_shoulder, right_shoulder)

        # Verificar se a postura dos ombros está alinhada e a inclinação da cabeça
        shoulder_line_angle = calculate_angle(left_shoulder, right_shoulder, (left_shoulder[0] + 1, left_shoulder[1]))
        head_posture = abs(head_angle - shoulder_line_angle)

        # Critérios ajustados para postura sentada
        if 120 <= arm_angle <= 180 and head_posture < 40:
            posture = "Good posture"
        else:
            posture = "Bad posture"
        
        # Exibir ângulos e resultado
        cv2.putText(frame, f"Arm Angle: {arm_angle:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, f"Head Angle: {head_angle:.2f}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, posture, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        # Desenhar os pontos de pose
        mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Exibir o resultado na janela
    cv2.imshow('Posture Detection', frame)

    # Pressionar 'q' para sair do loop
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Liberar a captura e fechar janelas
cap.release()
cv2.destroyAllWindows()
