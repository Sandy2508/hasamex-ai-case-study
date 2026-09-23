from app.parser import parse_transcript


files = [
    "data/transcripts/Transcript_1_France.txt",
    "data/transcripts/Transcript_2_Germany.txt",
    "data/transcripts/Transcript_3_UK.txt",
]


for file in files:
    print("\n" + "=" * 70)
    print(f"FILE: {file}")
    print("=" * 70)

    segments = parse_transcript(file)

    print(f"Total segments: {len(segments)}")

    for segment in segments:
        print(
            f"[{segment['timestamp']}] "
            f"{segment['speaker_type'].upper()} - "
            f"{segment['speaker']}: "
            f"{segment['text']}"
        )