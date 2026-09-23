from app.rag import ask_question


result = ask_question(
    "What are the main barriers to robotic surgery adoption?"
)

print("\nANSWER:")
print(result["answer"])

print("\nSUPPORTING EVIDENCE:")

for item in result["evidence"]:
    print("-" * 50)
    print("Expert:", item["expert"])
    print("Market:", item["market"])
    print("Timestamp:", item["timestamp"])
    print("Quote:", item["text"])