import asyncio
from typing import List, Dict, Any, Tuple, Optional
import os
import numpy as np
from tenacity import retry, stop_after_attempt, wait_exponential_jitter
import logging
import json

logger = logging.getLogger(__name__)

def _hash_to_vec(text: str, dim: int = 64) -> np.ndarray:
    # Deterministic pseudo-embedding for offline/dev/test
    import hashlib
    h = hashlib.sha256(text.encode()).digest()
    arr = np.frombuffer((h * (dim // len(h) + 1))[:dim], dtype=np.uint8).astype(np.float32)
    arr = (arr - 127.5) / 127.5
    norm = np.linalg.norm(arr) + 1e-8
    return arr / norm

async def embed_texts(texts: List[str], model: str, api_key: Optional[str]) -> np.ndarray:
    if not api_key:
        return np.stack([_hash_to_vec(t) for t in texts], axis=0)
    # Real OpenAI embeddings
    import openai
    client = openai.OpenAI(api_key=api_key)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential_jitter(initial=0.5, max=5))
    def _embed_sync(batch: List[str]) -> np.ndarray:
        resp = client.embeddings.create(model=model, input=batch)
        vecs = [np.array(d.embedding, dtype=np.float32) for d in resp.data]
        return np.stack(vecs, axis=0)

    # Batch with size ~256 tokens each, keep simple by 64 texts per batch
    outputs: List[np.ndarray] = []
    batch_size = 64
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        vecs = await asyncio.to_thread(_embed_sync, batch)
        outputs.append(vecs)
    return np.concatenate(outputs, axis=0)

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-8
    return float(np.dot(a, b) / denom)

class VectorIndex:
    """
    In-memory vector index for local/dev/testing. Stores vectors by chunk_id.
    """
    def __init__(self):
        self.vectors: Dict[str, np.ndarray] = {}

    def upsert(self, ids: List[str], vectors: np.ndarray) -> None:
        for i, cid in enumerate(ids):
            self.vectors[cid] = vectors[i]

    def query(self, query_vec: np.ndarray, top_k: int) -> List[Tuple[str, float]]:
        sims = [(cid, cosine_similarity(v, query_vec)) for cid, v in self.vectors.items()]
        sims.sort(key=lambda x: x[1], reverse=True)
        return sims[:top_k]

global_vector_index = VectorIndex()

async def upsert_embeddings(chunks: List[Dict[str, Any]], model: str, api_key: Optional[str]) -> None:
    texts = [c["text"] for c in chunks]
    ids = [c["id"] for c in chunks]
    vecs = await embed_texts(texts, model=model, api_key=api_key)
    global_vector_index.upsert(ids, vecs)