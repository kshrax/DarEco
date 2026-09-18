import json
import os

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_PATH = os.path.join(BASE_DIR, "data", "knowledge.json")


class KnowledgeRetriever:
    def __init__(self):
        with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        texts = [
            f"{doc['topic']} {doc['condition']} "
            f"{' '.join(doc['variables'])} "
            f"{doc['recommendation']} "
            f"{doc['reasoning']}"
            for doc in self.documents
        ]

        embeddings = self.model.encode(texts)

        embeddings = np.array(embeddings).astype("float32")

        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def search(self, query, k=3):
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, k)

        results = []

        for index in indices[0]:
            if index < len(self.documents):
                results.append(self.documents[index])

        return results