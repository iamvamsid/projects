"""Minimal OpenAI hello world — Day 2, week 01."""

from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = OpenAI()
model = "gpt-4o"
messages = [{"role": "user", "content": "Explain attention in one paragraph."}]

print("=== Non-streaming ===")
response = client.chat.completions.create(
    model=model,
    max_tokens=200,
    messages=messages,
)
print(response.choices[0].message.content)

print("\n=== Streaming ===")
stream = client.chat.completions.create(
    model=model,
    max_tokens=200,
    messages=messages,
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()
