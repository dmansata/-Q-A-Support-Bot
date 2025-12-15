def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
    
    return chunks

def process_page(page_data):
    # page_data: {url, title, raw_html} from crawler
    # Combined with extraction logic
    from extractor.cleaner import extract_content
    
    cleaned_text = extract_content(page_data['html'])
    text_chunks = chunk_text(cleaned_text)
    
    processed_chunks = []
    for i, chunk in enumerate(text_chunks):
        processed_chunks.append({
            "id": f"{page_data['url']}_{i}",
            "url": page_data['url'],
            "title": page_data['title'],
            "text": chunk
        })
    
    return processed_chunks
