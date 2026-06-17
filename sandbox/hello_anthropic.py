"""Minimal Claude hello world — Day 2, week 01."""

from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = Anthropic()
model = "claude-sonnet-4-6"
messages = [{"role": "user", "content": "Explain attention in one paragraph."}]

print("=== Non-streaming ===")
response = client.messages.create(
    model=model,
    max_tokens=200,
    messages=messages,
)
print(response.content[0].text)

print("\n=== Streaming ===")
with client.messages.stream(
    model=model,
    max_tokens=200,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
print()
