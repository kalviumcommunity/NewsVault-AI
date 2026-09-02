from services.ai_service import embed_query

question = "What was India's economic growth in 2025?"

embedding = embed_query(question)

print("Query embedding generated successfully!")
print("Embedding dimension:", len(embedding))
print("First 5 values:", embedding[:5])