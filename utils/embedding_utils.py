from sentence_transformers import SentenceTransformer
import torch
from PIL import Image


# ---- Custom embedding wrapper (no HuggingFaceEmbeddings) ----
class STClipEmbeddings:
    def __init__(self, model_name="sentence-transformers/clip-ViT-B-32", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SentenceTransformer(model_name, device=self.device)

    def embed_documents(self, texts):
        return self.model.encode(texts, convert_to_numpy=True)

    def embed_query(self, text):
        return self.model.encode([text], convert_to_numpy=True)[0]
    
    def embed_image(self, uris):
        imgs = [Image.open(path).convert("RGB") for path in uris]
        embeddings = self.model.encode(imgs, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings.tolist()   

