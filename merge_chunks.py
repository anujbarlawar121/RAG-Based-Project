import os
import math
import json

n = 5

for filename in sorted(os.listdir("jsons")):
    if filename.endswith(".json"):
        file_path = os.path.join("jsons", filename)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            chunks = data.get("chunks", [])
            if not chunks:
                print(f"Skipping {filename} because it has no chunks.")
                continue

            new_chunks = []
            num_chunks = len(chunks)
            num_groups = math.ceil(num_chunks / n)

            for i in range(num_groups):
                start_index = i * n
                end_index = min((i + 1) * n, num_chunks)

                chunk_group = chunks[start_index:end_index]

                new_chunks.append({
                        "number": chunks[0]["number"],
                        "title": chunk_group[0]["title"],
                        "start": chunk_group[0]["start"],
                        "end": chunk_group[-1]["end"],
                        "text": " ".join(chunk["text"] for chunk in chunk_group)
                })

            # Save file without double .json

            os.makedirs("new_json", exist_ok=True)
            with open(os.path.join("new_json", filename), "w", encoding="utf-8") as json_file:
                json.dump({"chunks": new_chunks, "text": data.get("text", "")}, json_file, indent=4)
