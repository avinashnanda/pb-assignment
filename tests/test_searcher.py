# tests/test_searcher.py
import sys, os,shutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from PIL import Image
from src.vector_store import ImageVectorPipeline
from src.symantic_search import SemanticSearcher

TEST_DB = "./test_db"

def setup_module(module):
    if os.path.exists(TEST_DB):
        shutil.rmtree(TEST_DB)

def create_dummy_image(path):
    img = Image.new("RGB", (50, 50), color="red")
    img.save(path)

def test_search_returns_results():
    os.makedirs("test_images", exist_ok=True)
    img_path = os.path.join("test_images", "img.jpg")
    create_dummy_image(img_path)

    pipeline = ImageVectorPipeline(persist_dir=TEST_DB)
    pipeline.add_images([img_path])

    searcher = SemanticSearcher(pipeline.get_vectorstore())
    results = searcher.search("a red square", k=1)

    assert isinstance(results, list)
    assert "score" in results[0]
    assert "metadata" in results[0]

    shutil.rmtree("test_images")
