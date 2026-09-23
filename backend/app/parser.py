import re
from pathlib import Path


TIMESTAMP_PATTERN = re.compile(r"^\d{2}:\d{2}$")
EXPERT_PATTERN = re.compile(r"^Expert\s*\d*\s*[-–—]\s*(.+)$")


def parse_transcript(file_path: str) -> list[dict]:
    path = Path(file_path)

    lines = path.read_text(encoding="utf-8-sig").splitlines()

    expert = None
    role = None
    market = None

    # Read transcript-level metadata
    for line in lines[:5]:
        line = line.strip()

        expert_match = EXPERT_PATTERN.match(line)

        if expert_match:
            expert = expert_match.group(1).strip()

        elif line.startswith("Role:"):
            role = line.replace("Role:", "", 1).strip()

        elif line.startswith("Market:"):
            market = line.replace("Market:", "", 1).strip()

    segments = []

    # Read timestamp + speaker + text
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if TIMESTAMP_PATTERN.match(line):
            timestamp = line

            # Find the next non-empty line
            j = i + 1

            while j < len(lines) and not lines[j].strip():
                j += 1

            if j < len(lines):
                speaker_line = lines[j].strip()

                if ":" in speaker_line:
                    speaker, text = speaker_line.split(":", 1)

                    speaker = speaker.strip()
                    text = text.strip()

                    speaker_type = (
                        "interviewer"
                        if speaker.lower() == "interviewer"
                        else "expert"
                    )

                    segments.append({
                        "expert": expert,
                        "role": role,
                        "market": market,
                        "timestamp": timestamp,
                        "speaker": speaker,
                        "speaker_type": speaker_type,
                        "text": text
                    })

            i = j

        i += 1

    return segments