## 📂 Project Structure

```text
/Uktllm-langchain
  ├── /data
  │     └── /destinations       # Place your .md files here (Nainital, Almora, etc.)
  ├── /chroma_db_store          # The generated Vector Database (Do not edit manually)
  ├── ingest_data.py            # Script to read MD files and build the DB
  ├── query_db.py               # Script to search the DB (Test retrieval)
  ├── requirements.txt          # Python dependencies
  └── README.md                 # This file
````

-----

## ⚙️ Setup & Installation

### 1\. Prerequisites

  * **Python 3.10+** installed.
  * **pip** (Python package manager).

### 2\. Create a Virtual Environment (Recommended)

Always use a virtual environment to avoid conflicts with your system packages.

**For Linux/Mac:**

```bash
python -m venv venv
source venv/bin/activate
# If using Fish shell: source venv/bin/activate.fish
```

**For Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3\. Install Dependencies

Run the following command to install `langchain`, `chromadb`, and `sentence-transformers`:

```bash
pip install -r requirements.txt
```

*(If `requirements.txt` is missing, run: `pip install langchain langchain-huggingface langchain-chroma langchain-text-splitters chromadb sentence-transformers`)*

-----

## 🏗️ Creating the Vector Database

### 1\. Prepare Your Data

The database is built from Markdown files located in `data/destinations/`.

  * Example: `data/destinations/nainital_profile.md`

### 2\. Run the Ingestion Script

This script reads all `.md` files, chunks them intelligently by header, creates embeddings using `all-MiniLM-L6-v2`, and stores them in `chroma_db_store`.

```bash
python ingest_data.py
```

**Expected Output:**

> 🚀 Starting Data Ingestion...
> 👉 Processed nainital\_profile.md: 13 chunks.
> ...
> ✅ SUCCESS\! Database created at: chroma\_db\_store

-----

## 🔎 Testing & Retrieval

You can test if the database is working by asking a question. The retrieval script searches for the **top 3 most relevant chunks**.

### Usage

Run `query_db.py` followed by your question in quotes:

```bash
python query_db.py "Where can I get petrol in Mukteshwar?"
```

### Understanding the Output

The script returns a JSON object:

  * **content**: The actual text chunk retrieved.
  * **source**: The filename (e.g., `mukteshwar_profile.md`).
  * **relevance\_score**: The "distance" score. **Lower is better** (closer match).
      * *Score \< 1.0:* Strong match.
      * *Score \> 1.4:* Weak/Irrelevant match.

-----

## 🛠️ Troubleshooting

**Error: `ModuleNotFoundError`**

  * Make sure your virtual environment is active (`(venv)` should be in your prompt, or verify with `which python`).
  * Re-run `pip install -r requirements.txt`.

**Error: `Database not found`**

  * You must run `python ingest_data.py` **once** before you can query.

**Warning: `Relevance Score is > 1.0`**

  * This is normal for L2 distance metrics in Chroma. As long as the correct answer appears in the results, the RAG pipeline will work.

<!-- end list -->
