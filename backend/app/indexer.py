from pathlib import Path

from app.parser import parse_transcript
from app.embeddings import create_embedding
from app.vector_store import collection


TRANSCRIPTS_DIR = Path("data/transcripts")


def index_transcripts():
    transcript_files = sorted(TRANSCRIPTS_DIR.glob("*.txt"))

    for file_path in transcript_files:
        print(f"Processing: {file_path.name}")

        segments = parse_transcript(str(file_path))

        for index, segment in enumerate(segments):
            document_id = f"{file_path.stem}_{index}"

            embedding = create_embedding(segment["text"])

            collection.add(
                ids=[document_id],
                embeddings=[embedding],
                documents=[segment["text"]],
                metadatas=[{
                    "expert": segment["expert"],
                    "role": segment["role"],
                    "market": segment["market"],
                    "timestamp": segment["timestamp"],
                    "speaker": segment["speaker"],
                    "speaker_type": segment["speaker_type"]
                }]
            )

        print(f"  Added {len(segments)} segments")


if __name__ == "__main__":
    index_transcripts()