from services.ai_service import generate_response

response = generate_response(
    "Say hello to NewsVault AI in one short sentence."
)

print("Gemini response:")
print(response)