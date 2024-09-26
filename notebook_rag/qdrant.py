from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct

def create_qdrant_client():
    return QdrantClient(url="http://localhost:6333")

def create_collection(client, collection_name):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.DOT)
        )

def insert_qdrant_point(client, collection_name, chunk):
    print(f'Inserting Chunk {chunk["element_id"]}', end="")
    status = client.upsert(
        collection_name=collection_name,
        wait=True,
        points=[
            PointStruct(
                id=chunk["element_id"],
                vector=chunk["embedding"],
                payload={
                    "text": chunk["text"],
                    "filename": chunk["metadata"]["filename"], 
                }), 
        ]
    )

def query_qdrant_point(client, collection_name, embedding):
    hits = client.query_points(
        collection_name=collection_name,
        query=embeddings.embed_query(user_query),
    ).points

    retrieved_docs = [hit.payload for hit in hits]
    print(len(retrieved_docs))
    for doc in retrieved_docs:
        print(doc, end="\n---\n")