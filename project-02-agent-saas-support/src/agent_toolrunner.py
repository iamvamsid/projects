"""The agent — version 2 of 3: the SDK TOOL RUNNER.

Same agent as src/agent.py, but the SDK runs the loop for us. Compare the two:
  - src/agent.py     : WE write the while-loop, detect tool_use, run tools, send
                       results back, repeat. ~40 lines of loop.
  - this file        : we decorate the tool function and hand it to tool_runner();
                       the SDK does the whole loop. The loop is GONE from our code.

The trade: less code, but the mechanics are hidden. We did it by hand first (Day 3)
precisely so this "magic" is understood.

Run:  python -m src.agent_toolrunner "Is acct_123 on a plan with priority support?"
"""

import json
import sys
from pathlib import Path

from anthropic import Anthropic, beta_tool
from dotenv import load_dotenv

from src.agent import MODEL, SYSTEM          # reuse the SAME model + system prompt
from src.tools import get_account_status as _lookup

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


# With the tool runner, the SCHEMA is generated automatically from the function
# signature + this docstring — so the docstring IS the tool description the model reads.
@beta_tool
def get_account_status(account_id: str) -> str:
    """Look up a customer's account status — plan tier, billing status, and any active
    incident — by account id. Use when the question depends on the customer's specific
    account, not on general documentation.

    Args:
        account_id: The customer's account id, e.g. 'acct_123'.
    """
    print("running tool")
    return json.dumps(_lookup(account_id))   # reuse the same underlying mock logic


def run(user_input: str, verbose: bool = True) -> str:
    client = Anthropic()

    # No manual loop. We hand the tool to the runner and iterate the messages it yields;
    # the SDK calls the tool and feeds results back automatically until Claude is done.
    runner = client.beta.messages.tool_runner(
        model=MODEL, max_tokens=1024, system=SYSTEM,
        tools=[get_account_status],
        messages=[{"role": "user", "content": user_input}],
    )

    print("after runner")

    final_text = ""
    for message in runner:
        for b in message.content:
            if verbose and b.type == "tool_use":
                print(f"  model calls {b.name}({json.dumps(b.input)})  "
                      f"[SDK runs it automatically]")
        text = "".join(b.text for b in message.content if b.type == "text")
        if text.strip():
            final_text = text
    return final_text


def main():
    q = " ".join(sys.argv[1:]) or \
        "Is my account acct_123 on a plan that includes priority support?"
    print(f"Customer: {q}\n")
    print(f"\nAgent: {run(q)}")


if __name__ == "__main__":
    main()
