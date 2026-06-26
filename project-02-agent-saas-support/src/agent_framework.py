"""The agent — version 3 of 3: an AGENT FRAMEWORK (LlamaIndex).

The most abstracted version. We hand the framework a tool, an LLM, and a system
prompt; its FunctionAgent runs the ENTIRE loop. Compare the three:

  - src/agent.py            : WE write the loop (raw SDK)
  - src/agent_toolrunner.py : the SDK runs the loop
  - this file               : the FRAMEWORK runs the loop AND wraps the LLM + tools + prompt

Least code, most hidden. We built it by hand first (Day 3), so none of this is
mysterious — we know exactly what FunctionAgent is doing under the surface.

Run:  python -m src.agent_framework "Is acct_123 on a plan with priority support?"
"""

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.anthropic import Anthropic

from src.agent import MODEL, SYSTEM
from src.tools import GET_ACCOUNT_STATUS_TOOL, get_account_status

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def build_agent() -> FunctionAgent:
    llm = Anthropic(model=MODEL, max_tokens=1024)
    # Wrap our plain Python function as a framework tool. We pass the same
    # description we used in the other two versions so behavior is comparable.
    tool = FunctionTool.from_defaults(
        fn=get_account_status,
        name="get_account_status",
        description=GET_ACCOUNT_STATUS_TOOL["description"],
    )
    return FunctionAgent(tools=[tool], llm=llm, system_prompt=SYSTEM)


def run(user_input: str) -> str:
    agent = build_agent()
    # FunctionAgent.run must be awaited inside an async context.
    async def _run_agent() -> str:
        response = await agent.run(user_input)
        return str(response)

    return asyncio.run(_run_agent())


def main():
    q = " ".join(sys.argv[1:]) or \
        "Is my account acct_123 on a plan that includes priority support?"
    print(f"Customer: {q}\n")
    print(f"Agent: {run(q)}")


if __name__ == "__main__":
    main()
