import chromadb
from sentence_transformers import SentenceTransformer

# Load persistent database
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection("hiring_kb")

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_context(query, n_results=3):

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    docs = results["documents"][0]

    context = "\n".join(docs)

    return context