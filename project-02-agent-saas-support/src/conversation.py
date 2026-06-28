"""Week 7 Day 1 — multi-turn memory.

`agent.run()` starts FRESH every call: it builds a new `messages` list, answers
once, and throws the history away. That's fine for one-shot Q&A but useless for a
real support chat, where a follow-up ("does IT include SSO?") depends on an earlier
turn ("what plan is acct_123 on?").

A `Conversation` fixes that by OWNING the `messages` list and keeping it across
turns. Each `.send()` is one turn appended to the same history — so the model sees
everything that came before. That persistent list *is* the memory.

Two things that differ from agent.run():
  1. We append the assistant's FINAL answer back into history (run() didn't bother,
     since it discarded the list) — otherwise the next turn wouldn't remember what
     the agent said.
  2. The loop guard (seen_calls) resets PER TURN, not per conversation: re-calling
     get_account_status in a later turn is legitimate, not a stuck loop.

Run a demo:  python -m src.conversation
"""

import json
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from src.agent import ESCALATION, MAX_STEPS, MODEL, SYSTEM
from src.tools import TOOLS, run_tool

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


MAX_TURNS = 6   # Day 2: keep at most this many recent CUSTOMER turns of history


class Conversation:
    """A multi-turn support session. The `messages` list persists = memory."""

    def __init__(self, max_turns: int = MAX_TURNS):
        self.client = Anthropic()
        self.messages: list[dict] = []   # <-- survives across .send() calls = MEMORY
        self.max_turns = max_turns

    def _trim(self, verbose: bool = False) -> None:
        """Day 2: bound memory so it can't grow forever.

        We only ever cut at a CUSTOMER-turn boundary (role=user with plain string
        content — not a tool_result turn). That guarantees we never orphan a
        tool_result from its tool_use, which would make the API reject the history.
        Keeps the most recent `max_turns` customer turns and everything after.
        """
        customer_idxs = [i for i, m in enumerate(self.messages)
                         if m["role"] == "user" and isinstance(m["content"], str)]
        if len(customer_idxs) <= self.max_turns:
            return
        cut = customer_idxs[-self.max_turns]      # first index we keep
        if verbose:
            print(f"    [memory] trimming {cut} old messages "
                  f"(keeping last {self.max_turns} customer turns)")
        self.messages = self.messages[cut:]

    def send(self, user_input: str, verbose: bool = True) -> str:
        """Run ONE turn: append the user message, drive the tool loop, return the answer.
        The whole conversation so far is sent every time, so the model has context."""
        self.messages.append({"role": "user", "content": user_input})
        self._trim(verbose=verbose)              # bound history before we send it
        seen_calls = set()   # per-turn: a repeat WITHIN one turn is a stuck loop

        for step in range(1, MAX_STEPS + 1):
            response = self.client.messages.create(
                model=MODEL, max_tokens=1024, system=SYSTEM,
                tools=TOOLS, messages=self.messages,
            )

            # Always record the assistant turn so memory stays complete.
            self.messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                # end_turn (or anything else) — return the final text.
                return "".join(b.text for b in response.content if b.type == "text")

            # tool_use: run each requested tool, append results, loop again.
            tool_results = []
            for tu in (b for b in response.content if b.type == "tool_use"):
                if verbose:
                    print(f"    [step {step}] calls {tu.name}({json.dumps(tu.input)})")
                sig = (tu.name, json.dumps(tu.input, sort_keys=True))
                if sig in seen_calls:
                    if verbose:
                        print(f"            -> [LOOP GUARD] repeated {tu.name}; escalating")
                    return ESCALATION
                seen_calls.add(sig)
                result = run_tool(tu.name, tu.input)
                is_error = isinstance(result, dict) and "error" in result
                if verbose:
                    print(f"            ->{' [ERROR]' if is_error else ''} {json.dumps(result)}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tu.id,
                    "content": json.dumps(result),
                    "is_error": is_error,
                })
            self.messages.append({"role": "user", "content": tool_results})

        return ESCALATION   # hit the step cap


def _valid_pairing(messages: list[dict]) -> bool:
    """Every tool_use must be answered by a tool_result with the matching id, and
    no tool_result may be orphaned. Returns True if the history is API-valid."""
    pending: set[str] = set()
    for m in messages:
        content = m["content"]
        if isinstance(content, list):
            for b in content:
                btype = b.get("type") if isinstance(b, dict) else getattr(b, "type", None)
                if btype == "tool_use":
                    pending.add(b.id if not isinstance(b, dict) else b["id"])
                elif btype == "tool_result":
                    tid = b["tool_use_id"]
                    if tid not in pending:
                        return False          # orphaned result
                    pending.discard(tid)
    return not pending                         # nothing left unanswered


def _test_trim_keeps_history_valid():
    """Deterministic (no API): a long fake history trims to a VALID, bounded one."""
    convo = Conversation(max_turns=2)
    # Fake 4 complete turns, each: user -> assistant(tool_use) -> user(tool_result) -> assistant(text)
    for n in range(4):
        convo.messages.append({"role": "user", "content": f"question {n}"})
        convo.messages.append({"role": "assistant",
                               "content": [{"type": "tool_use", "id": f"t{n}", "name": "x", "input": {}}]})
        convo.messages.append({"role": "user",
                               "content": [{"type": "tool_result", "tool_use_id": f"t{n}", "content": "{}"}]})
        convo.messages.append({"role": "assistant", "content": [{"type": "text", "text": f"answer {n}"}]})
    before = len(convo.messages)
    convo._trim(verbose=True)
    after = len(convo.messages)
    customer_turns = sum(1 for m in convo.messages
                         if m["role"] == "user" and isinstance(m["content"], str))
    ok = _valid_pairing(convo.messages) and customer_turns == 2
    print(f"    trimmed {before} -> {after} messages; customer_turns={customer_turns}; "
          f"valid_pairing={_valid_pairing(convo.messages)}")
    print(f"    {'PASS' if ok else 'FAIL'}: trim bounded history AND kept it API-valid\n")


def _live_continuity_demo():
    """Live: guardrails + routing hold mid-conversation, with memory intact."""
    convo = Conversation()
    turns = [
        "What plan is acct_123 on?",                 # routing -> account
        "Does it include SSO?",                      # chaining -> entitlements, "it"=Pro
        "Great, please cancel my subscription.",     # GUARDRAIL mid-convo: must refuse + escalate
        "Okay. What's my SLA then?",                 # memory still intact after the refusal
    ]
    for i, t in enumerate(turns, 1):
        print(f"\n=== Turn {i} ===\nCustomer: {t}")
        print(f"Agent: {convo.send(t)}")
    print(f"\n[memory] kept {len(convo.messages)} messages; valid_pairing={_valid_pairing(convo.messages)}")


def main():
    print("== Day 2: memory bound is valid (deterministic) ==")
    _test_trim_keeps_history_valid()
    print("== Day 2: continuity — guardrails/routing hold across turns (live) ==")
    _live_continuity_demo()


if __name__ == "__main__":
    main()
