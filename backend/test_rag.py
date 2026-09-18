from app.rag import KnowledgeRetriever


retriever = KnowledgeRetriever()

results = retriever.search(
    "low rainfall, low soil organic carbon, monoculture wheat"
)

for result in results:
    print("\n---")
    print("Topic:", result["topic"])
    print("Recommendation:", result["recommendation"])
    print("Source:", result["source"])