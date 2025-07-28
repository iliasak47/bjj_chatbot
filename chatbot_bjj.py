import numpy as np
from embeddings.search_vector import search_most_similar
from mongo.search_mongo import find_entry_by_id
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from pyllamacpp.model import Model

# Charger le modèle d'embedding
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["bjj_database"]
collection = db["bjj_transcripts"]

# Charger le modèle LLaMA (local)
llm = Model(
    model_path="llama-3-8b.gguf",
    n_ctx=4096
)

# Fonction pour trouver les passages les plus proches
def search_similar(query, top_k=3):
    query_embedding = embedder.encode(query)
    docs = list(collection.find())
    
    similarities = []
    for doc in docs:
        sim = np.dot(query_embedding, doc["embedding"]) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(doc["embedding"])
        )
        similarities.append((sim, doc["text"]))

    similarities.sort(key=lambda x: x[0], reverse=True)
    return similarities[:top_k]

# Boucle principale du chatbot
while True:
    question = input("\nAsk your BJJ question: ")
    if question.lower() in ["quit", "exit"]:
        break

    # 🔹 Récupérer les meilleurs passages
    top_results = search_similar(question)

    # 🔹 Construire le contexte pour le LLM
    context = "\n".join([res[1] for res in top_results])

    prompt = f"""You are John Danaher, an expert BJJ instructor.
Use the following context to answer the user's question in a clear and concise way.

Context:
{context}

Question: {question}

Answer as John Danaher:
"""
    response = llm(prompt, max_tokens=300)
    print("\n John Danaher:", response["choices"][0]["text"])
