"""Week 7 Day 3 — structured run traces (observability).

A trace is a complete, replayable record of ONE agent run: every step, every tool
call, the token usage, and the timing. The terminal `[step]` prints scroll away;
a trace is written to disk so you can answer, after the fact:
  - what did the agent actually do, in what order?
  - which tool failed, and why?
  - how many tokens did each step cost?  (Day 4 turns tokens into $.)
  - which step was slow?

One run -> one JSON file under traces/. These dataclasses are just the SHAPE of
that record; the agent loop fills them in, and src/trace_view.py reads them back.
"""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

TRACES_DIR = Path(__file__).resolve().parent.parent / "traces"

# Day 4: prices in USD per 1,000,000 tokens, as (input, output).
# Source: Claude API pricing. The whole point of a trace is turning token counts
# into money, so the model the trace ran on determines the rate.
PRICES_PER_MTOK = {
    "claude-opus-4-8":   (5.0, 25.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-haiku-4-5":  (1.0, 5.0),
}


def cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    """Dollar cost of a call: tokens / 1M * the per-MTok rate for that model."""
    in_rate, out_rate = PRICES_PER_MTOK.get(model, (0.0, 0.0))
    return round(input_tokens / 1e6 * in_rate + output_tokens / 1e6 * out_rate, 6)


@dataclass
class ToolCallTrace:
    """One tool invocation within a step."""
    name: str
    input: dict
    result: object          # dict / list / str — whatever the tool returned
    is_error: bool
    latency_ms: float


@dataclass
class StepTrace:
    """One trip around the loop: a single model call + any tools it triggered."""
    n: int
    stop_reason: str
    input_tokens: int
    output_tokens: int
    model_latency_ms: float
    tool_calls: list[ToolCallTrace] = field(default_factory=list)


@dataclass
class Trace:
    """The whole run."""
    user_input: str
    model: str
    started_at: str
    steps: list[StepTrace] = field(default_factory=list)
    final_text: str = ""
    outcome: str = ""           # "answered" | "escalated" | "max_steps" | "loop_guard"
    total_latency_ms: float = 0.0

    # --- convenience roll-ups (handy for Day 4/5; cheap to compute now) -------
    @property
    def total_input_tokens(self) -> int:
        return sum(s.input_tokens for s in self.steps)

    @property
    def total_output_tokens(self) -> int:
        return sum(s.output_tokens for s in self.steps)

    @property
    def tools_used(self) -> list[str]:
        return [tc.name for s in self.steps for tc in s.tool_calls]

    @property
    def total_cost_usd(self) -> float:
        """Day 4: total $ cost of the run (all steps), at this model's rate."""
        return cost_usd(self.model, self.total_input_tokens, self.total_output_tokens)

    def summary(self) -> dict:
        """The operational vitals: steps, tools, tokens, cost, latency."""
        return {
            "outcome": self.outcome,
            "steps": len(self.steps),
            "tools_used": self.tools_used,
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "cost_usd": self.total_cost_usd,
            "latency_ms": self.total_latency_ms,
        }

    def to_dict(self) -> dict:
        d = asdict(self)
        # Day 4: annotate each step with its own cost, and roll up totals.
        for step_dict, step in zip(d["steps"], self.steps):
            step_dict["cost_usd"] = cost_usd(self.model, step.input_tokens, step.output_tokens)
        d["total_input_tokens"] = self.total_input_tokens
        d["total_output_tokens"] = self.total_output_tokens
        d["total_cost_usd"] = self.total_cost_usd
        d["tools_used"] = self.tools_used
        return d

    def save(self, traces_dir: Path = TRACES_DIR) -> Path:
        traces_dir.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        path = traces_dir / f"{ts}.json"
        path.write_text(json.dumps(self.to_dict(), indent=2, default=str))
        return path
