from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["bjj_chatbot"]
segments_col = db["segments_blocks"]
chapters_col = db["chapters_by_volume"]

updated = 0
skipped = 0
debug_samples = []

# Tous les segments sans titre de chapitre (ou vide/null)
query = {
    "$or": [
        {"chapter_title": {"$exists": False}},
        {"chapter_title": None},
        {"chapter_title": ""}
    ],
    "volume": {"$exists": True},
    "source_key": {"$exists": True}
}

for segment in segments_col.find(query):
    vol = segment["volume"]
    start = segment.get("start")
    key = segment.get("source_key")

    if start is None or not key:
        skipped += 1
        continue

    chapter_doc = chapters_col.find_one({"volume": vol, "source_key": key})
    if not chapter_doc:
        skipped += 1
        continue

    matched = None
    for ch in chapter_doc["chapters"]:
        if ch["start"] <= start < ch["end"]:
            matched = ch
            break

    if matched:
        segments_col.update_one(
            {"_id": segment["_id"]},
            {"$set": {
                "chapter_title": matched["title"],
                "chapter_start": matched["start"],
                "chapter_end": matched["end"]
            }}
        )
        updated += 1
    else:
        skipped += 1
        # On peut conserver un exemple pour debug
        if len(debug_samples) < 5:
            debug_samples.append({
                "volume": vol,
                "source_key": key,
                "start": start,
                "chapters": chapter_doc["chapters"]
            })

print(f"\n✅ Segments enrichis : {updated}")
print(f"⚠️ Segments ignorés (pas de chapitre correspondant) : {skipped}")

if debug_samples:
    print("\n🧪 Exemples à vérifier manuellement :")
    for sample in debug_samples:
        print(f"  Volume: {sample['volume']}, Start: {sample['start']}, Source: {sample['source_key']}")
        for c in sample['chapters']:
            print(f"    - {c['title']} [{c['start']} → {c['end']}]")
        print("-" * 60)
