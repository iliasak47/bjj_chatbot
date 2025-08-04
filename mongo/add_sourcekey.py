from pymongo import MongoClient
import re

client = MongoClient("mongodb://localhost:27017/")
db = client["bjj_chatbot"]

collections = [
    ("segments_blocks", "instructional"),
    ("chapters_by_volume", "source")
]

def build_source_key(text):
    text = re.sub(r"by john.+$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"p0?\d+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"vol\.?\s*\d+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\.txt$", "", text, flags=re.IGNORECASE)
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")

for collection_name, field in collections:
    col = db[collection_name]
    updated = 0

    for doc in col.find({field: {"$exists": True}}):
        original = doc[field]
        source_key = build_source_key(original)
        col.update_one({"_id": doc["_id"]}, {"$set": {"source_key": source_key}})
        updated += 1

    print(f"✅ {updated} documents mis à jour dans '{collection_name}' avec 'source_key'")
