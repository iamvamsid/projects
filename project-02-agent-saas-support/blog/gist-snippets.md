# Gist bundle for the Medium post

Medium mangles pasted code. Instead, create each snippet below as a **public GitHub Gist**,
then paste the Gist URL on its own line in Medium where the code belongs — it embeds as a
clean, highlighted widget. (Filenames give the gist syntax highlighting; keep the `.py`.)

Order matches the article. The three "output" snippets can also just be Medium code blocks
(they're console output, not code) — but gists look better and never break.

---

### 1 · agent-loop.txt  — (the loop diagram; goes after "a straight line becomes a loop")
```
user message
  -> model decides: answer directly, OR call a tool
       -> (tool call) my code runs the tool, returns the result
            -> model continues with the result
                 -> final answer, or another tool call ...
```

### 2 · search_docs.py  — (after "Reusing a whole RAG system as a single tool")
```python
def search_docs(query: str) -> dict:
    nodes = load_project1_index().as_retriever(similarity_top_k=3).retrieve(query)
    return {"results": [
        {"source": n.node.metadata.get("file_name"),
         "score": round(float(n.score), 3),
         "text": n.node.get_content()[:500]} for n in nodes]}
```

### 3 · chaining.txt  — (in "The three-source problem")
```
[step 1] get_account_status(acct_123)  -> plan: Pro
[step 2] get_plan_features(Pro)         -> priority_support: true
Agent: Yes - your Pro plan includes priority support.
```

### 4 · run_tool.py  — (Half 1, "your code never crashes")
```python
def run_tool(name, tool_input):
    try:
        return TOOL_FUNCTIONS[name](**tool_input)
    except TypeError as e:        # wrong/missing args
        return {"error": "bad_arguments", "detail": str(e)}
    except Exception as e:        # anything else
        return {"error": "tool_exception", "detail": str(e)}
```

### 5 · is_error.py  — (Half 2, "the model is told it failed")
```python
is_error = isinstance(result, dict) and "error" in result
tool_results.append({"type": "tool_result", "tool_use_id": tu.id,
                     "content": json.dumps(result), "is_error": is_error})
```

### 6 · trace-output.txt  — (in "Observability")
```
Question : Does my plan acct_123 include priority support?
  step 1  [tool_use]   1006 in /  77 out   $0.00696   2172ms
        -> get_account_status(...)   OK { ... "plan": "Pro" ... }
  step 2  [tool_use]   1126 in /  69 out   $0.00736   1556ms
        -> get_plan_features(...)    OK { ... "priority_support": true ... }
  step 3  [end_turn]   1249 in / 117 out   $0.00917   2614ms
SUMMARY  answered · 3 steps · 3381 in / 263 out tokens · $0.023480 · 6343ms
```

---

## Fast path: make ONE multi-file gist

You don't need six separate gists. Create a single gist and add all six files (the
"+ Add file" button). When you embed that one gist URL, Medium shows a file tab strip —
or, to place each snippet at its own spot, append `?file=run_tool.py` to the gist URL on
each line, e.g.:

```
https://gist.github.com/<you>/<id>?file=search_docs.py
https://gist.github.com/<you>/<id>?file=run_tool.py
```

Each line embeds only that one file's widget exactly where you put it.

## The image
Upload `docs/architecture.png` where the figure marker is (or use the raw URL:
`https://raw.githubusercontent.com/iamvamsid/projects/master/project-02-agent-saas-support/docs/architecture.png`).
