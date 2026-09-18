import os
import json

from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise RuntimeError("MISTRAL_API_KEY is not configured.")

client = Mistral(api_key=api_key)

with open("data/knowledge.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

texts = []

for doc in documents:
    text = (
        f"{doc['topic']} "
        f"{doc['condition']} "
        f"{' '.join(doc['variables'])} "
        f"{doc['recommendation']} "
        f"{doc['reasoning']}"
    )
    texts.append(text)

print(f"Creating embeddings for {len(texts)} knowledge documents...")

response = client.embeddings.create(
    model="mistral-embed",
    inputs=texts
)

embeddings = [
    item.embedding
    for item in response.data
]

with open(
    "data/knowledge_embeddings.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(embeddings, f)

print("Embeddings created successfully.")
print("Saved to: data/knowledge_embeddings.json")