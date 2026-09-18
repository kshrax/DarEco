import json
import os

import numpy as np
from mistralai.client import Mistral

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_PATH = os.path.join(BASE_DIR, "data", "knowledge.json")


class KnowledgeRetriever:
    def __init__(self):
        with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

        api_key = os.getenv("MISTRAL_API_KEY")

        if not api_key:
            raise RuntimeError("MISTRAL_API_KEY is not configured.")

        self.client = Mistral(api_key=api_key)
        self.embedding_model = "mistral-embed"

        # Load precomputed embeddings if available.
        self.embedding_path = os.path.join(
            BASE_DIR, "data", "knowledge_embeddings.json"
        )

        if os.path.exists(self.embedding_path):
            with open(self.embedding_path, "r", encoding="utf-8") as f:
                self.embeddings = np.asarray(
                    json.load(f), dtype="float32"
                )
        else:
            # Generate embeddings only once.
            texts = [
                f"{doc['topic']} {doc['condition']} "
                f"{' '.join(doc['variables'])} "
                f"{doc['recommendation']} "
                f"{doc['reasoning']}"
                for doc in self.documents
            ]

            self.embeddings = self._embed(texts)

            with open(self.embedding_path, "w", encoding="utf-8") as f:
                json.dump(self.embeddings.tolist(), f)

    def _embed(self, texts):
        response = self.client.embeddings.create(
            model=self.embedding_model,
            inputs=texts
        )

        embeddings = [
            item.embedding for item in response.data
        ]

        return np.asarray(embeddings, dtype="float32")

    def search(self, query, k=3):
        # Only the user's query needs a new embedding.
        query_embedding = self._embed([query])[0]

        document_norms = np.linalg.norm(
            self.embeddings,
            axis=1,
            keepdims=True
        )

        query_norm = np.linalg.norm(query_embedding)

        normalized_documents = (
            self.embeddings /
            np.maximum(document_norms, 1e-12)
        )

        normalized_query = (
            query_embedding /
            max(query_norm, 1e-12)
        )

        similarities = normalized_documents @ normalized_query

        top_indices = np.argsort(similarities)[::-1][:k]

        return [
            self.documents[index]
            for index in top_indices
        ]