import requests
import os
import json
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity

EMBED_MODEL = "bge-m3"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
REQUEST_TIMEOUT = 120


def create_embedding(text_list):
    r = requests.post(
        OLLAMA_EMBED_URL,
        json={"model": EMBED_MODEL, "input": text_list},
        timeout=REQUEST_TIMEOUT,
    )
    r.raise_for_status()

    embeddings = r.json().get("embeddings")
    if not embeddings:
        raise ValueError("No embeddings were returned by the embedding model.")
    return embeddings

jsons = sorted(os.listdir("new_json"))
my_dict = []
chunk_id = 0

for json_file in jsons:

    with open(f"new_json/{json_file}", "r", encoding="utf-8") as f:
        content = json.load(f)
    print(f"Creating embedding for {json_file}...")

    chunks = content.get("chunks", [])
    if not chunks:
        print(f"Skipping {json_file} because it has no chunks.")
        continue

    embeddings = create_embedding(
        [c["text"] for c in chunks]
    )

    for i, chunk in enumerate(chunks):
        print(chunk)

        chunk["chunk_id"] = chunk_id
        chunk["embedding"] = embeddings[i]

        chunk_id += 1
        my_dict.append(chunk)

df = pd.DataFrame.from_records(my_dict)
#Save this dataframe
joblib.dump(df, "embeddings.joblib")

# ONLY THIS LINE CHANGED
# print(df.head())
