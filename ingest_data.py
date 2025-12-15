import os
import shutil
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import MarkdownHeaderTextSplitter

# --- CONFIGURATION ---
# 1. Where your markdown files are located
DATA_PATH = "data/destinations" 

# 2. Where the Vector Database will be saved
CHROMA_PATH = "chroma_db_store" 

# 3. The AI Model that turns text into numbers (Free, runs locally)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def ingest_data():
    print("🚀 Starting Data Ingestion...")

    # --- PART 1: LOAD & SPLIT DATA ---
    # We use a "Markdown Splitter" so the AI understands structure.
    # It will attach the Header name to the chunk of text.
    headers_to_split_on = [
        ("#", "Destination"),    # e.g. "Destination Profile: Nainital"
        ("##", "Category"),      # e.g. "Tourist Attractions"
        ("###", "SubTopic"),     # e.g. "Naini Lake"
    ]
    
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    
    all_chunks = []
    
    # Walk through your data folder
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: Directory '{DATA_PATH}' not found.")
        return

    print(f"📂 Scanning '{DATA_PATH}'...")
    
    files_found = 0
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".md"):
            files_found += 1
            file_path = os.path.join(DATA_PATH, filename)
            
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            # Intelligent Splitting
            chunks = markdown_splitter.split_text(text)

            # Tag every chunk with its source filename
            for chunk in chunks:
                chunk.metadata["source"] = filename
                all_chunks.append(chunk)
                
            print(f"   👉 Processed {filename}: {len(chunks)} chunks.")

    if files_found == 0:
        print("❌ No .md files found!")
        return

    # --- PART 2: CREATE DATABASE ---
    
    # Initialize the Embedding Model
    print(f"🧠 Loading AI Model ({EMBEDDING_MODEL_NAME})...")
    embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    # Clean start: Delete old DB if it exists to avoid duplicates
    if os.path.exists(CHROMA_PATH):
        print("🧹 Cleaning up old database...")
        shutil.rmtree(CHROMA_PATH)

    print("💾 Saving to Vector Database...")
    
    # Create the DB
    db = Chroma.from_documents(
        documents=all_chunks, 
        embedding=embedding_function, 
        persist_directory=CHROMA_PATH
    )

    print(f"✅ SUCCESS! Database created at: {CHROMA_PATH}")
    print(f"📊 Total Knowledge Chunks Stored: {len(all_chunks)}")

if __name__ == "__main__":
    ingest_data()
