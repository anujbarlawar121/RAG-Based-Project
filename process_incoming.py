import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import requests

EMBED_MODEL = "bge-m3"
GENERATION_MODEL = "llama3.2:3b"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
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


def inference(prompt):
    r = requests.post(
        OLLAMA_GENERATE_URL,
        json={
            "model": GENERATION_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=REQUEST_TIMEOUT,
    )
    r.raise_for_status()

    response = r.json()
    return response


df = joblib.load('embeddings.joblib')

incoming_query = input("Ask a question: ").strip()

if not incoming_query:
    raise ValueError("Question cannot be empty.")

question_embedding = create_embedding([incoming_query])[0]
# print(question_embedding)

# Find Similarities of Question_embedding with other embeddings
# print(np.vstack(df['embedding'].values))
# print(np.vstack(df['embedding'].shape))

similarities = cosine_similarity(np.vstack(df['embedding']),[question_embedding]).flatten()
# print(similarities)

top_results = 4
max_indx = similarities.argsort()[::-1][0:top_results]
# print(max_indx)

new_df = df.iloc[max_indx].sort_values(["number", "start"])
# print(new_df[["number", "title", "text"]])

context_json = new_df[["number", "title", "text", "start", "end"]].to_json(
    orient="records",
    indent=2,
)

prompt = f'''
You are an AI assistant for a Java DSA course.

Here are the video subtitle chunks with video number, title, timestamps, and subtitles:

{context_json}

User Question:
"{incoming_query}"

Instructions:
- Answer only from the provided video chunks.
- Tell which video and timestamp contains the answer.
- Briefly explain what is taught there.
- If multiple videos are relevant, mention all.
- If the question is unrelated, say:
    "I can only answer questions related to this Java DSA course."
- Do not make up information.

Output Format:

Video: <video number> - <title>
Timestamp: <start> to <end>
Content: <short explanation>
'''

with open("prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

response = inference(prompt)
answer = response.get("response", "").strip()

if not answer:
    raise ValueError("The model returned an empty response.")

print(answer)

with open("response.txt", "w", encoding="utf-8") as f:
    f.write(answer)

with open("output.json", "w", encoding="utf-8") as f:
    f.write(pd.Series(response).to_json(indent=4))

# for index, item in new_df.iterrows():
#     print(index,item["number"], item["title"], item["text"], item["chunk_id"], item["start"], item["end"])

# a = create_embedding("hello world")
# print(a)
