"""The agent loop — manual, raw Anthropic SDK.

Day 3: wire the loop BY HAND so you can see every step. The cycle is:
  send the user message + the tools  ->  if the model asks for a tool, run it and
  send the result back  ->  repeat until the model produces a final answer.

This is exactly what the SDK tool-runner and agent frameworks do for you later;
here we do it ourselves so the mechanics are visible.

Run:  python -m src.agent "Is my account acct_123 on a plan with priority support?"
"""

import json
import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from src.tools import TOOLS, run_tool

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

MODEL = "claude-opus-4-8"
MAX_STEPS = 6  # safety cap so the loop can never run forever

SYSTEM = (
    "You are a customer support agent for a B2B SaaS product. Help the customer by "
    "answering their question.\n"
    "When the question depends on the customer's specific account (plan, billing, "
    "incidents), use the get_account_status tool — do not guess account details. For "
    "general questions you can answer directly.\n\n"
    "GUARDRAILS:\n"
    "- You may READ account status, but you must NOT take destructive or billing actions "
    "(refunds, plan changes, cancellations, deletions). If the customer asks for such an "
    "action, explain you can't perform it and that you'll escalate to a human.\n"
    "- If you don't have enough information, say so and recommend escalation rather than "
    "guessing."
)


def run(user_input: str, verbose: bool = True) -> str:
    """Run the agent loop until the model produces a final answer."""
    client = Anthropic()
    messages = [{"role": "user", "content": user_input}]

    for step in range(1, MAX_STEPS + 1):
        response = client.messages.create(
            model=MODEL, max_tokens=1024, system=SYSTEM,
            tools=TOOLS, messages=messages,
        )

        # CASE 1: the model is done — return its final answer.
        if response.stop_reason == "end_turn":
            return "".join(b.text for b in response.content if b.type == "text")

        # CASE 2: the model wants to call one or more tools.
        if response.stop_reason == "tool_use":
            tool_uses = [b for b in response.content if b.type == "tool_use"]
            # Keep the assistant's turn (with its tool_use blocks) in the history.
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for tu in tool_uses:
                if verbose:
                    print(f"  [step {step}] model calls {tu.name}({json.dumps(tu.input)})")
                result = run_tool(tu.name, tu.input)        # <-- OUR code runs the tool (never raises)
                # Day 3: a result carrying an "error" key is a FAILURE. Tag it so the
                # model knows the tool failed and should adapt (clarify / try another
                # tool / escalate) instead of treating the error dict as a fact.
                is_error = isinstance(result, dict) and "error" in result
                if verbose:
                    tag = " [ERROR]" if is_error else ""
                    print(f"            ->{tag} {json.dumps(result)}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tu.id,                   # must match the request
                    "content": json.dumps(result),
                    "is_error": is_error,                   # <-- the model reads this
                })
            # Hand the results back as the next user turn, then loop again.
            messages.append({"role": "user", "content": tool_results})
            continue

        # Any other stop reason — return whatever text we have, safely.
        return "".join(b.text for b in response.content if b.type == "text")

    return "[stopped: reached the maximum number of tool-calling steps]"


def main():
    q = " ".join(sys.argv[1:]) or \
        "Is my account acct_123 on a plan that includes priority support?"
    print(f"Customer: {q}\n")
    answer = run(q)
    print(f"\nAgent: {answer}")


if __name__ == "__main__":
    main()
