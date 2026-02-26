import cv2
import mediapipe as mp
import paho.mqtt.client as mqtt
import time


MQTT_BROKER = "127.0.0.1"
MQTT_TOPIC = "robot/mano/motori"

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)
client.loop_start()


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cv2.namedWindow("Mano Robotica Vision", cv2.WINDOW_NORMAL)

print("Sistema di visione avviato! Premi 'q' per uscire.")

ultimo_payload = ""

while cap.isOpened():
    success, img = cap.read()
    if not success: continue

    img = cv2.resize(img, (640, 360))
    img = cv2.flip(img, 1) 
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            punti_punta = [4, 8, 12, 16, 20] 
            angoli = []

            for i, tip in enumerate(punti_punta):
                if tip == 4: # Pollice
                    is_open = handLms.landmark[tip].x < handLms.landmark[tip-2].x
                else: # Altre dita
                    is_open = handLms.landmark[tip].y < handLms.landmark[tip-2].y
                
                angoli.append("0" if is_open else "180")

            payload = ",".join(angoli)
            
            # Invia a Mosquitto SOLO se la posa è cambiata
            if payload != ultimo_payload:
                print(f"-> Nuovo comando inviato: {payload}")
                try:
                    client.publish(MQTT_TOPIC, payload)
                    ultimo_payload = payload
                except Exception as e:
                    print("Errore MQTT:", e)
            
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Mano Robotica Vision", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
