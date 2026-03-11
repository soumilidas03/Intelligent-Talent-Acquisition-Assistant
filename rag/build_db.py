import chromadb
from sentence_transformers import SentenceTransformer

# Persistent database client
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection("hiring_kb")

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load knowledge base
with open("rag/knowledge_base.txt", "r", encoding="utf-8") as f:
    documents = f.read().split("\n\n")

embeddings = model.encode(documents).tolist()

# Clear existing data (optional but good for rebuilds)
try:
    client.delete_collection("hiring_kb")
except:
    pass

collection = client.get_or_create_collection("hiring_kb")

for i, doc in enumerate(documents):
    collection.add(
        documents=[doc],
        embeddings=[embeddings[i]],
        ids=[str(i)]
    )

print("✅ ChromaDB vector database created successfully")