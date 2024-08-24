import cv2
import numpy as np
import torch
from torchvision import transforms

# Carregar os nomes das classes
with open('coco.names', 'r') as f:
    classes = f.read().splitlines()

# Carregar o modelo YOLOv3
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Capturar vídeo da webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)  # Tenta definir para 30 FPS, por exemplo

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Obter as dimensões do frame
    height, width = frame.shape[:2]

    # Preparar a imagem para o YOLOv3
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Obter as camadas de saída
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    # Fazer a predição
    outputs = net.forward(output_layers)

    # Processar as detecções
    boxes = []
    confidences = []
    class_ids = []
    for output in outputs:
        for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and class_id == 0:
                    # Caixa delimitadora
                    box = detection[0:4] * np.array([width, height, width, height])
                    (centerX, centerY, w, h) = box.astype("int")

                    x = int(centerX - (w / 2))
                    y = int(centerY - (h / 2))

                    boxes.append([x, y, int(w), int(h)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

    # Aplicar Non-Maxima Suppression (NMS)
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    if len(indices) > 0:
        print(len(indices))
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]

            # Desenhar a caixa e o rótulo no frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Mostrar o frame com as detecções
    cv2.imshow('YOLOv3 Webcam', frame)

    # Sair do loop pressionando a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar os recursos
cap.release()
cv2.destroyAllWindows()
