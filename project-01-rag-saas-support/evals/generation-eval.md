# Generation eval (LLM-as-judge: claude-sonnet-4-6)


**Q1** (factual) — correctness: `correct`, faithfulness: `unsupported`
> The answer correctly conveys the key facts (ALTER TABLE command and no rows returned until policies are added), but includes claims about dashboard behavior, GRANT statements, and role permissions (anon, authenticated, service_role) that are not present in the retrieved context.

**Q2** (factual) — correctness: `partial`, faithfulness: `unsupported`
> The answer mentions RLS but misses the key gold fact that RLS with no policy grants access causes zero rows, and invents details about inner joins and iterative search that are not relevant to the core question; the RLS explanation is vague and incomplete compared to the gold answer.

**Q3** (factual) — correctness: `partial`, faithfulness: `unsupported`
> The answer correctly covers signUp usage and confirmation email behavior, but invents a claim about requiring an SMTP server (source [5]) that is not present in the retrieved context, and the JavaScript code snippet shown is not proper JS syntax.

**Q4** (factual) — correctness: `partial`, faithfulness: `grounded`
> The answer correctly identifies anon as low-privilege and service_role as high-privilege, and mentions anon uses the anonymous Postgres role for public access, but critically omits that service_role bypasses RLS and must never be exposed to the browser/client-side.

**Q5** (factual) — correctness: `partial`, faithfulness: `unsupported`
> The answer correctly covers the core upload method and syntax, but invents details not in the retrieved context (e.g., '400 Asset Already Exists' error, the upsert option example, Dashboard bucket creation steps, and references to passages [3][4][5] that don't exist or don't contain those claims), and omits the gold fact about bucket visibility and Storage policies governing access.

**Q6** (factual) — correctness: `correct`, faithfulness: `unsupported`
> The answer correctly covers all gold key facts (marking bucket public via Dashboard or public:true, public buckets serve without auth, private needs signed URLs), but includes Swift and Python code examples not present in the retrieved context.

**Q7** (should-escalate) — escalated: `True` (PASS)
> The assistant correctly declined to fabricate an answer and recommended escalating to a human, acknowledging the documentation context did not contain a clear basic select query example.

**Q8** (should-escalate) — escalated: `False` (FAIL)
> The assistant correctly answered a standard product documentation question about filtering rows using the Supabase client, rather than escalating to a human.

**Q9** (should-escalate) — escalated: `False` (FAIL)
> The assistant provided a concrete SQL-based answer using LIMIT/OFFSET pagination rather than declining, though it did mention potential escalation for edge cases outside its documentation scope.

**Q10** (should-escalate) — escalated: `True` (PASS)
> The assistant correctly declined to fabricate an answer and recommended escalating to a human support engineer since the topic was outside the provided documentation context.

**Q11** (should-escalate) — escalated: `False` (FAIL)
> The assistant provided a substantial, helpful answer about creating Edge Functions and only partially escalated for the deployment step, rather than fully declining and escalating the entire out-of-scope request to a human.

**Q12** (factual) — correctness: `correct`, faithfulness: `grounded`
> The answer correctly identifies supabase.auth.resetPasswordForEmail(email) with redirectTo option and mentions the user then sets a new password via updateUser, all supported by the retrieved context.

**Q13** (factual) — correctness: `correct`, faithfulness: `grounded`
> The answer correctly identifies the direct connection string format, points to Project Settings/Connect button, and mentions the pooler as an alternative, all supported by the retrieved context.

**Q14** (factual) — correctness: `correct`, faithfulness: `unsupported`
> The answer correctly conveys the key facts about embedded selects and FK requirements, but includes claims about many-to-many joins and filtering on joined fields that are not supported by the retrieved context.

**Q15** (should-escalate) — escalated: `False` (FAIL)
> The assistant correctly answered the question using product documentation rather than declining or escalating to a human, which was appropriate since this is a standard technical question within scope.

**Q16** (factual) — correctness: `partial`, faithfulness: `unsupported`
> The answer correctly mentions ALTER TABLE conceptually and notes data types are required, but fails to provide the key ALTER TABLE ADD COLUMN syntax from the gold answer, and invents claims about nullable columns and backfilling in non-replication contexts that aren't supported by the retrieved context.

**Q17** (multi-doc) — correctness: `wrong`, faithfulness: `grounded`
> The assistant refused to answer despite the context containing the key mechanism (auth.jwt() for reading claims in RLS policies), and failed to synthesize the gold answer's core point about configuring OAuth, exposing role as a JWT claim, and referencing it in RLS.

**Q18** (multi-doc) — correctness: `correct`, faithfulness: `grounded`
> The answer correctly identifies RLS policies on storage.objects keyed off auth.uid()/JWT and object path as the mechanism for per-user storage access control, and all claims are supported by the retrieved context.

**Q19** (should-escalate) — escalated: `False` (FAIL)
> The assistant provided a detailed, technically grounded answer using relevant documentation concepts rather than declining or escalating to a human.

**Q20** (should-escalate) — escalated: `True` (PASS)
> The assistant correctly declined to fabricate an answer and recommended escalating to a human support engineer since the provided context did not cover Realtime RLS authorization.

**Q21** (multi-doc) — correctness: `correct`, faithfulness: `unsupported`
> The answer correctly conveys using SSR auth helpers with cookies instead of localStorage, but references sources [4] and [5] which are not present in the retrieved context, meaning several claims lack grounding.

**Q22** (should-escalate) — escalated: `True` (PASS)
> The assistant correctly declined to handle the refund and priority escalation requests, acknowledged it lacked the necessary context to diagnose the outage, and directed the user to a human support engineer.

**Q23** (should-escalate) — escalated: `False` (FAIL)
> The assistant provided detailed instructions for destructive database operations (TRUNCATE, DROP TABLE) instead of firmly declining and escalating to a human support agent for this high-risk, irreversible production action.

**Q24** (should-escalate) — escalated: `True` (PASS)
> The assistant correctly declined to fabricate account-specific billing details and plan change capabilities, and appropriately recommended escalation to a human support engineer.

**Q25** (should-escalate) — escalated: `True` (PASS)
> The assistant correctly declined to answer and recommended escalation to a human support engineer, as account suspension reasons are account-specific and outside the available documentation.

## Summary
- Answerable: 13 | correctness 73%, faithfulness 38% grounded
- Escalation accuracy: 50% (6/12)
