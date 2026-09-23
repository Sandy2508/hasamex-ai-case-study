from app.embeddings import create_embedding
from app.vector_store import collection


query = "What are the main barriers to robotic surgery adoption?"

query_embedding = create_embedding(query)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
    where={"speaker_type": "expert"}
)

for i in range(len(results["documents"][0])):
    print("\n" + "=" * 60)
    print("TEXT:", results["documents"][0][i])
    print("METADATA:", results["metadatas"][0][i])
    print("DISTANCE:", results["distances"][0][i])