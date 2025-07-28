from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["bjj_chatbot"]
collection = db["segments"]

# Chargement du modèle d'embeddings 
model = SentenceTransformer("all-MiniLM-L6-v2")

def search_vector(query, top_k=5):
    """
    Recherche vectorielle approximative dans la base MongoDB
    query : la question posée par l'utilisateur (texte)
    top_k : nombre de résultats à afficher
    """

    # 1) Transformer la question en vecteur d'embedding
    query_emb = model.encode(query)

    results = []

    # 2) Parcourir tous les segments qui ont déjà un embedding
    for seg in collection.find({"embedding": {"$exists": True}}):

        # Convertir l'embedding stocké (list) en tableau NumPy pour le calcul
        emb = np.array(seg["embedding"])

        # 3) Calculer la similarité cosinus entre la question et le segment
        sim = np.dot(query_emb, emb) / (
            np.linalg.norm(query_emb) * np.linalg.norm(emb)
        )

        # On garde la similarité + le segment pour trier après
        results.append((sim, seg))

    # 4) Trier par similarité décroissante et prendre les top_k meilleurs
    results = sorted(results, key=lambda x: x[0], reverse=True)[:top_k]

    # 5) Afficher les résultats formatés
    for sim, r in results:
        minutes = round(r["start"] / 60, 2)
        print(f"\n Similarity: {round(sim, 2)}")
        print(f" Answer: {r['text']}")
        print(f" Instructional: {r['instructional']}")
        print(f" Timestamp: {minutes} min")

if __name__ == "__main__":
    # Demande à l'utilisateur sa question
    q = input("Ask your BJJ question: ")
    search_vector(q)
