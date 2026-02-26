# Robotic-Hand
AI-controlled robotic hand. It tracks human gestures via webcam using Python and MediaPipe, transmitting commands to an ESP32 via MQTT to move the fingers in real-time. Features a Node-RED dashboard for live telemetry and Digital Twin monitoring.

## Demo
![GIF-2026-02-26-02-41-30](https://github.com/user-attachments/assets/438bf503-cd2d-4dcf-898b-97670dd7c455)

## Features
* **Real-Time Hand Tracking:** Uses Google MediaPipe to map 21 3D hand landmarks at 30 FPS.
* **Low-Latency Communication:** Utilizes the MQTT protocol for instant data transmission between the host Mac and the ESP32.
* **Independent Finger Control:** 5 SG90 servo motors controlled with PWM to mimic individual finger movements.
* **Live Telemetry & Digital Twin:** A Node-RED dashboard displays the physical robot's digital twin and real-time Wi-Fi signal strength (RSSI).

## Hardware Pinout
The project runs on an ESP32 microcontroller. Here is the wiring configuration for the servo motors:

| Finger | ESP32 GPIO Pin | Motor |
| :--- | :--- | :--- |
| Thumb (Pollice) | GPIO 26 | Servo 1 |
| Index (Indice) | GPIO 27 | Servo 2 |
| Middle (Medio) | GPIO 14 | Servo 3 |
| Ring (Anulare) | GPIO 12 | Servo 4 |
| Pinky (Mignolo) | GPIO 13 | Servo 5 |

## Software Stack
* **Microcontroller:** MicroPython, `umqttsimple`
* **Computer Vision:** Python 3, OpenCV, MediaPipe
* **Networking & IoT:** Mosquitto MQTT Broker, Node-RED
