from openai import OpenAI

client = OpenAI()

print("Hello world!!")

response = client.responses.create(
    model="gpt-5-mini",
    input="Summarize: Python is a programming language."
)

print(response.output_text)
