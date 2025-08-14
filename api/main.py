from fastapi import FastAPI
from pydantic import BaseModel
from bjj_chatbot.core import search_similar_segments, format_context_with_metadata, ask_openai

app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(question: Question):
    segments = search_similar_segments(question.question)
    context = format_context_with_metadata(segments)
    answer = ask_openai(question.question, context)

    return {
        "answer": answer,
        "segments": [
            {
                "instructional": s.get("instructional"),
                "volume": s.get("volume"),
                "chapter": s.get("chapter_title"),
                "start": s.get("start"),
                "end": s.get("end"),
            }
            for s in segments
        ]
    }
