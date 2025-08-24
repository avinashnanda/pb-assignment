import os, hashlib, torch
from utils.embedding_utils import STClipEmbeddings
from langchain_chroma import Chroma
from tqdm.auto import tqdm


# ------------------ Helper: Compute SHA256 Hash ------------------
def file_hash(path, chunk_size=8192):
    """Compute SHA256 hash of a file (content-based ID)."""
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            sha.update(chunk)
    return sha.hexdigest()


# ------------------ Chroma Image Pipeline ------------------
class ImageVectorPipeline:
    def __init__(self, persist_dir="chroma_db", collection="image_embeddings", model_name="sentence-transformers/clip-ViT-B-32"):
        self.persist_dir = persist_dir
        self.collection_name = collection
        self.embedding_model = STClipEmbeddings(model_name=model_name)

        os.makedirs(persist_dir, exist_ok=True)
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_dir,
            embedding_function=self.embedding_model
        )

    def add_images(self, image_paths, metadatas=None, batch_size=8):
        """Add images into Chroma with progress bar & batch insert (dedup via content hash)."""
        if not image_paths:
            print("⚠️ No images provided.")
            return []

        # Generate IDs based on SHA256 hash of image content
        ids = [file_hash(p) for p in image_paths]
        metadatas = metadatas or [{"filename": f} for f in image_paths]

        # ✅ Avoid duplicate inserts by checking existing IDs
        existing = set(self.vectorstore.get(limit=999999)["ids"])
        new_uris, new_ids, new_metas = [], [], []
        for uri, _id, meta in zip(image_paths, ids, metadatas):
            if _id not in existing:
                new_uris.append(uri)
                new_ids.append(_id)
                new_metas.append(meta)

        if not new_uris:
            print("ℹ️ All images already exist in DB.")
            return []

        inserted_ids = []
        # ✅ Batch process with progress bar
        for i in tqdm(range(0, len(new_uris), batch_size), desc="🔄 Adding images"):
            batch_uris = new_uris[i:i+batch_size]
            batch_ids = new_ids[i:i+batch_size]
            batch_metas = new_metas[i:i+batch_size]

            batch_inserted = self.vectorstore.add_images(
                uris=batch_uris, metadatas=batch_metas, ids=batch_ids
            )
            inserted_ids.extend(batch_inserted)

        print(f"✅ Added {len(inserted_ids)} new images.")
        return inserted_ids
    
    def get_vectorstore(self):
        return self.vectorstore

