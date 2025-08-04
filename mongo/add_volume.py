from pymongo import MongoClient
import re

client = MongoClient("mongodb://localhost:27017/")
db = client["bjj_chatbot"]
segments = db["segments_blocks"]

def extract_volume_flexible(text):
    m1 = re.search(r"Vol\.?\s*(\d+)", text, re.IGNORECASE)
    if m1:
        return int(m1.group(1))
    m2 = re.search(r"p0?(\d+)", text, re.IGNORECASE)
    if m2:
        return int(m2.group(1))
    return None

updated = 0
skipped = 0

for seg in segments.find({"volume": {"$exists": False}}):
    instr = seg.get("instructional", "")
    vol = extract_volume_flexible(instr)

    if vol:
        segments.update_one({"_id": seg["_id"]}, {"$set": {"volume": vol}})
        updated += 1
    else:
        skipped += 1

print(f"✅ Segments mis à jour avec champ 'volume' : {updated}")
print(f"⚠️ Segments ignorés (volume non détecté) : {skipped}")
