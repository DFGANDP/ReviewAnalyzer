from ollama import Client

client = Client()
prompt = """Your prompt here with {INSERT_ASPECT_HERE}""".replace("{INSERT_ASPECT_HERE}", "fun RPG gameplay")

response = client.chat(
    model="MHKetbi/Mistral-Small3.1-24B-Instruct-2503:q5_K_L",
    messages=[{"role": "user", "content": prompt}]
)

print(response["message"]["content"])
