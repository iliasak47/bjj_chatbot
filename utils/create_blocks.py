import math
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np

#  Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["bjj_chatbot"]
segments_col = db["segments"]
blocks_col = db["segments_blocks"]

model = SentenceTransformer("all-MiniLM-L6-v2")

BLOCK_DURATION = 60  # en secondes

def create_blocks():
    """
    Regroupe les segments en blocs de 60 s
    et insère dans la collection segments_blocks avec embeddings.
    """

    #  Parcourir tous les instructionals déjà dans la base
    instructionals = segments_col.distinct("instructional")

    for instructional in instructionals:
        print(f"\n Processing instructional: {instructional}")

        #  Récupérer tous les segments de cet instructional (triés par start)
        segs = list(segments_col.find({"instructional": instructional}).sort("start", 1))

        if not segs:
            continue

        #  On découpe en blocs de 60 s
        start_time = segs[0]["start"]
        end_time = segs[-1]["end"]
        total_blocks = math.ceil((end_time - start_time) / BLOCK_DURATION)

        for i in range(total_blocks):
            block_start = i * BLOCK_DURATION
            block_end = block_start + BLOCK_DURATION

            #  Récupérer les segments qui tombent dans ce bloc
            block_texts = [
                s["text"] for s in segs if block_start <= s["start"] < block_end
            ]

            if not block_texts:
                continue

            full_text = " ".join(block_texts)

            #  Vérifier si ce bloc existe déjà pour éviter les doublons
            if blocks_col.find_one(
                {"instructional": instructional, "start": block_start}
            ):
                continue

            #  Générer l'embedding pour ce bloc
            embedding = model.encode(full_text).tolist()

            #  Insérer le bloc
            blocks_col.insert_one(
                {
                    "instructional": instructional,
                    "start": block_start,
                    "end": block_end,
                    "text": full_text,
                    "embedding": embedding,
                }
            )

        print(f" Done: {instructional}")

    print("\n🎉 All blocks created and embeddings generated!")

if __name__ == "__main__":
    create_blocks()
