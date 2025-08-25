# Visual Search System
An  visual search system that allows users to search image repositories using natural language queries. 

# Project Stucture
```
pb-assignment
├─ .dockerignore               # Specifies files/folders to exclude from Docker image build
├─ app                         # FastAPI application folder
│  └─ main.py                  # Entry point for FastAPI app
├─ benchmarking_retriever.ipynb # Jupyter notebook for benchmarking retrieval performance
├─ dockerfile                  # Instructions to build Docker image
├─ docs                        # Documentation folder
│  ├─ Image-search-problem-statement.docx # Problem statement description
│  └─ System Architecture.docx            # High-level architecture design doc
├─ End_to_end_example.ipynb    # Jupyter notebook showing full workflow example
├─ README.md                   # Project description, setup instructions
├─ requirements.txt            # Python dependencies
├─ search_app.py               # Gradio seach application
├─ src                         # Core source code
│  ├─ explain_images.py        # Module to generate explanations/descriptions for images
│  ├─ ingest_images.py         # Module to ingest/preprocess images into vector DB
│  ├─ semantic_search.py       # Implements semantic search logic
│  ├─ vector_store.py          # Creates vector store using ChromaDB
├─ tests                       # Unit/integration tests
│  └─ test_searcher.py         # Tests cases
└─ utils                       # Utility/helper functions
   ├─ download_images.py       # Script for downloading images from external sources
   ├─ embedding_utils.py       # Utilities for creating/managing embeddings
   ├─ image_utils.py           # General image processing helpers
```

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
