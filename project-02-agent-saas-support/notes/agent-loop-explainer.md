# The agent loop — in my own words

> Homework scaffold. Fill each section in YOUR words (interview prep — if you can't
> explain it without notes, you don't own it yet). Prompts are hints, not answers.

## 1. What an agent loop actually is
_(One paragraph. How is it different from Project 1's retrieve → generate straight line?
Who decides the steps — you or the model?)_

- After analysing the question from user loop calls back again with tools for more information. it will be calling back again and again for more information from the tools until it get's the required information to respond. 

We set the maximum number of steps

## 2. One trip around the loop
_(Walk through the four moves: send message + tools → model returns `stop_reason` →
if `tool_use`, run the tool and send `tool_result` back → repeat until `end_turn`.
What do `tool_use_id` and the assistant/user turn ordering do?)_

- tool_use_id tells you the tools that I need to use

## 3. Routing vs. chaining
_(Two tools, one question = routing — model picks the right one. Some questions need
several tools. When does it run them in PARALLEL vs. SEQUENTIAL? Use the priority-support
example: why must `get_account_status` happen before `get_plan_features`?)_
PARALLEL -  when tool execution is independent of other
SEQUENTIAL - when one tool output is required for other tool execution
get_account_status is required to know what kind of user he is (pro/free/enterprise) and based on that get_plan_features will output it's features

-

## 4. Why three data sources
_(Account state, product docs, entitlements. What does each know? Why couldn't "does my
plan include priority support?" be answered by account + docs alone — what was missing?)_

Account state - To know what kind of user he is (pro/free/enterprise)
product docs - this doc has all info about the product.
account + docs alone - this requires embedding of vectors but having entitlements reduces the need for embeddings


-

## 5. Failing gracefully
_(Two halves: your code never crashes (`run_tool` try/except) AND the model is told it
failed (`is_error: true`). Why do you need BOTH? What would break if you had only one?)_

If there is any error instead of crashing let's escalate to human in except block

-

## 6. Guardrails
_(The mixed request: "what plan is acct_789 on, and cancel it." Why answer the read but
refuse the action? Why escalate instead of just saying no?)_

If the user really wants to cancel, escalate to human as this is a critical which impacts business

-

## 7. The three build styles
_(Manual loop vs. SDK tool_runner vs. LlamaIndex FunctionAgent. What does each layer hide?
Why build the manual one first?)_
Manual loop - No hidden
SDK tool_runner - tool calling hidden
LlamaIndex FunctionAgent - tool calling, number of retries, calling AI model

-

## 8. The 60-second version (for an interviewer)
_(Compress all of the above into something you could say out loud in a screen.)_

-
