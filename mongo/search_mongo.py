from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["bjj_chatbot"]
collection = db["segments"]

print(collection.count_documents({}))

def search(query):
    results = collection.find({"text": {"$regex": query, "$options": "i"}}) #On filtre uniquement sur le champ text des documents
    for r in results:
        minutes = round(r["start"] / 60, 2)
        print(f"\n Answer: {r['text']}")
        print(f"Instructional: {r['instructional']}")
        print(f" Timestamp: {minutes} min")

if __name__ == "__main__":
    q = input("Ask your BJJ question: ")
    search(q)
