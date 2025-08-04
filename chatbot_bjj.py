import os
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

# Load OpenAI key from .env
load_dotenv()
client = OpenAI()

# MongoDB connection
mongo = MongoClient("mongodb://localhost:27017/")
db = mongo["bjj_chatbot"]
collection = db["segments_blocks"]

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def expand_segment_with_neighbors(seg, margin=1):
    """
    Étend un segment avec ses voisins (dans le même chapitre)
    """
    volume = seg.get("volume")
    chapter = seg.get("chapter_title")
    start_time = seg.get("start")

    if not (volume and chapter and start_time is not None):
        return [seg]  # Retourne au moins lui-même

    query = {
        "volume": volume,
        "chapter_title": chapter,
        "start": {"$gte": start_time - 60 * margin, "$lte": start_time + 60 * margin}
    }

    neighbors = list(collection.find(query).sort("start", 1))
    return neighbors


def search_similar_segments(query, top_k=5):
    query_emb = model.encode(query)
    results = []

    for seg in collection.find({"embedding": {"$exists": True}}):
        emb = np.array(seg["embedding"])
        sim = np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb))

        # Boost sémantique sur titre de chapitre
        chapter = seg.get("chapter_title", "").lower()
        query_words = set(query.lower().split())
        if any(word in chapter for word in query_words):
            sim += 0.15

        results.append((sim, seg))

    results = sorted(results, key=lambda x: x[0], reverse=True)[:top_k]

    # Expansion
    expanded = []
    seen_ids = set()
    for _, seg in results:
        for neighbor in expand_segment_with_neighbors(seg):
            if neighbor["_id"] not in seen_ids:
                expanded.append(neighbor)
                seen_ids.add(neighbor["_id"])

    # Trie final par ordre chronologique
    expanded.sort(key=lambda s: s.get("start", 0))
    return expanded


def format_context_with_metadata(segments):
    context = ""
    for i, seg in enumerate(segments, 1):
        context += f"\n--- Segment {i} ---\n"
        context += f"📖 Chapter: {seg.get('chapter_title', 'N/A')} | 📦 Volume: {seg.get('volume', 'N/A')}\n"
        context += f"⏱️ Time: {int(seg.get('start', 0))}s - {int(seg.get('end', 0))}s\n"
        context += f"{seg['text']}\n"
    return context


def ask_openai(question, context):
    messages = [
        {"role": "system", "content": "You are a Brazilian Jiu-Jitsu expert and instructor. Use the context excerpts below, which come from instructional videos by John Danaher, to provide a clear and detailed answer to the user's question. Be concise, practical, and make sure your response is grounded in the provided context. Only use the most relevant excerpts below to answer the question accurately. Ignore unrelated content."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    user_question = input("❓ Ask your BJJ question: ")

    print("\n🔍 Searching for relevant passages...")
    context_segments = search_similar_segments(user_question)
    context = format_context_with_metadata(context_segments)

    print("\n📚 Selected Context:\n")
    print(context)

    print("\n🧠 Expert Answer:\n")
    answer = ask_openai(user_question, context)
    print(answer)
