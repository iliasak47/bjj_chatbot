# 🥋 BJJ Chatbot RAG – John Danaher Instructionals

This project is a **Retrieval-Augmented Generation (RAG) chatbot** specialized in **Brazilian Jiu-Jitsu**.  
It answers technical BJJ questions using context extracted from **John Danaher’s instructional videos**.

The chatbot uses:
- **MongoDB** to store and retrieve instructional transcripts
- **SentenceTransformers** for semantic search
- **OpenAI GPT** for generating answers
- **FastAPI** for the backend API
- **Streamlit** for the frontend interface

---

## 🚀 Features

- **Semantic search** in instructional transcripts using vector embeddings
- **Boosted relevance** with chapter titles
- **Metadata display** (instructional name, volume, chapter, timestamps)
- **FastAPI backend** to expose the chatbot as an API
- **Streamlit frontend** for a user-friendly interface

---

## 📂 Project Structure

```text 
CHATBOT_BJJ/
│
├── api/                       # Backend API (FastAPI)
│   └── main.py
│
├── bjj_chatbot/                # Core logic package
│   ├── __init__.py
│   └── core.py
│
├── data/                       # Raw and processed data
│   ├── downloads/
│   ├── timestamp/
│   └── transcriptions/
│
├── embeddings/                 # Scripts for embeddings
│   ├── generate_embeddings.py
│   └── search_vector.py
│
├── evaluation/                 # Evaluation datasets & results
│   └── rag_eval_manual.xlsx
│
├── interface/                  # Frontend (Streamlit)
│   └── frontend.py
│
├── mongo/                      # MongoDB data handling scripts
│   ├── add_sourcekey.py
│   ├── add_timestamp.py
│   ├── add_volume.py
│   ├── insert_mongo.py
│   ├── search_mongo.py
│   └── volume.py
│
├── utils/                      # Utility scripts
│   ├── create_blocks.py
│   ├── download_only.py
│   └── transcribe_bilibili.py
│
├── venv/                       # Virtual environment 
│
├── .env                        # Environment variables
├── .gitignore
├── README.md
├── requirements.txt
└── scrap_timestamp.py

```

---

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/bjj-chatbot.git
cd bjj-chatbot
```

2. **Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root folder:
```
OPENAI_API_KEY=your_openai_api_key
MONGO_URI=mongodb://localhost:27017/
```

---

## ▶️ Usage

### 1. Start the API
```bash
uvicorn api.main:app --reload
```
API will be available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Launch the Streamlit frontend
In another terminal:
```bash
streamlit run interface/frontend.py
```

---

## 📦 Tech Stack

- **Python 3.9+**
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [MongoDB](https://www.mongodb.com/)
- [SentenceTransformers](https://www.sbert.net/)
- [OpenAI API](https://platform.openai.com/)

---