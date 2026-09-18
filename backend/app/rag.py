import json
import os
import re

import numpy as np
from mistralai.client import Mistral

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_PATH = os.path.join(BASE_DIR, "data", "knowledge.json")
EMBEDDING_PATH = os.path.join(
    BASE_DIR,
    "data",
    "knowledge_embeddings.json"
)


class KnowledgeRetriever:

    def __init__(self):
        with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

        api_key = os.getenv("MISTRAL_API_KEY")

        if not api_key:
            raise RuntimeError(
                "MISTRAL_API_KEY is not configured."
            )

        self.client = Mistral(api_key=api_key)
        self.embedding_model = "mistral-embed"

        if os.path.exists(EMBEDDING_PATH):
            with open(EMBEDDING_PATH, "r", encoding="utf-8") as f:
                self.embeddings = np.asarray(
                    json.load(f),
                    dtype="float32"
                )
        else:
            self.embeddings = None

    def _embed(self, texts):
        response = self.client.embeddings.create(
            model=self.embedding_model,
            inputs=texts
        )

        return np.asarray(
            [item.embedding for item in response.data],
            dtype="float32"
        )

    def _keyword_search(self, query, k=3):
        query_words = set(
            re.findall(
                r"[a-zA-Z]+",
                query.lower()
            )
        )

        scored = []

        for document in self.documents:

            searchable_text = " ".join([
                document.get("topic", ""),
                document.get("condition", ""),
                " ".join(document.get("variables", [])),
                document.get("recommendation", ""),
                document.get("reasoning", "")
            ]).lower()

            document_words = set(
                re.findall(
                    r"[a-zA-Z]+",
                    searchable_text
                )
            )

            score = len(
                query_words.intersection(document_words)
            )

            scored.append((score, document))

        scored.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            document
            for _, document in scored[:k]
        ]

    def search(self, query, k=3):

        # Prefer semantic Mistral retrieval.
        if self.embeddings is not None:
            try:
                query_embedding = self._embed([query])[0]

                document_norms = np.linalg.norm(
                    self.embeddings,
                    axis=1,
                    keepdims=True
                )

                query_norm = np.linalg.norm(
                    query_embedding
                )

                normalized_documents = (
                    self.embeddings /
                    np.maximum(
                        document_norms,
                        1e-12
                    )
                )

                normalized_query = (
                    query_embedding /
                    max(query_norm, 1e-12)
                )

                similarities = (
                    normalized_documents @
                    normalized_query
                )

                top_indices = np.argsort(
                    similarities
                )[::-1][:k]

                return [
                    self.documents[index]
                    for index in top_indices
                ]

            except Exception as error:
                print(
                    "Mistral embeddings unavailable, "
                    f"using keyword retrieval: {error}"
                )

        # Local fallback — no API required.
        return self._keyword_search(query, k)