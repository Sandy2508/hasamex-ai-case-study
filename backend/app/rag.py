
from app.embeddings import create_embedding
from app.vector_store import collection
from app.llm import generate_answer


EXPERTS = [
    "Dr. Jean Martin",
    "Anna Keller",
    "Dr. Emily Carter",
]


def ask_question(
    question: str,
    n_results: int = 5,
    expert: str | None = None
) -> dict:

    query_embedding = create_embedding(question)

    if expert:
        filters = {
            "$and": [
                {"speaker_type": "expert"},
                {"expert": expert}
            ]
        }
    else:
        filters = {
            "speaker_type": "expert"
        }

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=filters
    )

    evidence = []

    if results["documents"] and results["documents"][0]:
        for i, text in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i]

            evidence.append({
                "expert": metadata["expert"],
                "role": metadata["role"],
                "market": metadata["market"],
                "timestamp": metadata["timestamp"],
                "text": text
            })

    answer = generate_answer(question, evidence)

    return {
        "question": question,
        "answer": answer,
        "evidence": evidence
    }


def compare_interviews() -> dict:
    comparison_question = (
        "Identify the common themes and differences across the three "
        "expert interviews about the European robotic surgery market. "
        "Organize the response into common themes and differences. "
        "Use only the supplied evidence. Do not claim that a point is "
        "shared by all experts unless the evidence supports it."
    )

    query_embedding = create_embedding(comparison_question)
    evidence = []

    # Retrieve evidence separately for each expert.
    # Do not generate an individual answer for each expert.
    for expert in EXPERTS:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5,
            where={
                "$and": [
                    {"speaker_type": "expert"},
                    {"expert": expert}
                ]
            }
        )

        if results["documents"] and results["documents"][0]:
            for i, text in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i]

                evidence.append({
                    "expert": metadata["expert"],
                    "role": metadata["role"],
                    "market": metadata["market"],
                    "timestamp": metadata["timestamp"],
                    "text": text
                })

    # Generate the cross-interview analysis once, using the collected evidence.
    answer = generate_answer(comparison_question, evidence)

    return {
        "answer": answer,
        "evidence": evidence
    }