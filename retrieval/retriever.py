from vector_store.chroma_store import query_similar

def retrieve_context(query):
    results = query_similar(query)
    # results['documents'] is a list of lists (one list per query)
    # results['metadatas'] is the same
    
    context_list = []
    sources = []
    
    if results['documents']:
        for i, doc in enumerate(results['documents'][0]):
            meta = results['metadatas'][0][i]
            context_list.append(f"Source: {meta['title']} ({meta['url']})\nContent: {doc}")
            sources.append({"url": meta['url'], "title": meta['title']})
            
    return "\n\n".join(context_list), sources

def generate_answer_dummy(query, context):
    # In a real scenario, call OpenAI/Gemini API here
    prompt = f"""
    Answer the question based ONLY on the following context:
    
    {context}
    
    Question: {query}
    """
    
    # Placeholder response since we don't have an API key configured
    return f"Based on the context details from {len(context.split('Source:')) - 1} sources, here is what I found about '{query}'. (Note: This is a placeholder since no LLM is configured)."

def rag_pipeline(query):
    context, sources = retrieve_context(query)
    if not context:
        return "I couldn't find any relevant information in the crawled documents.", []
        
    answer = generate_answer_dummy(query, context)
    return answer, sources
