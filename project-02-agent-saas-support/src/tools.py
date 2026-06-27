"""Tools the support agent can call.

Day 2: the FIRST tool — get_account_status — with its schema and a mock
implementation. No agent loop yet (that's Day 3). A "tool" has two halves:

  1. The PYTHON FUNCTION that actually does the work (here, returns canned data).
  2. The SCHEMA the model reads to decide WHEN and HOW to call it.

Run a standalone check:  python -m src.tools
"""

from pathlib import Path

from dotenv import load_dotenv

# search_docs embeds queries via OpenAI, so load keys here too (not just in agent.py).
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


# --- Mock "database" of customer accounts -----------------------------------
# Canned data standing in for a real account API. In production this function
# would call your billing/account service; the agent never sees the difference.
_ACCOUNTS = {
    "acct_123": {"plan": "Pro",        "billing_status": "active",   "active_incident": None},
    "acct_456": {"plan": "Free",       "billing_status": "active",   "active_incident": None},
    "acct_789": {"plan": "Enterprise", "billing_status": "past_due",
                 "active_incident": "Elevated API latency in us-east-1"},
}


# --- 1. The function --------------------------------------------------------
def get_account_status(account_id: str) -> dict:
    """Look up a customer's account status. Mock implementation."""
    account = _ACCOUNTS.get(account_id)
    if account is None:
        return {"error": "account_not_found", "account_id": account_id}
    return {"account_id": account_id, **account}


# --- 2. The schema the model sees (Anthropic tool-use format) ---------------
GET_ACCOUNT_STATUS_TOOL = {
    "name": "get_account_status",
    "description": (
        "Look up a customer's account status — plan tier, billing status, and any "
        "active incident — by account id. Use this when the question depends on the "
        "customer's specific account, not on general documentation."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "account_id": {
                "type": "string",
                "description": "The customer's account id, e.g. 'acct_123'.",
            }
        },
        "required": ["account_id"],
    },
}


# --- Tool 2: search_docs (Week 6) — reuse Project 1's retrieval -------------
# Instead of rebuilding a RAG system, we load Project 1's already-persisted index
# and expose it as a tool. The agent's knowledge of "how the product works" is
# literally Project 1, now a capability the agent can call.

# Project 1's persisted index lives in the sibling repo.
_P1_INDEX = Path(__file__).resolve().parents[2] / "project-01-rag-saas-support" / "storage"
_P1_EMBED_MODEL = "text-embedding-3-small"   # MUST match Project 1's ingest config
_p1_index = None


def _load_p1_index():
    """Load Project 1's vector index once, then cache it."""
    global _p1_index
    if _p1_index is None:
        from llama_index.core import Settings, StorageContext, load_index_from_storage
        from llama_index.embeddings.openai import OpenAIEmbedding
        Settings.embed_model = OpenAIEmbedding(model=_P1_EMBED_MODEL)
        ctx = StorageContext.from_defaults(persist_dir=str(_P1_INDEX))
        _p1_index = load_index_from_storage(ctx)
    return _p1_index


def search_docs(query: str) -> dict:
    """Search the product documentation. Returns top passages with sources."""
    if not _P1_INDEX.exists():
        return {"error": "docs_index_unavailable",
                "detail": f"No index at {_P1_INDEX}. Build Project 1 first."}
    nodes = _load_p1_index().as_retriever(similarity_top_k=3).retrieve(query)
    if not nodes:
        return {"results": [], "note": "no relevant documentation found"}
    return {"results": [
        {"source": n.node.metadata.get("file_name"),
         "score": round(float(n.score), 3),
         "text": n.node.get_content()[:500]}
        for n in nodes
    ]}


SEARCH_DOCS_TOOL = {
    "name": "search_docs",
    "description": (
        "Search the product documentation for how the product works — including what "
        "features and support levels each plan includes. Use for general 'how do I' and "
        "'what does X include' questions. Do NOT use it for a customer's specific account "
        "state (use get_account_status for that)."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "What to look up in the docs."}
        },
        "required": ["query"],
    },
}


# --- Tool 3: get_plan_features (Week 6 Day 2) — the ENTITLEMENTS source ------
# Day-2 finding: account state knows the PLAN NAME ("Pro") and product docs know
# FEATURES, but nothing maps plan -> features. "What a plan includes" is entitlements
# data — in production it lives in a billing/entitlements service, NOT product docs.
# This tool is that source. Now "does my plan include priority support?" can be
# answered by CHAINING: get_account_status (which plan) -> get_plan_features (what it includes).
_PLAN_FEATURES = {
    "Free":       {"support": "Community support (forums)", "priority_support": False,
                   "sla": None,        "seats": 1,  "sso": False},
    "Pro":        {"support": "Email support",              "priority_support": True,
                   "sla": "99.9%",     "seats": 10, "sso": False},
    "Enterprise": {"support": "Dedicated support manager",  "priority_support": True,
                   "sla": "99.99%",    "seats": "unlimited", "sso": True},
}


def get_plan_features(plan: str) -> dict:
    """Look up what a plan tier includes (support level, SLA, seats, SSO)."""
    features = _PLAN_FEATURES.get(plan)
    if features is None:
        return {"error": "unknown_plan", "plan": plan,
                "known_plans": list(_PLAN_FEATURES)}
    return {"plan": plan, **features}


GET_PLAN_FEATURES_TOOL = {
    "name": "get_plan_features",
    "description": (
        "Look up what a PLAN TIER includes — support level, whether priority support is "
        "included, SLA, seat count, SSO — by plan name (e.g. 'Pro'). Use this for "
        "'what does my plan include / does my plan have X' questions. If you don't know "
        "which plan the customer is on, call get_account_status first to find the plan name."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "plan": {"type": "string",
                     "description": "The plan tier name, e.g. 'Free', 'Pro', 'Enterprise'."}
        },
        "required": ["plan"],
    },
}


# --- Registry the agent loop uses (Day 2: three tools) ----------------------
TOOLS = [GET_ACCOUNT_STATUS_TOOL, SEARCH_DOCS_TOOL, GET_PLAN_FEATURES_TOOL]
TOOL_FUNCTIONS = {
    "get_account_status": get_account_status,
    "search_docs": search_docs,
    "get_plan_features": get_plan_features,
}


def run_tool(name: str, tool_input: dict) -> dict:
    """Dispatch a tool call by name. The agent loop calls this.

    Day 3 (error recovery): this must NEVER raise. Whatever goes wrong — unknown
    tool, bad/missing arguments (TypeError from **tool_input), or the tool itself
    blowing up — is caught and returned as an {"error": ...} dict. The loop then
    tags it is_error=True so the model can adapt instead of the program crashing.
    """
    fn = TOOL_FUNCTIONS.get(name)
    if fn is None:
        return {"error": "unknown_tool", "name": name,
                "known_tools": list(TOOL_FUNCTIONS)}
    try:
        return fn(**tool_input)
    except TypeError as e:
        # Wrong/missing/extra arguments for this tool.
        return {"error": "bad_arguments", "tool": name,
                "got": tool_input, "detail": str(e)}
    except Exception as e:
        # Any other failure inside the tool (network, parsing, etc.).
        return {"error": "tool_exception", "tool": name, "detail": str(e)}


if __name__ == "__main__":
    # Day-2 sanity check: the tool works on its own, no model involved yet.
    import json
    for acc in ["acct_123", "acct_789", "acct_000"]:
        print(f"{acc} -> {json.dumps(get_account_status(acc))}")
