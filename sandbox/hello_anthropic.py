"""Minimal Claude hello world — Day 2, week 01."""

from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = Anthropic()
model = "claude-sonnet-4-6"

# Anthropic runs this server-side — no tool loop needed on your end.
WEB_SEARCH_TOOL = {
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 3,
}

hello_messages = [
    {"role": "user", "content": "Explain attention in one paragraph."}
]
stock_messages = [
    {
        "role": "user",
        "content": "What is Amazon (AMZN) share price as of June 17, 2026? Search the web.",
    }
]


def print_text_blocks(response) -> None:
    for block in response.content:
        if block.type != "text":
            continue
        print(block.text)
        if block.citations:
            print("\nSources:")
            for cite in block.citations:
                print(f"  - {cite.title}: {cite.url}")


print("=== Non-streaming ===")
response = client.messages.create(
    model=model,
    max_tokens=200,
    messages=hello_messages,
)
print(response.content[0].text)

print("\n=== Streaming ===")
with client.messages.stream(
    model=model,
    max_tokens=200,
    messages=hello_messages,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
print()

print("\n=== Web search (live data) ===")
response = client.messages.create(
    model=model,
    max_tokens=1024,
    messages=stock_messages,
    tools=[WEB_SEARCH_TOOL],
)
print_text_blocks(response)

print("\n=== Web search + streaming ===")
with client.messages.stream(
    model=model,
    max_tokens=1024,
    messages=stock_messages,
    tools=[WEB_SEARCH_TOOL],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
print()
