from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

def init_qdrant():
    client = QdrantClient("localhost", port=6333)
    
    client.recreate_collection(
        collection_name="cybersecurity_docs",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    
    return client

def store_embedding(client, embedding, metadata, collection_name="cybersecurity_docs"):
    client.upsert(
        collection_name=collection_name,
        points=[
            {
                "id": metadata["id"],
                "vector": embedding,
                "payload": metadata
            }
        ]
    )

# Add the missing function
def get_text_from_embedding(client, embedding, collection_name="cybersecurity_docs"):
    search_result = client.search(
        collection_name=collection_name,
        query_vector=embedding,
        limit=1
    )
    if search_result:
        return search_result[0].payload.get("text", "")
    return ""