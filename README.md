# RAG-Based AI Teaching Assistant

A simple retrieval-augmented generation project that turns course videos into a question-answering assistant.

This project:
- extracts audio from video lectures
- transcribes the audio with Whisper
- merges subtitle chunks into larger retrieval units
- creates embeddings with Ollama
- retrieves the most relevant chunks for a user question
- generates an answer grounded in course content

## Project Flow

1. Put lecture videos inside the `Videos/` folder.
2. Convert videos to MP3 files.
3. Transcribe MP3 files into JSON subtitle chunks.
4. Merge subtitle chunks into larger context windows.
5. Generate embeddings and store them in `embeddings.joblib`.
6. Ask questions and generate grounded answers from the retrieved chunks.

## Tech Stack

- Python
- OpenAI Whisper
- Ollama
- `bge-m3` for embeddings
- `llama3.2:3b` for answer generation
- `pandas`, `numpy`, `scikit-learn`, `joblib`, `requests`

## Prerequisites

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

Install and verify `ffmpeg`:

```powershell
ffmpeg -version
```

Start Ollama and download the required models:

```powershell
ollama serve
ollama pull bge-m3
ollama pull llama3.2:3b
```

## How To Run

Run the following commands from the project folder:

```powershell
python video_to_mp3.py
python mp3_to_json.py
python merge_chunks.py
python preprocess_json.py
python process_incoming.py
```

When `process_incoming.py` runs, enter your question in the terminal.

## Files

- `video_to_mp3.py`: extracts audio from lecture videos
- `mp3_to_json.py`: transcribes audio and stores subtitle chunks as JSON
- `merge_chunks.py`: groups transcript chunks for better retrieval
- `preprocess_json.py`: creates embeddings and saves them in `embeddings.joblib`
- `process_incoming.py`: retrieves relevant chunks and generates the final answer

## Repository Notes

This repository intentionally ignores:
- raw videos
- generated audio files
- generated chunk files
- local embeddings
- prompt and response output files
- the local `whisper/` folder

That keeps the GitHub repository small, clean, and easy to run on another machine.

## Example Question

```text
What is 2D array?
```

## Future Improvements

- Add a FastAPI interface
- Add batch processing commands
- Improve retrieval ranking
- Add evaluation examples and sample screenshots
