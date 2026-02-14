import cv2
import face_recognition
import pickle
import csv
import os
from datetime import datetime
import pyttsx3
import threading
import queue
import time

ENCODINGS_FILE = "encodings.pickle"
ATTENDANCE_FILE = f"attendance_{datetime.now().strftime('%Y-%m-%d')}.csv"

voice_queue = queue.Queue()
engine = pyttsx3.init()
engine.setProperty("rate", 160)

def voice_worker():
    while True:
        text = voice_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()
        voice_queue.task_done()
        time.sleep(0.2)

# Start voice thread
threading.Thread(target=voice_worker, daemon=True).start()

if os.path.exists(ENCODINGS_FILE):
    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)
        known_encodings = data["encodings"]
        known_names = data["names"]
else:
    print("Encodings file not found. Run encode_faces.py first.")
    exit()

cap = cv2.VideoCapture(0)
attendance_marked = set()

if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Time"])

print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)

    for encoding, box in zip(encodings, boxes):
        matches = face_recognition.compare_faces(known_encodings, encoding)
        name = "Unknown"

        if True in matches:
            matched_idxs = [i for i, b in enumerate(matches) if b]
            counts = {}

            for i in matched_idxs:
                counts[known_names[i]] = counts.get(known_names[i], 0) + 1

            name = max(counts, key=counts.get)

            if name not in attendance_marked:
                now = datetime.now().strftime("%H:%M:%S")

                with open(ATTENDANCE_FILE, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([name, now])

                attendance_marked.add(name)

                # 🔊 Push to voice queue
                voice_queue.put(f"Attendance marked for {name}")

        top, right, bottom, left = box
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(
            frame,
            name,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 0),
            2
        )

    cv2.imshow("Face Recognition Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# Stop voice thread
voice_queue.put(None)
