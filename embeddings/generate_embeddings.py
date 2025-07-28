from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

client = MongoClient("mongodb://localhost:27017/")
db = client["bjj_chatbot"]
collection = db["segments"]

model = SentenceTransformer("all-MiniLM-L6-v2")

for seg in collection.find({"embedding": {"$exists": False}}):
    embedding = model.encode(seg["text"]).tolist()
    collection.update_one({"_id": seg["_id"]}, {"$set": {"embedding": embedding}})

print("All embeddings generated!")

print(collection.find_one({"embedding": {"$exists": True}}))