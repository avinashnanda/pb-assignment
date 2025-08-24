import os
from src.vector_store import ImageVectorPipeline


if __name__ == "__main__":
    image_dir = "./data/images"

    image_files = [
        os.path.join(image_dir, f)
        for f in os.listdir(image_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    pipeline = ImageVectorPipeline(persist_dir="chroma_db")
    pipeline.add_images(image_files, batch_size=4)

    print("✅ Images added to ChromaDB")
