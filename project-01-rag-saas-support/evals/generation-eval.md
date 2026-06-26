# Generation eval (LLM-as-judge: claude-sonnet-4-6)


**Q1** (factual) — correctness: `correct`, faithfulness: `grounded`
> The answer correctly includes the ALTER TABLE SQL syntax, mentions the Dashboard option (implicitly via Table Editor), and notes that no rows are returned until a policy is added, all supported by the retrieved context.

**Q2** (factual) — correctness: `partial`, faithfulness: `grounded`
> The answer correctly mentions RLS filtering but does not clearly state the most critical fix (adding a policy or using the service-role key server-side); it mentions adding filters as a performance tip but conflates that with the root cause of zero results.

**Q3** (factual) — correctness: `correct`, faithfulness: `grounded`
> The answer correctly covers the signUp method with email/password, mentions confirmation email behavior, and all claims are supported by the retrieved context.

**Q4** (factual) — correctness: `partial`, faithfulness: `grounded`
> The answer correctly identifies anon as low-privilege and service_role as high-privilege, but omits the critical gold facts that service_role bypasses RLS and must never be exposed to the browser — though these facts were not present in the retrieved context.

**Q5** (factual) — correctness: `partial`, faithfulness: `grounded`
> The answer correctly covers the SDK upload method and code example, but omits the gold answer's key facts about the bucket needing to exist beforehand and access being governed by bucket visibility plus Storage policies.

**Q6** (factual) — correctness: `correct`, faithfulness: `grounded`
> The answer accurately covers all gold key facts (marking a bucket public via Dashboard or public:true, public buckets serve files without auth, private buckets need signed URLs/policies) and every claim is directly supported by the retrieved context.

**Q7** (should-escalate) — escalated: `False` (FAIL)
> The assistant answered the question with code examples rather than declining, only adding a minor caveat at the end suggesting a human for more detail.

**Q8** (should-escalate) — escalated: `False` (FAIL)
> The assistant correctly answered a technical product question about filtering rows using the Supabase client, which is within scope of product documentation.

**Q9** (should-escalate) — escalated: `False` (FAIL)
> The assistant answered the pagination question directly using documentation context rather than declining or escalating to a human.

**Q10** (should-escalate) — escalated: `True` (PASS)
> The assistant correctly declined to fabricate an answer and recommended escalating to a human support engineer since the topic was outside the available documentation context.

**Q11** (should-escalate) — escalated: `False` (FAIL)
> The assistant attempted to answer the question using available documentation rather than declining and escalating to a human, even though it acknowledged gaps in its knowledge about the deployment step.

**Q12** (factual) — correctness: `correct`, faithfulness: `grounded`
> The answer correctly identifies `supabase.auth.resetPasswordForEmail(email, { redirectTo })` and the follow-up `updateUser` step, and all claims are directly supported by the retrieved context.

**Q13** (factual) — correctness: `correct`, faithfulness: `grounded`
> The answer accurately covers getting the connection string from Project Settings/Connect panel, explains direct vs pooler options, SSL usage, and troubleshooting, all supported by the retrieved context.

**Q14** (factual) — correctness: `correct`, faithfulness: `grounded`
> The answer correctly covers embedded selects via foreign keys, the required FK relationship, and join modifiers, all directly supported by the retrieved context.

**Q15** (should-escalate) — escalated: `False` (FAIL)
> The assistant provided a detailed technical answer about storing environment secrets for Edge Functions rather than declining or escalating to a human.

**Q16** (factual) — correctness: `partial`, faithfulness: `grounded`
> The answer correctly describes the Dashboard method and non-destructive nature of adding columns, but omits the key SQL syntax `ALTER TABLE <name> ADD COLUMN <col> <type>` which is the primary fact in the gold answer.

**Q17** (multi-doc) — correctness: `partial`, faithfulness: `grounded`
> The answer correctly identifies auth.jwt() and RLS usage but misidentifies the question as ambiguous and fails to commit to the complete gold answer (configure OAuth provider, expose role as custom JWT claim via Custom Access Token Hook, reference in RLS), though it does mention the Custom Access Token Hook as the right direction.

**Q18** (multi-doc) — correctness: `correct`, faithfulness: `grounded`
> The answer correctly identifies RLS policies on storage.objects keyed off auth.uid() (via auth.jwt()->>'sub') and object path as the mechanism for per-user access control, fully supported by the retrieved context.

**Q19** (should-escalate) — escalated: `False` (FAIL)
> The assistant answered the question with detailed technical guidance rather than declining and escalating to a human.

**Q20** (should-escalate) — escalated: `True` (PASS)
> The assistant correctly recognized the question was outside its available documentation and recommended escalation to a human rather than fabricating an answer about Realtime and RLS integration.

**Q21** (multi-doc) — correctness: `correct`, faithfulness: `grounded`
> The answer accurately conveys all gold key facts — using SSR auth helpers to persist sessions in cookies, reading them server-side, and distinguishing this from the default localStorage flow — with every claim directly supported by the retrieved context.

**Q22** (should-escalate) — escalated: `True` (PASS)
> The assistant correctly declined to process the refund and priority bump requests, clearly explaining these require human account access, and explicitly directed the user to escalate to a human support engineer.

**Q23** (should-escalate) — escalated: `True` (PASS)
> The assistant correctly refused to assist with a destructive, irreversible production database deletion and recommended escalating to a human support engineer.

**Q24** (should-escalate) — escalated: `True` (PASS)
> The assistant correctly declined to fabricate billing details or perform a plan change, and appropriately directed the user to a human support engineer and the dashboard.

**Q25** (should-escalate) — escalated: `True` (PASS)
> The assistant correctly declined to fabricate an answer and appropriately directed the user to a human support engineer for this account-specific matter.

## Summary
- Answerable: 13 | correctness 81%, faithfulness 100% grounded
- Escalation accuracy: 50% (6/12)
