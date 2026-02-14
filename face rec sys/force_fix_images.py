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

        if not file.lower().endswith((".jpg", ".jpeg")):
            continue

        try:
            img = Image.open(path)
            img = img.convert("RGB")  # force RGB 8-bit
            img.save(path, "JPEG", quality=95, subsampling=0)
            print(f"Re-encoded: {path}")
        except Exception as e:
            print(f"FAILED: {path} → {e}")
