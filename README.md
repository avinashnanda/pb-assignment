# Visual Search System
An  visual search system that allows users to search image repositories using natural language queries. 

## 🚀 Features
- Store and index images with embeddings.
- Perform semantic search with natural language queries.
- Generate AI-driven explanations for retrieved images.
- REST API built with FastAPI.
- Persistent vector database using ChromaDB.
- Containerized deployment with Docker.

## 🛠️ Setup & Installation


Create a virtual environment and activate it:

```
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

```

Install dependencies. First install PyTorch (CUDA 12.8 example; use CPU build if needed):

```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
Then install the rest:
pip install -r requirements.txt
```

## Batch Add Images to ChromaDB
To add images from a directory to ChromaDB, run:

```
python -m src.ingest_images
```

## Running the App
Run with Uvicorn:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000

```
run the search app:

```
Python search_app.py
```

Once running, the app is available at http://localhost:8000 and API docs are at http://localhost:8000/docs


## Running Tests

Run the test suite with:
```
pytest -q
```


## 🐳 Docker Deployment

Build the Docker image:

```
docker build -t pb-assignment:latest .
```

Run the container with a persistent ChromaDB volume:
```
docker run -p 8000:8000 -v /local/path/to/chroma_db:/app/chroma_db pb-assignment:latest

```

The API will be accessible at http://localhost:8000/docs


## ✅ Example Workflow
1. Add images → embeddings stored in ChromaDB.
2. Search with natural language query.
3. Retrieve top-k similar images + AI-driven explanations.


## Important Notes
- Ensure GPU drivers and CUDA version match the installed PyTorch build.
- By default, ChromaDB persists in ./chroma_db/. Tests use a temporary database.
- For production, always mount a persistent volume as shown in the Docker section.
- Due to lack of openai keys i am using a lmstudio model for generating explanations. Need to change when openai key is available.
