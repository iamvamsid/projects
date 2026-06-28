"""Week 7 Day 5 — the trace viewer.

A trace on disk is JSON: complete, but not readable. This pretty-prints one run
as a timeline (each step, each tool call, tokens / cost / latency) plus the
one-line operational summary. It's the "show a teammate or an exec what the agent
did" artifact — the human-readable face of the trace.

Run:  python -m src.trace_view                 # newest trace in traces/
      python -m src.trace_view <file.json>     # a specific trace
      python -m src.trace_view --last 3        # the 3 most recent, each summarized
"""

import json
import sys
from pathlib import Path

from src.trace import TRACES_DIR


def _newest(n: int = 1) -> list[Path]:
    files = sorted(TRACES_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[:n]


def _short(obj, n: int = 90) -> str:
    s = json.dumps(obj, ensure_ascii=False) if not isinstance(obj, str) else obj
    return s if len(s) <= n else s[: n - 1] + "…"


def render(trace: dict) -> str:
    """Render one trace dict as a readable timeline + summary."""
    out = []
    out.append("─" * 72)
    out.append(f"Question : {trace['user_input']}")
    out.append(f"Model    : {trace['model']}    Started: {trace.get('started_at', '')[:19]}")
    out.append("─" * 72)

    for s in trace["steps"]:
        cost = s.get("cost_usd", 0.0)
        out.append(
            f"  step {s['n']}  [{s['stop_reason']:<9}]  "
            f"{s['input_tokens']:>5} in / {s['output_tokens']:>3} out   "
            f"${cost:.5f}   {s['model_latency_ms']:.0f}ms"
        )
        for tc in s.get("tool_calls", []):
            mark = "✗ ERROR" if tc["is_error"] else "✓"
            out.append(f"        → {tc['name']}({_short(tc['input'], 60)})")
            out.append(f"          {mark} {_short(tc['result'])}   ({tc['latency_ms']:.0f}ms)")

    out.append("")
    out.append("Answer:")
    for line in (trace.get("final_text") or "").strip().splitlines() or ["(none)"]:
        out.append(f"  {line}")

    out.append("")
    out.append("─" * 72)
    out.append(
        f"SUMMARY  {trace['outcome']} · {len(trace['steps'])} steps · "
        f"tools: {', '.join(trace.get('tools_used') or ['none'])}"
    )
    out.append(
        f"         {trace.get('total_input_tokens', 0)} in / "
        f"{trace.get('total_output_tokens', 0)} out tokens · "
        f"${trace.get('total_cost_usd', 0.0):.6f} · "
        f"{trace.get('total_latency_ms', 0.0):.0f}ms"
    )
    out.append("─" * 72)
    return "\n".join(out)


def summarize_line(path: Path) -> str:
    """One-line summary of a trace file (for --last listings)."""
    t = json.loads(path.read_text())
    return (f"{path.name}  {t['outcome']:<9} {len(t['steps'])} steps  "
            f"${t.get('total_cost_usd', 0.0):.5f}  {t.get('total_latency_ms', 0.0):.0f}ms  "
            f"| {_short(t['user_input'], 50)}")


def _resolve_trace_path(raw: str) -> Path | None:
    """Resolve a CLI path robustly (explicit path, traces/<name>, .json fallback)."""
    p = Path(raw)
    candidates = [p, TRACES_DIR / p]

    # Common typo: pass ".js" or no extension; traces are always .json.
    if p.suffix != ".json":
        candidates.extend([p.with_suffix(".json"), TRACES_DIR / p.with_suffix(".json")])

    for c in candidates:
        if c.exists():
            return c
    return None


def main():
    args = sys.argv[1:]
    if args and args[0] == "--last":
        n = int(args[1]) if len(args) > 1 else 5
        files = _newest(n)
        if not files:
            print(f"No traces in {TRACES_DIR}")
            return
        for p in files:
            print(summarize_line(p))
        return

    if args:
        path = _resolve_trace_path(args[0])
        if path is None:
            print(f"Trace file not found: {args[0]}")
            newest = _newest(3)
            if newest:
                print("\nTry one of these:")
                for p in newest:
                    print(f"  {p}")
            else:
                print(f"\nNo traces found in {TRACES_DIR}")
            return
    else:
        newest = _newest(1)
        if not newest:
            print(f"No traces in {TRACES_DIR}. Run an agent with collect_trace=True first.")
            return
        path = newest[0]

    print(render(json.loads(path.read_text())))


if __name__ == "__main__":
    main()
