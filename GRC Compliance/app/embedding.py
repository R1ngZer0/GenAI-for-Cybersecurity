import ollama

def embed_document(text):
    response = ollama.embed(model='nomic-embed-text', prompt=text)
    return response['embedding']