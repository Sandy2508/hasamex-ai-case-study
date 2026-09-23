
import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(question: str, evidence: list[dict]) -> str:
    if not evidence:
        return (
            "Insufficient evidence in the provided transcripts "
            "to answer this question."
        )

    evidence_text = ""

    for i, item in enumerate(evidence, start=1):
        evidence_text += (
            f"\nEvidence {i}:\n"
            f"Expert: {item['expert']}\n"
            f"Market: {item['market']}\n"
            f"Timestamp: {item['timestamp']}\n"
            f"Statement: {item['text']}\n"
        )

    prompt = f"""
You are an AI research assistant analyzing expert interviews
about the European robotic surgery market.

Answer the user's question using only the evidence supplied below.

Rules:
- Do not use outside knowledge.
- Do not invent facts or make unsupported assumptions.
- Do not invent or modify quotes, expert names, markets, or timestamps.
- Summarize the evidence clearly and neutrally.
- If the evidence does not sufficiently answer the question,
  explicitly say that the transcripts do not provide enough information.
- Do not create a separate quotes or citations section.
  The application will display the original evidence separately.
- Keep the answer concise and focused on the question.

User question:
{question}

Retrieved evidence:
{evidence_text}

Write a concise answer:
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text or (
            "Insufficient evidence in the provided transcripts "
            "to answer this question."
        )

    except Exception as error:
        print(f"Gemini generation error: {error}")

        return (
            "The AI analysis is temporarily unavailable. "
            "The retrieved transcript evidence is still available below. "
            "Please try again later."
        )