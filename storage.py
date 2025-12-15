import chromadb
from chromadb.utils import embedding_functions

# Use a persistent client
client = chromadb.PersistentClient(path="./chroma_db")

# Use Sentence Transformers for embeddings
# This will download the model locally on first run
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = client.get_or_create_collection(name="rag_docs", embedding_function=sentence_transformer_ef)

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
