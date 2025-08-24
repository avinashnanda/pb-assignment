class SemanticSearcher:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

    def search(self, query, k=5):
        """Return top-k relevant images with score + metadata."""
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        return [
            {"id": res.id, "score": score, "metadata": res.metadata,"content":res.page_content}
            for res, score in results
        ]

