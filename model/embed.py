import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ---------------- CONFIG ----------------
CASE_FOLDER = "../cases"   # Folder with 1.json, 2.json, ...
INDEX_FILE = "cases_local.index"
META_FILE = "metadata_local.json"
MODEL_NAME = "all-MiniLM-L6-v2"  # Small, fast, free model

# ---------------- LOAD CASES ----------------
case_texts = []
metadata = []

for filename in os.listdir(CASE_FOLDER):
    if filename.endswith(".json"):
        path = os.path.join(CASE_FOLDER, filename)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            text = f"{data.get('case_number','')} | {data.get('facts',{})} | {data.get('legal_issues',[])} | {data.get('judgment_summary',{})}"
            case_texts.append(text)
            metadata.append({
                "file": filename,
                "case_number": data.get("case_number", ""),
                "judgment_summary": data.get("judgment_summary", "")
            })

# ---------------- CREATE EMBEDDINGS ----------------
model = SentenceTransformer(MODEL_NAME)
embeddings = model.encode(case_texts, show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

# ---------------- BUILD FAISS INDEX ----------------
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

# ---------------- SAVE INDEX & METADATA ----------------
faiss.write_index(index, INDEX_FILE)
with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print(f"✅ Built embeddings for {len(case_texts)} cases.")