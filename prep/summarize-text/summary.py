import os

from openai import OpenAI

client = OpenAI()

print("Hello world!!")
print("Current directory:", os.getcwd())
with open("./prep/summarize-text/input.txt", "r", encoding="utf-8") as file:
    text = file.read()

# response = client.responses.create(
#     model="gpt-5-mini",
#     input="Summarize: Python is a programming language."
# )

response = client.responses.create(
    model="gpt-5-mini",
    input=f"""
    You are a helpful summarization assistant.

    Summarize the following text:
    - Keep it concise
    - Use bullet points
    - Focus on key ideas

    TEXT:
    {text}
    """
)
print(response.output_text)
