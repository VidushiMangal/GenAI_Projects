from groq import Groq
import os

knowledge_base = [
    {
        "title": "Python",
        "content": "Python is a programming language widely used for backend development."
    },
    {
        "title": "FastAPI",
        "content": "FastAPI is a modern Python web framework for building APIs quickly."
    },
    {
        "title": "JWT",
        "content": "JWT is used for authentication and authorization in web applications."
    },
    {
        "title": "Groq",
        "content": "Groq provides very fast inference for open-source large language models."
    }
]

def retrieve_context(query):
    query = query.lower()
    matched_chunks = []

    for doc in knowledge_base:
        if query in doc["title"].lower() or query in doc["content"].lower():
            print("I am in retrieve_conetxt method")
            matched_chunks.append(doc["content"])
    return matched_chunks

def ask_rag(question):
    context = retrieve_context(question)

    if not context:
        context_text = "No relevant information found."
    else:
        context_text = "\n".join(context)

    prompt = f"""
You are a helpful assistant.
Answer using the context.
If the answer is not present, say "I don't know".

Context:
{context_text}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="groq/compound-mini",  # free-tier friendly
        messages=[
            {"role": "system", "content": "You answer from provided context only."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


client = Groq(api_key=os.getenv("GROQ_API_KEY"))

while True:
    question = input("Ask a question (type exit to quit): ").strip()
    if question.lower() == "exit":
        break

    answer = ask_rag(question)
    print("\nANSWER:", answer)
    print("-" * 60)
