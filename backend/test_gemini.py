from services.ai_service import generate_response

question = "What was India's economic growth in 2025?"

answer = generate_response(question)

print("Gemini answer:")
print(answer)