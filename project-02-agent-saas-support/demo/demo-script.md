# 5-Minute Demo Script — B2B SaaS Support Agent

**Audience:** a non-technical executive (CTO/VP). Present it as if they will never read the code.
**Goal:** they leave understanding *what it does*, *why it's safe*, and *that you can see/price every action*.
**Length:** aim for 4:30–5:00. Practice once out loud before recording.

---

## Before you hit record (pre-flight)

1. Terminal open, **large font** (18pt+), dark or light — whatever reads clearly on video.
2. Activate the env and `cd` in:
   ```bash
   cd /Users/vamsidhar/Google/ai-journey/projects && source .ai-proj/bin/activate && cd project-02-agent-saas-support
   ```
3. Pre-warm so the first run isn't slow on camera (loads the doc index once):
   ```bash
   python -m src.agent "How do I enable row level security?" >/dev/null 2>&1
   ```
4. Have the **architecture diagram** open in a second window (`docs/architecture.png`) to show during the intro.
5. Clear the terminal (`clear`). Recorder ready (Loom or QuickTime → File → New Screen Recording).

> Tip: keep each command already typed in a scratch file and paste it, so you're not typing on camera.

---

## [0:00–0:30] The problem  *(talk to camera / diagram — no terminal yet)*

**SAY:**
> "Support teams are drowning in tickets, and the answer to a single question is usually scattered across three systems — the customer's account, the product docs, and what their plan actually includes. So responses are slow and inconsistent, and skilled people spend their day on routine lookups. I built an AI agent that pulls those together and handles the conversation end to end — and, just as importantly, knows when to stop and hand off to a human."

## [0:30–1:00] What it is  *(show the architecture diagram)*

**DO:** put `docs/architecture.png` on screen.
**SAY:**
> "Here's the shape of it. A customer question comes in. The agent decides which sources it needs and pulls them together — account status, a documentation search, and plan entitlements. It remembers the conversation, and — this part matters — every single action it takes is logged: what it did, how long it took, and what it cost. Let me show you three things: it answering a real question, it handling something it *shouldn't* do, and the full audit trail."

---

## [1:00–2:00] Beat 1 — it chains tools to answer  *(switch to terminal)*

**DO:** run
```bash
python -m src.agent "Does my plan acct_123 include priority support?"
```
**SAY (while the step lines appear):**
> "This question can't be answered by one system. Watch — the agent first looks up the account and finds it's on the Pro plan… then, because it now knows the plan, it checks what Pro actually includes… and combines them into one answer: *yes, Pro includes priority support.* It chained two lookups on its own — I didn't script that order, it worked it out from the question."

*(Point at the two `[step]` lines, then the final answer.)*

## [2:00–3:00] Beat 2 — it stays safe under pressure  *(terminal)*

**DO:** run
```bash
python -m src.agent "What plan is acct_789 on, and please cancel its subscription."
```
**SAY:**
> "Now the risky case. The customer asks for a lookup *and* a cancellation. A naive bot either refuses everything or — worse — cancels the subscription. This one does neither. It answers the safe part — the account is on Enterprise — and then it *refuses* to cancel, because billing actions are off-limits, and escalates that to a human. Safe part done, dangerous part handed off, in the same reply. That boundary is the whole reason you can trust it in front of customers."

*(Optional 15s, if time:)*
```bash
python -m src.agent "What plan is acct_999 on?"
```
> "And when something genuinely isn't found, it doesn't invent an answer — it says so and escalates."

## [3:00–4:00] Beat 3 — you can see and price every action  *(terminal)*

**DO:** run a traced question, then the viewer:
```bash
python -c "from src.agent import run; run('Does my plan acct_123 include priority support?', verbose=False, collect_trace=True)"
python -m src.trace_view
```
**SAY (over the timeline output):**
> "Every run produces a record like this. You can see each step the agent took, which tool it called and what came back, and for each one — the time it took and the exact cost in dollars. This whole interaction was about two-and-a-half cents and six seconds. So you're never guessing what the agent did or what it costs to run — it's all here, per ticket. That's what makes it operable, not just impressive."

---

## [4:00–5:00] Why it matters + honest close  *(talk to camera)*

**SAY:**
> "So: faster, consistent first responses on the routine questions, your people freed up for the cases that actually need them, and a complete, costed audit trail behind every answer. It extends the team's capacity without giving up control or visibility.
>
> To be straight with you — this is a working prototype. The account and billing connections use stand-in data right now, but it's built so that wiring in the real systems doesn't change how the agent behaves. The technical write-up and the full code are available. Thanks for watching."

---

## Recording tips
- **One re-take is fine, three is procrastination.** Slightly rough but confident beats over-polished.
- Keep the cursor calm; pause ~1s after each command finishes so the viewer can read it.
- If a run is slower than expected on camera, keep narrating — don't go silent.
- Export, watch it once at 1.25× to catch dead air, then publish (Loom gives an instant link; or upload unlisted to YouTube).
- Put the link in `weeks/week-08.md` and the README when done.

## The 3 commands, all in one place (paste targets)
```bash
python -m src.agent "Does my plan acct_123 include priority support?"
python -m src.agent "What plan is acct_789 on, and please cancel its subscription."
python -c "from src.agent import run; run('Does my plan acct_123 include priority support?', verbose=False, collect_trace=True)" && python -m src.trace_view
```
