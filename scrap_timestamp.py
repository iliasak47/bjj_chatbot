import os
import re
from pymongo import MongoClient

def time_to_seconds(t):
    parts = list(map(int, t.strip().split(":")))
    if len(parts) == 2:
        m, s = parts
        return m * 60 + s
    elif len(parts) == 3:
        h, m, s = parts
        return h * 3600 + m * 60 + s
    return 0.0

def parse_chapters_from_text(text):
    volumes = {}
    current_volume = None
    line_re = re.compile(r"^(.*?)\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*[-–]\s*(\d{1,2}:\d{2}(?::\d{2})?)$")

    for line in text.splitlines():
        line = line.strip()
        if not line or line in {"CHAPTER TITLE", "START TIME"}:
            continue
        if line.lower().startswith("volume"):
            current_volume = int(re.search(r"\d+", line).group())
            volumes[current_volume] = []
            continue
        if current_volume is not None:
            match = line_re.match(line)
            if match:
                title, start, end = match.groups()
                volumes[current_volume].append({
                    "title": title.strip(),
                    "start": time_to_seconds(start),
                    "end": time_to_seconds(end)
                })
    return volumes

if __name__ == "__main__":
    folder_path = "data/timestamp"

    # Connexion MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["bjj_chatbot"]
    collection = db["chapters_by_volume"]

    for filename in os.listdir(folder_path):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(folder_path, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        volumes = parse_chapters_from_text(text)

        for vol, chapters in volumes.items():
            collection.update_one(
                {"volume": vol, "source": filename},  # Ajoute "source" pour tracer le fichier
                {"$set": {"chapters": chapters}},
                upsert=True
            )
            print(f"✅ {filename} → Volume {vol} : {len(chapters)} chapitres insérés.")

    print("✅ Tous les fichiers .txt traités et insérés.")
