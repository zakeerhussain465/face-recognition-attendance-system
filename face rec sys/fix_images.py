from PIL import Image
import os

BASE_DIR = "dataset"

for person in os.listdir(BASE_DIR):
    person_dir = os.path.join(BASE_DIR, person)

    if not os.path.isdir(person_dir):
        continue

    print(f"Fixing images for: {person}")

    for file in os.listdir(person_dir):
        path = os.path.join(person_dir, file)

        try:
            img = Image.open(path)
            img = img.convert("RGB")
            img.save(path, "JPEG")
            print(f"Fixed: {path}")
        except Exception as e:
            print(f"Failed: {path} → {e}")
