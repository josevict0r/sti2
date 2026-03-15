from google import genai

client = genai.Client(api_key="AIzaSyCd5DcabNvTta4A3xCvk4XqMrBEb9S5l1U")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain what a stack data structure is."
)

print(response.text)