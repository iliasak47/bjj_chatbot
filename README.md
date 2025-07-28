# 🥋 BJJ Chatbot

An intelligent chatbot that answers questions about Brazilian Jiu-Jitsu using instructional videos from the top coach, John Danaher

## Project structure

chatbot_bjj/
├── data/
│ ├── downloads/
│ └── transcriptions/
├── embeddings/
│ ├── generate_embeddings.py
│ └── search_vector.py
├── mongo/
│ └── insert_mongo.py
│ └── search_mongo.py
├── utils/
│ ├── create_blocks.py
│ └── transcribe_bilibili.py
├── chatbot_bjj.py
├── requirements.txt
├── .gitignore
└── README.md



## Installation

1. **Create a virtual environment (optional but recommended)**
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

2. **Install the dependencies**
pip install -r requirements.txt

3. **Start MongoDB**
Make sure MongoDB is running on localhost:27017.

## Fonctionnement
Download and transcribe a video using transcribe_bilibili.py

Insert the segments into MongoDB using insert_mongo.py

Generate embeddings using generate_embeddings.py

Create blocks of segments (optional but recommended)

Ask questions using:

search_mongo.py (text search, regex)

search_vector.py (semantic, vector search)

or chatbot_bjj.py (full chatbot)