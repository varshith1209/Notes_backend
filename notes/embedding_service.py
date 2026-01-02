import numpy as np
import requests
from django.conf import settings

# ---------------------------
# LOCAL SENTENCE TRANSFORMERS (FREE)
# ---------------------------
from sentence_transformers import SentenceTransformer
_local_model = SentenceTransformer("all-MiniLM-L6-v2")

def local_embedding(text):
    return _local_model.encode(text).tolist()


# ---------------------------
# GEMINI (uses provider: Google DeepMind)
# ---------------------------
def gemini_embedding(text):
    url = "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedText"
    params = {"key": settings.GEMINI_API_KEY}
    r = requests.post(url, params=params, json={"text": text})
    return r.json()["embedding"]["value"]


# ---------------------------
# OPENAI (optional)
# ---------------------------
def openai_embedding(text):
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return res.data[0].embedding


# ---------------------------
# SELECTOR
# ---------------------------
def get_embedding(text):
    provider = getattr(settings, "EMBEDDING_PROVIDER", "local")

    if provider == "gemini":
        return gemini_embedding(text)
    elif provider == "openai":
        return openai_embedding(text)
    return local_embedding(text)  # default


# ---------------------------
# COSINE SIMILARITY
# ---------------------------
def cosine(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
