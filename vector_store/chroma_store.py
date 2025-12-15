import chromadb
from embeddings.embedder import get_embedding_function

# Use a persistent client
# Assuming the script is run from the project root, this will go to ./chroma_db
client = chromadb.PersistentClient(path="./chroma_db")

embedding_function = get_embedding_function()

collection = client.get_or_create_collection(name="rag_docs", embedding_function=embedding_function)

def add_documents(chunks):
    ids = [chunk['id'] for chunk in chunks]
    documents = [chunk['text'] for chunk in chunks]
    metadatas = [{"url": chunk['url'], "title": chunk['title']} for chunk in chunks]

    if ids:
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

def query_similar(query_text, n_results=3):
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results
