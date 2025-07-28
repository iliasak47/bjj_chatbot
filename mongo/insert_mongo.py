import json, os
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["bjj_chatbot"]
collection = db["segments"]

# Création d’un index unique pour éviter les doublons
collection.create_index(
    [("instructional", 1), ("start", 1), ("text", 1)],
    unique=True
)

# Construction du chemin vers le dossier "data/transcriptions"
base_dir = os.path.dirname(os.path.dirname(__file__))  # remonte à la racine du projet
transcriptions_dir = os.path.join(base_dir, "data", "transcriptions")

# Parcours des fichiers JSON de transcription
for file in os.listdir(transcriptions_dir):
    if file.endswith(".json"):
        file_path = os.path.join(transcriptions_dir, file)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for seg in data["segments"]:
                try:
                    collection.insert_one({
                        "instructional": data["instructional"],
                        "start": seg["start"],
                        "end": seg["end"],
                        "text": seg["text"]
                    })
                except:
                    pass  # Ignore les doublons déjà insérés
        print(f" Checked: {file}")
