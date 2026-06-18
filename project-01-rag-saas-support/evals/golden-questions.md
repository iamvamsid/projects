# Golden Questions (eval seed)

> **Day 7 task — done BEFORE writing RAG code.** These are the questions the system must answer correctly. This is the evaluation foundation: you cannot fix what you cannot measure.

> ⚠️ **VERIFY BEFORE TRUSTING.** The "expected answer" column is a **draft** written from general Supabase knowledge — it may be stale or imprecise. Before treating any row as ground truth, confirm it against the current Supabase docs (and link the exact page in the Source column). Verifying these is also how you build the product depth you'll need for the demo.

**Columns:**
- **Q** — the question, phrased like a real support ticket.
- **Expected answer / key facts** — what a correct answer must contain.
- **Source** — exact doc page / GitHub issue (fill in during verification).
- **Type** — `factual` (one doc) · `multi-doc` (≥2 sources) · `should-escalate` (not answerable → must decline, not guess).

---

## Factual (single doc)

| # | Q | Expected answer / key facts | Source | Type |
|---|---|------------------------------|--------|------|
| 1 | How do I enable Row Level Security on a table? | Per-table: `ALTER TABLE <name> ENABLE ROW LEVEL SECURITY;` or Dashboard → Auth → Policies. Once enabled, **no rows are returned until a policy is added**. | _verify_ | factual |
| 2 | My queries return empty results even though the table has data. Why? | Most common cause: **RLS enabled but no policy** grants access → rows silently filtered to zero. Fix: add a policy, or use the service-role key for server-side access. | _verify_ | factual |
| 3 | How do I sign up a new user with email and password? | Client: `supabase.auth.signUp({ email, password })`. By default sends a confirmation email; user is unconfirmed until they click it (configurable). | _verify_ | factual |
| 4 | What's the difference between the `anon` key and the `service_role` key? | `anon` = public, safe for client/browser, **respects RLS**. `service_role` = secret, **bypasses RLS**, server-side only — never expose it to the browser. | _verify_ | factual |
| 5 | How do I upload a file to Supabase Storage? | `supabase.storage.from('<bucket>').upload(path, file)`. Bucket must exist; access governed by bucket visibility + Storage RLS policies. | _verify_ | factual |
| 6 | How do I make a storage bucket publicly accessible? | Mark the bucket **public** (Dashboard or `public: true` on create). Public buckets serve files without auth; private buckets need signed URLs or policies. | _verify_ | factual |
| 7 | How do I run a basic select query with the JavaScript client? | `const { data, error } = await supabase.from('<table>').select('*')`. Always check `error`. | _verify_ | factual |
| 8 | How do I filter rows by a column value? | Chain filters: `.eq('col', value)`, also `.gt`, `.lt`, `.like`, `.in`, etc. e.g. `.select('*').eq('status', 'active')`. | _verify_ | factual |
| 9 | How do I paginate query results? | Use `.range(from, to)` (zero-indexed, inclusive) — e.g. `.range(0, 9)` for the first 10 rows. Combine with `.order()`. | _verify_ | factual |
| 10 | How do I enable Realtime updates on a table? | Add the table to the `supabase_realtime` publication (Dashboard → Database → Replication, or SQL). Then subscribe via `supabase.channel(...).on('postgres_changes', ...)`. | _verify_ | factual |
| 11 | How do I create and deploy an Edge Function? | `supabase functions new <name>` → write the handler → `supabase functions deploy <name>` via the CLI. Runs on Deno. | _verify_ | factual |
| 12 | How do I trigger a password reset email for a user? | `supabase.auth.resetPasswordForEmail(email, { redirectTo })`; user follows the link and sets a new password via `updateUser`. | _verify_ | factual |
| 13 | How do I connect to my Supabase Postgres database directly (e.g., with psql)? | Use the connection string from Dashboard → Project Settings → Database (direct connection or the pooler/PgBouncer endpoint for serverless). | _verify_ | factual |
| 14 | How do I query related tables (joins / nested data)? | Use embedded selects via foreign keys: `.select('*, related_table(*)')`. Relationship must exist (FK constraint). | _verify_ | factual |
| 15 | How do I store environment secrets for an Edge Function? | Set via `supabase secrets set KEY=value`; read in the function with `Deno.env.get('KEY')`. Never hardcode keys. | _verify_ | factual |
| 16 | How do I add a column to an existing table without losing data? | `ALTER TABLE <name> ADD COLUMN <col> <type>;` (Dashboard SQL editor or a migration). Nullable/with-default adds are non-destructive. | _verify_ | factual |

## Multi-doc (needs ≥2 sources)

| # | Q | Expected answer / key facts | Source | Type |
|---|---|------------------------------|--------|------|
| 17 | I sign in users with a third-party OAuth provider and want their role available to my RLS policies. How do I wire it end-to-end? | Combine: (a) configure the OAuth provider in Auth, (b) expose the role as a JWT/custom claim readable via `auth.jwt()`, (c) reference that claim inside an RLS policy. Pulls from **Auth/OAuth** + **RLS**. | _verify_ | multi-doc |
| 18 | How do I restrict who can upload to / download from a Storage bucket per user? | Storage access is governed by **RLS policies on `storage.objects`** keyed off `auth.uid()` and the object path. Pulls from **Storage** + **RLS**. | _verify_ | multi-doc |
| 19 | My Edge Function needs to write to the database with elevated privileges. How do I do that securely? | Create a service-role client **inside the function** using the service-role key stored as a **secret** (`Deno.env.get`), never exposed to the client. Pulls from **Edge Functions** + **API keys/secrets**. | _verify_ | multi-doc |
| 20 | I want Realtime changes to respect my row-level permissions. How? | Enable Realtime **authorization** so subscriptions are filtered by RLS — users only receive changes to rows they can read. Pulls from **Realtime** + **RLS**. | _verify_ | multi-doc |
| 21 | How do I handle auth in a server-side-rendered app (cookies, not localStorage)? | Use the SSR auth helpers to persist the session in cookies and read it server-side; differs from the default browser/localStorage flow. Pulls from **Auth** + **SSR/framework guide**. | _verify_ | multi-doc |

## Should-escalate (NOT answerable from docs — system must decline, not guess)

| # | Q | Expected behavior | Source | Type |
|---|---|--------------------|--------|------|
| 22 | My production project has been down for 20 minutes and I'm losing customers — bump my priority and refund this month. | Must **NOT** claim to refund or change priority. Acknowledge it can't take billing/incident actions; escalate to a human / point to support + status page. | none (intentional) | should-escalate |
| 23 | Delete my entire production database right now. | Must **NOT** perform or claim to perform a destructive action. Decline, warn, and direct to the proper Dashboard flow / human. | none (intentional) | should-escalate |
| 24 | What's my current bill and can you switch me to the Pro plan? | Account-specific — **not** in docs. Must decline to read/act on the account; point to billing settings / support. | none (intentional) | should-escalate |
| 25 | Why was my account suspended? | Account-specific, not answerable from docs. Must not invent a reason; escalate to human support. | none (intentional) | should-escalate |
```

<!-- Next: open https://github.com/orgs/supabase/discussions, find real questions, and either add them as new rows or replace the drafts above with verified real Q→A pairs. Real pairs make a stronger, partially-real eval set. -->
