# =========================================
# 🔹 SAFE IMPORT (RAG OPTIONAL)
# =========================================
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    RAG_AVAILABLE = True
except:
    RAG_AVAILABLE = False

import numpy as np
from core.llm import generate_answer
import json
import re

# =========================================
# 🔹 LOAD MODEL (ONLY IF AVAILABLE)
# =========================================
if RAG_AVAILABLE:
    model = SentenceTransformer('all-MiniLM-L6-v2')
else:
    model = None


# =========================================
# 🔹 SMART CHUNKING
# =========================================
def create_chunks(text, chunk_size=400, overlap=100):
    words = text.split()
    chunks = []

    start = 0
    chunk_id = 0

    while start < len(words):
        end = start + chunk_size
        chunk_text = " ".join(words[start:end])

        chunks.append({
            "id": chunk_id,
            "text": chunk_text
        })

        start += chunk_size - overlap
        chunk_id += 1

    return chunks


# =========================================
# 🔹 VECTOR STORE
# =========================================
def create_vector_store(chunks):

    if not RAG_AVAILABLE:
        return None, None

    texts = [c["text"] for c in chunks]

    embeddings = model.encode(texts, convert_to_numpy=True)

    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    return index, embeddings


# =========================================
# 🔥 CLEAN JSON
# =========================================
def extract_json(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r'\[.*?\]', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
    return []


# =========================================
# 🔥 LLM RE-RANK
# =========================================
def llm_rerank(query, results):

    if len(results) <= 3:
        return results

    chunks_text = "\n\n".join([
        f"[{i}] {r['text']}" for i, r in enumerate(results)
    ])

    prompt = f"""
You are an AI ranking system.

Select the BEST 3 chunks for answering the question.

Return ONLY a JSON list like:
[0, 2, 4]

Question:
{query}

Chunks:
{chunks_text}
"""

    response = generate_answer(prompt)

    indices = extract_json(response)

    valid_indices = []

    for idx in indices:
        if isinstance(idx, int) and idx < len(results):
            valid_indices.append(idx)

    if not valid_indices:
        return results[:3]

    return [results[i] for i in valid_indices]


# =========================================
# 🔥 SMART COMPRESSION
# =========================================
def smart_compress(text):
    sentences = text.split(".")
    if len(sentences) > 2:
        return ".".join(sentences[:2]).strip()
    return text[:200]


# =========================================
# 🔹 SEARCH
# =========================================
def search(query, chunks, index, embeddings, k=8):

    # 💀 fallback mode (no RAG)
    if not RAG_AVAILABLE or index is None:
        return [], 0

    query_embedding = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_embedding)

    distances, indices = index.search(query_embedding, k)

    results = []

    for i, idx in enumerate(indices[0]):
        score = float(distances[0][i])

        results.append({
            "text": chunks[idx]["text"],
            "score": score,
            "source": chunks[idx].get("source", ""),
            "page": chunks[idx].get("page", "")
        })

    # 🔹 threshold
    if results:
        max_score = max(r["score"] for r in results)
        threshold = max(max_score * 0.6, 0.3)
    else:
        threshold = 0

    filtered = [r for r in results if r["score"] >= threshold]

    if not filtered:
        filtered = results[:3]

    results = sorted(filtered, key=lambda x: x["score"], reverse=True)

    results = llm_rerank(query, results)

    for r in results:
        r["text"] = smart_compress(r["text"])

    return results, len(results)