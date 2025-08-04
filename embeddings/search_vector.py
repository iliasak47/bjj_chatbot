from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["bjj_chatbot"]
collection = db["segments_blocks"]  # On travaille avec les blocs

# Chargement du modèle d'embeddings 
model = SentenceTransformer("all-MiniLM-L6-v2")

def search_vector(query, top_k=3):  # top_k plus petit pour éviter trop de doublons
    """
    Recherche vectorielle dans les blocs et ajoute contexte avant/après.
    """
    query_emb = model.encode(query)
    results = []

    # 1) Parcourir les blocs
    for seg in collection.find({"embedding": {"$exists": True}}):
        emb = np.array(seg["embedding"])
        sim = np.dot(query_emb, emb) / (
            np.linalg.norm(query_emb) * np.linalg.norm(emb)
        )
        results.append((sim, seg))

    # 2) Trier et prendre les top_k blocs pertinents
    top_blocks = sorted(results, key=lambda x: x[0], reverse=True)[:top_k]

    already_seen = set()  # Pour éviter les doublons

    for sim, block in top_blocks:
        instructional = block["instructional"]
        start = block["start"]

        # Cherche les blocs : précédent, actuel, suivant
        for offset in [-60, 0, 60]:
            adj_start = start + offset
            key = f"{instructional}-{adj_start}"
            if key in already_seen:
                continue

            adj_block = collection.find_one({
                "instructional": instructional,
                "start": adj_start
            })

            if adj_block:
                already_seen.add(key)
                minutes = round(adj_block["start"] / 60, 2)
                print(f"\n✅ Similarity: {round(sim, 2)}" if offset == 0 else "")
                print(f"➡️ Context: {adj_block['text']}")
                print(f"▶️ Instructional: {adj_block['instructional']}")
                print(f"⏱️ Timestamp: {minutes} min")

if __name__ == "__main__":
    q = input("Ask your BJJ question: ")
    search_vector(q)
