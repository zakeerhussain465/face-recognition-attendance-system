import face_recognition
import cv2
import os
import pickle

DATASET_DIR = "dataset"
ENCODINGS_FILE = "encodings.pickle"

known_encodings = []
known_names = []

print("Scanning dataset...")

for name in os.listdir(DATASET_DIR):
    person_dir = os.path.join(DATASET_DIR, name)

    if not os.path.isdir(person_dir):
        continue

    images = os.listdir(person_dir)

    if len(images) == 0:
        print(f"[SKIP] No images in folder: {name}")
        continue

    print(f"Processing: {name}")

    for image_name in images:
        image_path = os.path.join(person_dir, image_name)

        try:
            image = cv2.imread(image_path)

            if image is None:
                print(f"[SKIP] Cannot read: {image_path}")
                continue

            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb, model="hog")

            if len(boxes) == 0:
                print(f"[SKIP] No face found: {image_path}")
                continue

            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(name)

        except Exception as e:
            print(f"[SKIP] Error with file {image_path}: {e}")
            continue

print("Total faces encoded:", len(known_encodings))

data = {"encodings": known_encodings, "names": known_names}

with open(ENCODINGS_FILE, "wb") as f:
    f.write(pickle.dumps(data))

print("Encoding completed successfully.")
