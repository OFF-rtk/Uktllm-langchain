import sys
import json
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# --- CONFIGURATION ---
CHROMA_PATH = "chroma_db_store"
# MUST use the same model as ingestion!
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def query_database(query_text):
    if not os.path.exists(CHROMA_PATH):
        return {"error": "Database not found. Run ingest_data.py first."}

    # 1. Initialize the Embedding Model
    embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    # 2. Connect to the DB
    db = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=embedding_function
    )

    # 3. Search for the Top 3 Matches
    # k=3 is usually enough context for an LLM
    results = db.similarity_search_with_score(query_text, k=3)

    # 4. Format the output
    retrieved_context = []
    for doc, score in results:
        retrieved_context.append({
            "source": doc.metadata.get("source", "Unknown"),
            "section": doc.metadata.get("Category", "General"), # Uses the ## Header
            "content": doc.page_content,
            "relevance_score": float(score) # Lower score = Better match
        })

    return {"results": retrieved_context}

if __name__ == "__main__":
    # Allow running from command line: python query_db.py "My question"
    if len(sys.argv) > 1:
        user_query = sys.argv[1]
    else:
        user_query = "Is there a petrol pump in Mukteshwar?" # Default test

    response = query_database(user_query)
    
    # Print pretty JSON
    print(json.dumps(response, indent=2))
