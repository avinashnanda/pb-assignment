from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.vector_store import ImageVectorPipeline
from src.semantic_search import SemanticSearcher
from src.explain_images import ExplanationGenerator
from langchain_openai import ChatOpenAI

# ----------- FastAPI Setup -----------
app = FastAPI(
    title="Visual Search API",
    description="Enterprise-grade visual semantic search with explanations",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend url production. disabled for dev
    allow_credentials=True, # will be required for later authentication
    allow_methods=["*"], # need to restrict few methods for prod.
    allow_headers=["*"], # will be required for later authentication . need to restrict later.
)

# ----------- Init Models & Pipelines -----------
llm = ChatOpenAI(
    model="local-model",
    base_url="http://host.docker.internal:1234/v1",
    api_key="not-needed"
)


pipeline = ImageVectorPipeline(persist_dir="chroma_db")
searcher = SemanticSearcher(pipeline.get_vectorstore())
explainer = ExplanationGenerator(llm_model=llm)

# pydantic for stuctured and valid inputs and outputs
class SearchRequest(BaseModel):
    query: str
    k: int = 5

class SearchResult(BaseModel):
    image_url: str
    image_base64: str
    explanation: str
    score: float
    

# ----------- API Routes -----------
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/search", response_model=list[SearchResult])
def search_images(request: SearchRequest):
    results = searcher.search(request.query, k=request.k)

    response = []
    for r in results:
        try:
            explanation = explainer.explain(request.query, r["content"])
        except Exception as e:
            explanation = f"Could not generate explanation: {str(e)}"

        response.append({
            "image_url": r["metadata"].get("filename", "N/A"),
            "image_base64": r["content"],
            "explanation": str(explanation),
            "score": float(r["score"])
        })

    return response