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
import time
from datetime import datetime
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from src.tools import TOOLS, run_tool
from src.trace import StepTrace, ToolCallTrace, Trace

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

MODEL = "claude-opus-4-8"
MAX_STEPS = 6  # safety cap so the loop can never run forever

# Day 4: what the CUSTOMER sees when the agent can't finish on its own. Never leak a
# developer string ("max steps reached") to a customer — escalate politely instead.
ESCALATION = (
    "I'm sorry — I wasn't able to resolve this automatically. I've escalated your "
    "request to a human support agent who will follow up shortly. Thanks for your patience."
)

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


def run(user_input: str, verbose: bool = True, collect_trace: bool = False):
    """Run the agent loop until the model produces a final answer.

    Returns the answer string. If collect_trace=True, also builds a structured
    Trace (Week 7 Day 3), saves it under traces/, and returns (answer, trace).
    """
    client = Anthropic()
    messages = [{"role": "user", "content": user_input}]
    seen_calls = set()   # Day 4: detect the model repeating an identical tool call (a stuck loop)

    # Day 3: observability. Build a trace as we go (cheap; only saved if requested).
    trace = Trace(user_input=user_input, model=MODEL,
                  started_at=datetime.now().isoformat())
    run_start = time.perf_counter()

    def _finish(text: str, outcome: str):
        """Common exit: stamp the trace, optionally save, and return."""
        trace.final_text = text
        trace.outcome = outcome
        trace.total_latency_ms = round((time.perf_counter() - run_start) * 1000, 1)
        if collect_trace:
            path = trace.save()
            if verbose:
                print(f"  [trace] saved -> {path.name}")
            return text, trace
        return text

    for step in range(1, MAX_STEPS + 1):
        t0 = time.perf_counter()
        response = client.messages.create(
            model=MODEL, max_tokens=1024, system=SYSTEM,
            tools=TOOLS, messages=messages,
        )
        model_ms = round((time.perf_counter() - t0) * 1000, 1)
        # Record this step's model call (token usage comes straight from the API).
        st = StepTrace(n=step, stop_reason=response.stop_reason,
                       input_tokens=response.usage.input_tokens,
                       output_tokens=response.usage.output_tokens,
                       model_latency_ms=model_ms)
        trace.steps.append(st)

        # CASE 1: the model is done — return its final answer.
        if response.stop_reason == "end_turn":
            return _finish("".join(b.text for b in response.content if b.type == "text"),
                           "answered")

        # CASE 2: the model wants to call one or more tools.
        if response.stop_reason == "tool_use":
            tool_uses = [b for b in response.content if b.type == "tool_use"]
            # Keep the assistant's turn (with its tool_use blocks) in the history.
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for tu in tool_uses:
                if verbose:
                    print(f"  [step {step}] model calls {tu.name}({json.dumps(tu.input)})")
                # Day 4: loop guard. If the model asks for the EXACT same call it already
                # made, it's stuck — repeating won't help. Escalate instead of spinning.
                sig = (tu.name, json.dumps(tu.input, sort_keys=True))
                if sig in seen_calls:
                    if verbose:
                        print(f"            -> [LOOP GUARD] repeated call to {tu.name}; escalating")
                    return _finish(ESCALATION, "loop_guard")
                seen_calls.add(sig)
                tt0 = time.perf_counter()
                result = run_tool(tu.name, tu.input)        # <-- OUR code runs the tool (never raises)
                tool_ms = round((time.perf_counter() - tt0) * 1000, 1)
                # Day 3: a result carrying an "error" key is a FAILURE. Tag it so the
                # model knows the tool failed and should adapt (clarify / try another
                # tool / escalate) instead of treating the error dict as a fact.
                is_error = isinstance(result, dict) and "error" in result
                if verbose:
                    tag = " [ERROR]" if is_error else ""
                    print(f"            ->{tag} {json.dumps(result)}")
                st.tool_calls.append(ToolCallTrace(name=tu.name, input=dict(tu.input),
                                                   result=result, is_error=is_error,
                                                   latency_ms=tool_ms))
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
        return _finish("".join(b.text for b in response.content if b.type == "text"),
                       "answered")

    # Day 4: hit the step cap without finishing — escalate gracefully (no debug leak).
    if verbose:
        print(f"            -> [MAX STEPS] reached {MAX_STEPS} steps without finishing; escalating")
    return _finish(ESCALATION, "max_steps")


def main():
    q = " ".join(sys.argv[1:]) or \
        "Is my account acct_123 on a plan that includes priority support?"
    print(f"Customer: {q}\n")
    answer = run(q)
    print(f"\nAgent: {answer}")


if __name__ == "__main__":
    main()
