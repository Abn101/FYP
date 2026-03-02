# reterive.py
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import ollama  # just import the module
from dotenv import load_dotenv

load_dotenv()

# ---------------- CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(BASE_DIR, "cases_local.index")
META_FILE = os.path.join(BASE_DIR, "metadata_local.json")
MODEL_NAME = "all-MiniLM-L6-v2"  # embeddings
LLM_MODEL = os.getenv("LLM_MODEL", "gemma3:1b")
TOP_K = 1

# ---------------- LOAD INDEX AND METADATA ----------------
index = faiss.read_index(INDEX_FILE)
with open(META_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# ---------------- LOAD EMBEDDING MODEL ----------------
embed_model = SentenceTransformer(MODEL_NAME)

# ---------------- RETRIEVAL FUNCTION ----------------
def retrieve_cases(query, top_k=TOP_K):
    q_emb = embed_model.encode([query]).astype("float32")
    D, I = index.search(q_emb, top_k)
    results = []
    for idx in I[0]:
        case = metadata[idx]
        # Ensure judgment_summary is string
        if isinstance(case.get("judgment_summary",""), dict):
            case["judgment_summary"] = json.dumps(case["judgment_summary"])
        results.append(case)
    return results

# ---------------- PROMPT BUILDER ----------------
def build_prompt(query, cases):
    prompt = f"""
You are a professional legal research assistant. A lawyer asks: "{query}"

For each case provided below, create a **structured legal brief** in the following format. 
**Use only the information provided in the case JSON, including legal references, judgment, legal issues, etc.** 
Do NOT add any new cases or citations from outside sources. Do NOT invent any information.

1. Case Reference:
   - Case Number:
   - Court:
   - Decision Date:

2. Decision Summary:
   - What the court decided
   - Key reasons for the decision

3. Relevance to Current Case:
   - Why this case supports or relates to the lawyer's query

4. How to Use in Argument:
   - Suggested strategy for referencing this case in defense or prosecution

5. Key Legal Issues Addressed:
   - Highlight main issues addressed in the case
   - Include only citations provided in the case JSON

6. Suggested Strategy for Reference in Argument:
   - Focus on how this case can be applied to strengthen the lawyer’s argument

Cases to analyze:
"""
    for case in cases:
        case_json_string = json.dumps(case, indent=2, ensure_ascii=False)

        prompt += f"""
--- CASE JSON START ---
{case_json_string}
--- CASE JSON END ---
"""

    prompt += """
**Instructions to AI:** 
- Do not add any information not present in the case JSON.
- Only use legal references provided in the JSON for citations.
- Present the output in numbered sections as requested.
- Ensure clarity and lawyer-friendly structure.
"""
    return prompt