import cv2
import os

name = input("Enter student name: ").strip()

folder = f"dataset/{name}"
os.makedirs(folder, exist_ok=True)

cap = cv2.VideoCapture(0)
count = 0

print("Press 's' to save image, 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Register Student", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        img_path = f"{folder}/{count+1}.jpg"
        cv2.imwrite(img_path, frame)
        print(f"Saved: {img_path}")
        count += 1

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("Now run encode_faces.py to update encodings.")
