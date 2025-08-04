from pymongo import MongoClient
import re

client = MongoClient("mongodb://localhost:27017/")
db = client["bjj_chatbot"]
segments = db["segments_blocks"]

def has_volume(text):
    return re.search(r"Vol\.?\s*\d+", text, re.IGNORECASE)

instructionals = segments.distinct("instructional", {"chapter_title": {"$exists": False}})
no_volume_instr = [instr for instr in instructionals if not has_volume(instr)]

print("🧾 Instructionals sans 'Vol.X' détecté :")
for instr in no_volume_instr:
    print("-", instr)
