import whisper
import json
import os

model = whisper.load_model("base")

os.makedirs("jsons", exist_ok=True)

audios = sorted(os.listdir("audios"))

for audio in audios:
    audio_path = os.path.join("audios", audio)
    if not os.path.isfile(audio_path):
        continue

    print(audio)

    if "_" in audio:

        number, raw_title = audio.split("_", 1)
        title = os.path.splitext(raw_title)[0]

        print(number, title)

        result = model.transcribe(
            audio=audio_path,
            language="hi",
            task="translate",
            word_timestamps=False
        )

        chunks = []

        for segment in result["segments"]:

            chunks.append({
                "number": number,
                "title": title,
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            })

        chunks_with_metadata = {
            "chunks": chunks,
            "text": result["text"]
        }

        with open(f"jsons/{audio}.json", "w", encoding="utf-8") as f:

            json.dump(chunks_with_metadata, f, indent=4)
