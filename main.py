import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

# Constants
width = 1280
height = 720

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# MediaPipe Hand Detector
detector = HandDetector(maxHands=2, detectionCon=0.8)

# Communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("127.0.0.1", 42111)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    # Landmarks
    data = []
    if hands:
        if len(hands) == 1:
            handr = hands[0] if hands[0]["type"] == "Right" else None
            handl = hands[0] if hands[0]["type"] == "Left" else None
        else:
            handr = hands[0] if hands[0]["type"] == "Right" else hands[1]
            handl = hands[0] if hands[0]["type"] == "Left" else hands[1]

        # Left Hand
        if handl:
            lmListl = handl["lmList"]
            for lm in lmListl:
                x, y, z = lm
                data.extend([x, height - y, z])
        else:
            for _ in range(21):
                data.extend([0, 0, 0])

        # Right Hand
        if handr:
            lmListr = handr["lmList"]
            for lm in lmListr:
                x, y, z = lm
                data.extend([x, height - y, z])
        else:
            for _ in range(21):
                data.extend([0, 0, 0])

        sock.sendto(str.encode(str(data)), server_address)
    cv2.imshow("Webcam", img)
    cv2.waitKey(1)
