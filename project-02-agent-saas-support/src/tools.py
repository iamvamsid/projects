"""Tools the support agent can call.

Day 2: the FIRST tool — get_account_status — with its schema and a mock
implementation. No agent loop yet (that's Day 3). A "tool" has two halves:

  1. The PYTHON FUNCTION that actually does the work (here, returns canned data).
  2. The SCHEMA the model reads to decide WHEN and HOW to call it.

Run a standalone check:  python -m src.tools
"""

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


# --- Registry the agent loop will use (Day 3) -------------------------------
TOOLS = [GET_ACCOUNT_STATUS_TOOL]                       # what we send to the model
TOOL_FUNCTIONS = {"get_account_status": get_account_status}  # name -> function


def run_tool(name: str, tool_input: dict) -> dict:
    """Dispatch a tool call by name. The agent loop calls this in Day 3."""
    fn = TOOL_FUNCTIONS.get(name)
    if fn is None:
        return {"error": "unknown_tool", "name": name}
    return fn(**tool_input)


if __name__ == "__main__":
    # Day-2 sanity check: the tool works on its own, no model involved yet.
    import json
    for acc in ["acct_123", "acct_789", "acct_000"]:
        print(f"{acc} -> {json.dumps(get_account_status(acc))}")
