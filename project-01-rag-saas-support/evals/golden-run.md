# Golden-question run — 2026-06-18

Ran 25 questions through `generate.answer()`. Eyeball each: correct? grounded? cited? did escalation cases decline?


---

## Q1 — `factual`
**Question:** How do I enable Row Level Security on a table?

**Top retrieval score:** 0.685  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

You can enable Row Level Security (RLS) on a table using the `enable row level security` clause in SQL [1]:

```sql
alter table "table_name" enable row level security;
```

A few important things to know:

- **Once RLS is enabled, no data will be accessible via the API when using a publishable key until you create policies** [1]. RLS works by adding the equivalent of a `WHERE` clause to every query based on the policies you define [1][4].

- **RLS must always be enabled on any tables stored in an exposed schema** (by default, the `public` schema) [4].

- **Tables created with the Table Editor in the dashboard have RLS enabled by default.** However, if you create a table using raw SQL or the SQL editor, you must remember to enable RLS yourself and grant only the permissions each Postgres role needs [4]. For example:

```sql
GRANT SELECT ON <schema_name>.<table_name> TO anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON <schema_name>.<table_name> TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON <schema_name>.<table_name> TO service_role;

alter table <schema_name>.<table_name>
enable row level security;
```
[4]

**Auto-enabling RLS for new tables:** If you want RLS enabled automatically on newly created tables, you can set up a Postgres event trigger that calls `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` after table creation [1][2]. Note that this only applies to tables created *after* the trigger is installed — existing tables still need RLS enabled manually [2].

After enabling RLS, you'll typically also want to create policies to control access to the rows [1][5].

**Sources:** row-level-security.mdx (0.68), row-level-security.mdx (0.67), column-level-security.mdx (0.63), row-level-security.mdx (0.62), row-level-security.mdx (0.61)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q2 — `factual`
**Question:** My queries return empty results even though the table has data. Why?

**Top retrieval score:** 0.354  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

There are a couple of possible causes covered in the context, depending on your situation:

1. **Row Level Security (RLS) policies / missing filters**: Policies act as "implicit where clauses," so running `select` statements without filters can be problematic. You should always add an explicit filter, e.g. `.eq('user_id', userId)`, which both helps Postgres construct a better query plan and ensures rows match your access conditions [4].

2. **Join behavior**: If your query uses joins, the type of join matters. A left join (the default) returns all parent rows but may show empty arrays for joined data that doesn't match your filter [2]. Using `!inner` filters out parent rows that don't match the joined filter, which could reduce or empty your results [5].

3. **Vector (pgvector) similarity searches with filters**: A query like `... WHERE category_id = 123 ORDER BY embedding <-> '[...]' LIMIT 5` may return fewer rows than expected (even if matching rows exist) because the embedding index may not return enough rows matching the filter. To get the exact number requested, use iterative search [3].

If none of these scenarios match your case, I don't have enough information in the provided context to diagnose the issue confidently — I'd recommend escalating to a human support engineer with details about your specific query, table, and RLS setup.

**Sources:** arrays.mdx (0.35), joins-and-nesting.mdx (0.35), pgvector.mdx (0.35), row-level-security.mdx (0.35), joins-and-nesting.mdx (0.35)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q3 — `factual`
**Question:** How do I sign up a new user with email and password?

**Top retrieval score:** 0.517  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

To sign up a new user with email and password, you use the sign-up method provided by your SDK. Note that email authentication is enabled by default in Supabase [3].

Here are examples for different languages:

**JavaScript** — call `signUp()`:
```js
const { data, error } = await supabase.auth.signUp({
  email: 'valid.email@supabase.io',
  password: 'example-password',
})
```
(Inferred from the sign-up usage pattern; see [1] for the related sign-in example.)

**Kotlin** — call `signUpWith(Email)` [1]:
```kotlin
suspend fun signUpNewUser() {
	supabase.auth.signUpWith(Email) {
		email = "valid.email@supabase.io"
		password = "example-password"
	}
}
```

**Python** — call `sign_up()` [1]:
```python
data = supabase.auth.sign_up({
  'email': 'valid.email@supabase.io',
  'password': 'example-password',
})
```

A few important details to keep in mind:

- There are two possible signup flows: the **implicit flow** and the **PKCE flow**. If you're using SSR, you'll use the PKCE flow. For client-only code, the default depends on the library (implicit flow is the default in JavaScript and Dart; PKCE is the default in Swift) [3].
- On hosted Supabase projects, **email confirmation is required by default**, so the user will need to verify their email before signing in. You can configure this on the Auth Providers page (hosted) or in the configuration file (self-hosted/local) [3].
- The signup confirmation flow requires an SMTP server to send emails. Supabase provides a default email service for testing (with a rate limit), but you should configure a custom SMTP server for production [5].

If you need the exact JavaScript `signUp()` snippet or details about a specific SDK not fully shown here, I'd recommend checking the linked SDK reference docs or escalating to a human support engineer.

**Sources:** passwords.mdx (0.52), auth-email-passwordless.mdx (0.51), passwords.mdx (0.49), passwords.mdx (0.48), passwords.mdx (0.48)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q4 — `factual`
**Question:** What's the difference between the `anon` key and the `service_role` key?

**Top retrieval score:** 0.518  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

I don't have enough information to fully and confidently answer this question.

The context explains some things about the `anon` and `service_role` keys, but it does not provide a clear, direct comparison of the difference between them. Here's what the passages do say:

- Both `anon` and `service_role` are not just API keys but are also valid JSON Web Tokens (JWTs) signed by the legacy JWT secret [2].
- They map to different privilege levels: `anon` is described as "low privilege" and `service_role` as "high privilege" [2].
- The `anon` API key does not create a user and can be used to implement public access to your database, as it uses the `anonymous` Postgres role [1].
- Separately, the `anon` Postgres role corresponds to an unauthenticated request (user not logged in), while authenticated requests use the `authenticated` role [3].

However, the context does not give a complete description of the `service_role` key's specific purpose and behavior (e.g., that it bypasses RLS), so I can't fully answer the difference between the two keys.

I'd recommend escalating to a human support engineer for a complete and accurate explanation of how these two keys differ in practice.

**Sources:** auth-anonymous.mdx (0.52), signing-keys.mdx (0.52), row-level-security.mdx (0.46), signing-keys.mdx (0.45), auth-anonymous.mdx (0.45)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q5 — `factual`
**Question:** How do I upload a file to Supabase Storage?

**Top retrieval score:** 0.714  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

There are a few ways to upload a file to Supabase Storage, depending on the file size and your needs:

## 1. Standard Upload (best for small files)

For small files (up to 6MB recommended, though up to 5GB is supported), use the standard upload method with the supabase-js SDK using `multipart/form-data` format [2]. For example, in JavaScript:

```javascript
// Create Supabase client
const supabase = createClient('your_project_url', 'your_supabase_api_key')

// Upload file using standard upload
async function uploadFile(file) {
  const { data, error } = await supabase.storage.from('bucket_name').upload('file_path', file)
  if (error) {
    // Handle error
  } else {
    // Handle success
  }
}
```

The SDK also supports Dart, Swift, Kotlin, Python, and cURL [2][3]. For files larger than 6MB, TUS Resumable Upload is recommended for better reliability [2].

### Overwriting existing files
By default, uploading to an existing path returns a `400 Asset Already Exists` error. To overwrite, set `upsert` to `true` (or use the `x-upsert` header) [3][5]:

```javascript
await supabase.storage.from('bucket_name').upload('file_path', file, {
  upsert: true,
})
```

## 2. S3 Protocol Upload

You can also use the S3 protocol [1]:

- **Single request (`PutObject`)** — ideal for smaller files where retrying the whole upload isn't an issue. Max file size on paid plans is 500 GB [1].
- **Multipart Upload** — splits the file into parts and uploads them in parallel, maximizing speed and allowing retries of individual parts. This is preferable for server-side uploads of large files. Max file size on paid plans is 500 GB [1].

See the [S3 setup guide](/docs/guides/storage/s3/authentication) to get started with S3 [1].

## Before you upload

You'll need a bucket to upload into. Buckets are distinct containers for your files and folders, which you can create via the Dashboard, SQL, or client libraries [4]. Note that file, folder, and bucket names must follow AWS object key naming guidelines [4].

If you'd like guidance on resumable (TUS) uploads specifically, the context only references them but doesn't include the detailed steps here — let me know and I can help you find that, or escalate to a human support engineer.

**Sources:** s3-uploads.mdx (0.71), standard-uploads.mdx (0.70), standard-uploads.mdx (0.67), quickstart.mdx (0.67), standard-uploads.mdx (0.66)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q6 — `factual`
**Question:** How do I make a storage bucket publicly accessible?

**Top retrieval score:** 0.595  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

You can make a storage bucket publicly accessible by setting it as a **public** bucket. When a bucket is designated as 'Public,' it bypasses access controls for retrieving and serving files, so anyone with the asset URL can access the file [1].

You can create a public bucket in a few ways:

**Using the JavaScript library**, pass `public: true` when creating the bucket [3]:
```js
const { data, error } = await supabase.storage.createBucket('avatars', {
  public: true, // default: false
})
```

**Using SQL**, set the `public` column to `true` [3]:
```sql
insert into storage.buckets
  (id, name, public)
values
  ('avatars', 'avatars', true);
```

**Using the Dashboard**, go to the Storage page, click **New Bucket**, enter a name, and create it [3] (you can configure the public option there as well).

Other SDKs support this too — for example, Swift uses `BucketOptions(public: true)` and Python uses `options={"public": True}` [5].

A couple of notes:
- Buckets are **private by default**, so you must explicitly enable public access [1].
- Even for public buckets, access control is still enforced for operations like uploading, deleting, moving, and copying [1].
- Public buckets are also more performant than private buckets because they are cached differently [1].

**Sources:** fundamentals.mdx (0.60), access-control.mdx (0.55), creating-buckets.mdx (0.55), quickstart.mdx (0.53), creating-buckets.mdx (0.51)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q7 — `factual`
**Question:** How do I run a basic select query with the JavaScript client?

**Top retrieval score:** 0.456  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

I don't have enough information to answer this question confidently. The context passages show examples of more specialized queries—such as querying JSON data [1], full-text search [2][3][4], and creating Supabase clients [5]—but none of them demonstrate a *basic* select query with the JavaScript client on its own.

The closest examples involve `.select()` combined with additional methods like `.textSearch()` (e.g., `supabase.from('books').select().textSearch('description', "'big'")` [3]), but these don't isolate the basic select operation you're asking about.

I'd recommend escalating to a human support engineer, who can point you to the correct documentation for performing a simple select query with the JavaScript client.

**Sources:** json.mdx (0.46), full-text-search.mdx (0.46), full-text-search.mdx (0.42), full-text-search.mdx (0.42), creating-a-client.mdx (0.42)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q8 — `factual`
**Question:** How do I filter rows by a column value?

**Top retrieval score:** 0.368  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

To filter rows by a column value, you can use filter methods like `eq` (equals), `neq` (not equals), and `in` on your query [4].

For example, using the JavaScript client, you add a `.eq()` filter specifying the column name and the value you want to match:

```js
const { data } = supabase
  .from('table')
  .select()
  .eq('user_id', userId)
```

This filters the rows so only those where `user_id` matches the given value are returned [3].

For filtering using fields from a joined table, you reference the column with the format `joined_table.column` in your filter—for example:

```js
const { data, error } = await supabase
  .from('instruments')
  .select(`
    id,
    name,
    orchestral_sections!inner ( id, name )
  `)
  .eq('orchestral_sections.name', 'woodwinds')
```

This filters based on a column in the joined table [4].

As a performance note, adding explicit filters to your queries (rather than relying solely on RLS policies) is recommended, since Postgres can use the filter to build a better query plan [3].

**Sources:** column-level-security.mdx (0.37), row-level-security.mdx (0.37), row-level-security.mdx (0.36), joins-and-nesting.mdx (0.35), pg_plan_filter.mdx (0.34)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q9 — `factual`
**Question:** How do I paginate query results?

**Top retrieval score:** 0.333  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

Based on the context, you can paginate query results using `LIMIT` and `OFFSET` in your SQL query [5].

For example:

```sql
order by key asc
limit 100 offset 0;
-- To paginate, increase OFFSET for next page:
-- OFFSET 100 for page 2, OFFSET 200 for page 3, etc.
```

The approach is to set a fixed `LIMIT` (e.g., 100 rows per page) and increase the `OFFSET` for each subsequent page — `OFFSET 100` for page 2, `OFFSET 200` for page 3, and so on [5].

If you need pagination guidance for a more specific scenario (such as with a particular client SDK or another type of query), the context doesn't cover those cases in detail, and I'd recommend escalating to a human support engineer for further help.

**Sources:** full-text-search.mdx (0.33), pgvector.mdx (0.32), full-text-search.mdx (0.32), full-text-search.mdx (0.31), querying-vectors.mdx (0.31)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q10 — `factual`
**Question:** How do I enable Realtime updates on a table?

**Top retrieval score:** 0.457  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

I don't have enough information to answer this question confidently. The provided context covers topics like materialized views [1], enabling Row Level Security (RLS) [2][5], replica identity for logical replication [3][4], and BigQuery table structures [4] — but none of these passages explain how to enable **Realtime updates** on a table.

I'd recommend escalating this to a human support engineer, or consulting the Supabase Realtime documentation directly for accurate guidance.

**Sources:** tables.mdx (0.46), row-level-security.mdx (0.45), external-replication-faq.mdx (0.42), bigquery.mdx (0.42), row-level-security.mdx (0.42)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q11 — `factual`
**Question:** How do I create and deploy an Edge Function?

**Top retrieval score:** 0.454  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

Based on the context provided, I can share part of the process for creating an Edge Function, but not a complete create-and-deploy workflow.

**Creating an Edge Function:**

To create a new edge function, you use the Supabase CLI:

```bash
supabase functions new <function-name>
```

For example, `supabase functions new before-user-created-hook` [2][5] or `supabase functions new send-email` [4].

You then add your code to the edge function. The code is written in TypeScript/JavaScript and typically uses `Deno.serve()` to handle incoming requests [2][4][5].

You can also set any required secrets for your project using:

```bash
supabase secrets set --env-file .env
```
[2][4][5]

**Deploying an Edge Function:**

Unfortunately, the provided context does not include the specific command or steps to **deploy** an Edge Function (i.e., pushing it live). I don't have enough information to confidently explain the deployment step.

I'd recommend escalating to a human support engineer for the exact deployment instructions, or consulting the Supabase Edge Functions documentation directly.

For reference, the context does note that Edge Functions are "globally-distributed and can be written in Typescript" and are recommended for use-cases requiring low-latency [1].

**Sources:** functions.mdx (0.45), before-user-created-hook.mdx (0.40), functions.mdx (0.38), send-email-hook.mdx (0.38), before-user-created-hook.mdx (0.37)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q12 — `factual`
**Question:** How do I trigger a password reset email for a user?

**Top retrieval score:** 0.530  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

To trigger a password reset email for a user, you call the reset password by email function with the user's email address. The exact method depends on your SDK [1]:

**JavaScript:**
```js
async function resetPassword() {
  const { data, error } = await supabase.auth.resetPasswordForEmail(email)
}
```

**Swift:**
```swift
try await supabase.auth.resetPasswordForEmail("valid.email@supabase.io")
```

**Kotlin:**
```kotlin
supabase.gotrue.sendRecoveryEmail(
    email = "valid.email@supabase.io",
)
```

**Python:**
```python
supabase.auth.reset_password_email('valid.email@supabase.io')
```

**Dart:**
```dart
await supabase.auth.resetPasswordForEmail('valid.email@supabase.io');
```

(All from [1].)

When initiating the reset, you should typically specify a redirect URL that points to a **change password** page. This URL needs to be configured in your redirect URLs [3]. For example:

**Python:**
```python
client.auth.reset_password_email(
  'valid.email@supabase.io',
  {'redirect_to':'http://example.com/account/update-password'}
)
```

**Dart:**
```dart
await supabase.auth.resetPasswordForEmail(
  'valid.email@supabase.io',
  redirectTo: 'http://example.com/account/update-password',
);
```
(Both from [2].)

The overall flow is:
1. Create a publicly accessible **reset password** page where you collect the user's email and request the reset email [3].
2. Create a **change password** page (accessible only to authenticated users) where you collect the new password and call `updateUser` to update it [1][2].

Note that the implicit flow provides the access token directly after the user clicks the confirmation link, while the PKCE flow requires an intermediate token exchange step before you can get the access token [2].

**Sources:** passwords.mdx (0.53), passwords.mdx (0.52), passwords.mdx (0.51), password-verification-hook.mdx (0.48), auth-email-templates.mdx (0.47)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q13 — `factual`
**Question:** How do I connect to my Supabase Postgres database directly (e.g., with psql)?

**Top retrieval score:** 0.669  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

To connect directly to your Supabase Postgres database (e.g., with a Postgres client like psql), here's what you need to know:

## Getting your connection string

Use the **direct connection string** for single sessions or Postgres native commands like database GUIs, `pg_dump`, migrations, or backup-restore [5]. You can get it from your project dashboard by clicking the **Connect** button at the top of the page [1][2].

The direct connection string looks like this [2]:

```
postgresql://postgres:[YOUR-PASSWORD]@db.abcdefghijklmnopqrst.supabase.co:5432/postgres
```

The direct connection uses port `5432` [4].

## Connecting with SSL (recommended)

You should connect using SSL wherever possible to prevent snooping and man-in-the-middle attacks [3]. You can obtain your connection info and Server root certificate from your dashboard [3].

For `psql` specifically, download your SSL certificate, then use a connection string like this (note this example uses the Session pooler host) [3]:

```shell
psql "sslmode=verify-full sslrootcert=/path/to/prod-supabase.cer host=[CLOUD_PROVIDER]-0-[REGION].pooler.supabase.com dbname=postgres user=postgres.[PROJECT_REF]"
```

## Important note about IPv4 vs. IPv6

Direct connections are on **IPv6** by default, or on IPv4 if your project has the [IPv4 add-on](/docs/guides/platform/ipv4-address) [2]. **If your network is IPv4-only and you don't have the add-on**, you should use [pooler session mode](#pooler-session-mode) instead, which is IPv4-only and available on every project tier [1][2].

Let me know if you'd like guidance on setting up the pooler session connection instead!

**Sources:** connecting-to-postgres.mdx (0.67), connecting-to-postgres.mdx (0.64), psql.mdx (0.61), connecting-to-postgres.mdx (0.59), connecting-to-postgres.mdx (0.58)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q14 — `factual`
**Question:** How do I query related tables (joins / nested data)?

**Top retrieval score:** 0.547  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

Supabase's data APIs automatically detect relationships between Postgres tables, so you can query related/nested data directly in your `select` statement [4].

## Basic nested select (one-to-many)

You can embed a related table by nesting it inside your select. For example, with `orchestral_sections` and `instruments` tables [4]:

```js
supabase.from('orchestral_sections').select('id, name, instruments(id, name)')
```

This works across SDKs — for example in Python:

```python
data = supabase.from_('orchestral_sections').select('id, name, instruments(id, name)').execute()
```

Or via the URL/REST API [1]:

```
GET https://[REF].supabase.co/rest/v1/orchestral_sections?select=id,name,instruments(id,name)
```

## Join types

By default, embedded relations use **left join** semantics from the parent table [1][2]:

- Parent rows are returned even if no related rows match.
- The embedded relation is `[]` for one-to-many joins and `null` for many-to-one joins when nothing matches.

To filter out parent rows that don't have a matching related row, use `!inner` on the embedded relation [2].

## Join syntax modifiers

| Syntax | Meaning | Example |
| --- | --- | --- |
| `alias:relation(columns)` | Rename the embedded relation in the response | `start_scan:scans(id, badge_scan_time)` |
| `relation!inner(columns)` | Use inner join behavior | `instruments!inner(id, name)` |
| `relation!foreign_key(columns)` | Choose which foreign key to use when multiple match | `scans!scan_id_start(id)` |

(See [2][3].)

You can also filter on joined fields. For example, to return only instruments in the woodwinds section [5]:

```
?select=id,name,orchestral_sections!inner(id,name)&orchestral_sections.name=eq.woodwinds
```

## Many-to-many joins

The data APIs also detect many-to-many relationships. For example, with `users`, `teams`, and a joining `members` table, you can fetch all teams and their members **without explicitly referencing the joining table** [5]:

```js
const { data, error } = await supabase.from('teams').select(`
  id,
  team_name,
  users ( id, name )
`)
```

Let me know if you need an example for a specific SDK (JavaScript, Swift, Kotlin, Python, Dart, or GraphQL) — the context includes several of those variations.

**Sources:** joins-and-nesting.mdx (0.55), joins-and-nesting.mdx (0.53), joins-and-nesting.mdx (0.52), joins-and-nesting.mdx (0.51), joins-and-nesting.mdx (0.50)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q15 — `factual`
**Question:** How do I store environment secrets for an Edge Function?

**Top retrieval score:** 0.443  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

To store environment secrets for an Edge Function in your Supabase project, you can use a `.env` file and then set the secrets with the Supabase CLI.

1. Create a `.env` file with your environment variables. For example:

```ini
BEFORE_USER_CREATED_HOOK_SECRET="v1,whsec_<base64_secret>"
```

You can generate the secret in the Auth Hooks section of the Supabase dashboard [5].

2. Set the secrets in your Supabase project using the CLI:

```bash
supabase secrets set --env-file .env
```

This command is the standard way to load your environment secrets into your project [1][2][3][5].

Once set, you can access these secrets inside your Edge Function using `Deno.env.get('YOUR_SECRET_NAME')` [1][2][5].

**Sources:** before-user-created-hook.mdx (0.44), send-email-hook.mdx (0.44), before-user-created-hook.mdx (0.43), signing-keys.mdx (0.42), before-user-created-hook.mdx (0.42)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q16 — `factual`
**Question:** How do I add a column to an existing table without losing data?

**Top retrieval score:** 0.468  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

The context confirms that you can add and remove columns at any time after creating a table [1]. You can do this either through the Dashboard or with SQL [1]:

- **Dashboard:** Go to the Table Editor, click **New Column**, give it a name and data type, then click **Save** [1].
- **SQL:** When adding a column you must define its data type, since every column requires a predefined type [1].

A couple of additional considerations from the context:

- If you're adding a column with column-level privileges, be aware that turning off a column privilege means you won't be able to use that column at all [2].
- The context only directly discusses the BigQuery replication scenario regarding existing data: there, added columns must be nullable, and if you add a column with a default, BigQuery does not backfill existing rows — they remain `NULL` unless you run a separate backfill [3]. This is specific to BigQuery ETL replication.

For a standard Postgres table in Supabase, adding a column is a non-destructive operation, so your existing data in other columns is preserved [1].

However, the provided context does not give a detailed, general explanation of the exact `ALTER TABLE ... ADD COLUMN` SQL syntax or guarantees about data preservation for the general case beyond what's noted above. If you need specifics about adding a column with defaults or constraints on a large existing table without impacting data, I'd recommend escalating to a human support engineer for confirmation.

**Sources:** tables.mdx (0.47), column-level-security.mdx (0.42), bigquery.mdx (0.41), prisma-troubleshooting.mdx (0.39), tables.mdx (0.39)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q17 — `multi-doc`
**Question:** I sign in users with a third-party OAuth provider and want their role available to my RLS policies. How do I wire it end-to-end?

**Top retrieval score:** 0.554  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

I don't have enough information to answer this confidently.

An important clarification: the context here covers **Supabase acting as the OAuth 2.1 authorization server** — that is, how third-party applications (OAuth *clients*) access your users' data, and how to use the `client_id` claim in RLS policies [3]. It explains that OAuth access tokens are JWTs with standard Supabase claims plus a `client_id` claim, and that you can read claims in RLS via `auth.jwt()` (e.g., `auth.jwt() ->> 'client_id'`) [1][3].

However, your question is about **signing users in with a third-party OAuth provider** (an inbound social/identity provider login) and surfacing a custom **role** claim into your RLS policies end-to-end. The provided passages don't cover:

- Configuring an external OAuth identity provider for sign-in,
- Extracting/mapping a `role` from the provider's token into the Supabase JWT,
- The full end-to-end wiring to make a custom role available in RLS.

The passages do hint at a relevant building block — the "Custom Access Token Hooks" doc for injecting custom claims [4] — but the actual steps aren't included in this context, so I can't responsibly detail them here.

I'd recommend escalating to a human support engineer, and in the meantime reviewing the linked resources referenced in the docs: the Custom Access Token Hooks guide and the JWTs guide [4].

**Sources:** token-security.mdx (0.55), token-security.mdx (0.54), token-security.mdx (0.53), token-security.mdx (0.50), token-security.mdx (0.50)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q18 — `multi-doc`
**Question:** How do I restrict who can upload to / download from a Storage bucket per user?

**Top retrieval score:** 0.584  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

You can restrict per-user uploads and downloads in Supabase Storage using Postgres Row Level Security (RLS) policies on the `storage.objects` table. By default, Storage does not allow any uploads to buckets without RLS policies, so you must selectively grant operations by creating policies [4].

## Restricting uploads per user

To allow authenticated users to upload files only to a folder named with their own user ID inside a bucket, you can use a policy like this [5]:

```sql
create policy "Allow authenticated uploads"
on storage.objects
for insert
to authenticated
with check (
  bucket_id = 'my_bucket_id' and
  (storage.foldername(name))[1] = (select auth.jwt()->>'sub')
);
```

This ties uploads to a folder matching the user's ID (`sub` claim from the JWT), so each user can only upload into their own folder [5].

## Restricting downloads per user

To allow a user to access (download/select) only files they previously uploaded, you can use the `owner_id` field [5]:

```sql
create policy "Individual user Access"
on storage.objects for select
to authenticated
using ( (select auth.jwt()->>'sub') = owner_id );
```

## Important notes

- **Use a private bucket.** Per-user access control only applies to private buckets, since RLS governs all operations including downloads. Public buckets bypass access controls for retrieving/serving files — anyone with the asset URL can access it [1].
- **For downloads in a private bucket**, you must either use the `download` method with the user's JWT in the authorization header (so the RLS policy can evaluate the user), or generate a signed URL with `createSignedUrl` for time-limited access [1].
- **For overwriting files** via `upsert`, you'll additionally need to grant `SELECT` and `UPDATE` permissions, not just `INSERT` [4].

To craft and simplify these policies, you can use Supabase's storage [helper functions](/docs/guides/storage/schema/helper-functions) [4].

**Sources:** fundamentals.mdx (0.58), access-control.mdx (0.52), creating-buckets.mdx (0.52), access-control.mdx (0.51), access-control.mdx (0.49)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q19 — `multi-doc`
**Question:** My Edge Function needs to write to the database with elevated privileges. How do I do that securely?

**Top retrieval score:** 0.454  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

Based on the context, here's how to securely give your Edge Function elevated database privileges:

**Use a secret/service role key inside the Edge Function (never on the frontend).** Edge Functions are designed to put custom server-side logic between your client and database, and you can safely use secrets, API keys, or database connection strings inside them [2]. Your secret and service role keys bypass RLS, so they should **only** be used on the backend—which an Edge Function is. Treat them as secrets, for example by importing them as sensitive environment variables rather than hardcoding them [3].

A couple of important related points from the context:

- The service role / secret keys are what grant elevated, RLS-bypassing access, so they are the right tool when your function needs to write with elevated privileges—just keep them strictly server-side [3].
- If your application accesses data only through Edge Functions, you can also consider disabling the Data API to reduce your attack surface [2].

**A note on alternatives:** The context also mentions `security definer` database functions, which run with the privileges of the function's creator (and can have `bypassrls` if created by a superuser like `postgres`) [5]. These can be a secure way to perform privileged operations from the database side. If you use one, be sure to set the `search_path` (e.g. `search_path = ''`, stating the schema explicitly for every relation) [1], and never create security-definer functions in a schema listed in your "Exposed schemas" API settings [5].

**Caveat:** The context covers the general security principles (where to use secret keys, server-side only) but does not give a step-by-step example of wiring up a service-role Supabase client *inside* an Edge Function specifically. If you'd like exact code for initializing the client with the service role key in an Edge Function, I don't have enough detail in these passages to show that confidently—I'd recommend escalating to a human support engineer for the precise implementation.

**Sources:** functions.mdx (0.45), secure-data.mdx (0.45), secure-data.mdx (0.42), functions.mdx (0.42), row-level-security.mdx (0.41)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q20 — `multi-doc`
**Question:** I want Realtime changes to respect my row-level permissions. How?

**Top retrieval score:** 0.522  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

I don't have enough information in the provided context to confidently answer how to make Realtime changes respect your row-level permissions.

The passages cover Row Level Security (RLS) concepts, enabling RLS, writing policies, column-level privileges, and bypassing RLS [1][2][3][4][5], but none of them specifically address how RLS interacts with Supabase Realtime or how to configure Realtime to respect row-level permissions.

I'd recommend escalating this to a human support engineer who can provide accurate guidance on Realtime authorization.

**Sources:** column-level-security.mdx (0.52), row-level-security.mdx (0.52), row-level-security.mdx (0.50), row-level-security.mdx (0.50), row-level-security.mdx (0.49)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q21 — `multi-doc`
**Question:** How do I handle auth in a server-side-rendered app (cookies, not localStorage)?

**Top retrieval score:** 0.572  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

# Handling Auth in a Server-Side-Rendered App

For SSR, you need to store auth tokens in cookies rather than local storage, since local storage isn't accessible by the server. Here's how it works:

## Why cookies instead of localStorage

When a user authenticates with Supabase Auth, two pieces of information are issued:
1. An **access token** (a JWT)
2. A **refresh token** (a randomly generated string)

The default behavior when not using SSR is to store these in local storage, but since local storage isn't accessible to the server, SSR requires storing the tokens in a secure cookie that can be passed back and forth between your client and server code [4].

## Use the PKCE flow

If you're not using SSR, you might be using the implicit flow, but the server can't access tokens in that flow. For SSR, you should switch to the **PKCE flow** [4].

The good news: the `@supabase/ssr` package initiates clients using the PKCE flow by default, and automatically handles saving and retrieving session information in cookies [4].

## How it works

In the PKCE flow, a redirect is made to your app with an Auth Code in the URL. When you exchange this code using `exchangeCodeForSession`, you receive the session information containing the access and refresh tokens. These must be stored in a storage medium securely shared between client and server (traditionally cookies), and updated whenever the session is refreshed [4].

## Important considerations

**Caching / CDN / ISR:** If your app uses ISR or sits behind a CDN, be careful—caching of HTTP responses with `Set-Cookie` headers can cause a user to receive another user's session [1][2]. Recommendations:
- Don't enable ISR on any route where authentication or session refresh occurs [2].
- In Next.js, use `export const dynamic = 'force-dynamic'` on authenticated pages; in Nuxt, avoid setting `isr` on authenticated routes [2].

**HttpOnly cookies:** Making cookies `HttpOnly` is generally not necessary, since the browser side of your app needs access to the refresh token to maintain the session [3]. Fully HTTP-only cookies are only feasible for traditional server-only apps that return rendered HTML and use no client-side JavaScript [5].

**Cookie expiration:** When using cookies, set the `Expires` or `Max-Age` attributes far into the future and let Supabase Auth control token validity, rather than setting short values (which degrades UX) [3][5].

**SameSite:** A good default is `Lax`, which sends cookies when users navigate to your site. Cookies typically need the `Secure` attribute (HTTPS only), which can complicate local development [2].

For framework-specific examples and deeper detail, see the [advanced Auth server-side rendering guide](/docs/guides/auth/server-side/advanced-guide) [1].

Let me know which framework you're using if you'd like more specific guidance.

**Sources:** creating-a-client.mdx (0.57), advanced-guide.mdx (0.56), advanced-guide.mdx (0.56), advanced-guide.mdx (0.56), sessions.mdx (0.53)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q22 — `should-escalate`
**Question:** My production project has been down for 20 minutes and I'm losing customers — bump my priority and refund this month.

**Top retrieval score:** 0.321  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

I'm sorry your project is experiencing downtime — I understand the urgency. However, I don't have enough information in the provided context to address your specific requests:

- **Bumping priority / billing refunds** are not covered in the context passages available to me, so I can't action or promise those here.
- The context I have relates to external replication (ETL) monitoring and behavior, not general project outages or support prioritization.

I'd strongly recommend escalating this to a human support engineer immediately so they can investigate the outage and review your priority and billing requests.

If it's relevant, one thing I can note: if your project recently became inactive or was restarted, external replication pipelines do **not** resume automatically and must be restarted manually from **Database > Replication** in the Dashboard [4]. But this is only applicable if replication is part of your issue.

For the outage itself, refund, and priority change, please escalate to human support right away.

**Sources:** external-replication-monitoring.mdx (0.32), external-replication-faq.mdx (0.31), auth-smtp.mdx (0.31), external-replication-faq.mdx (0.31), external-replication-monitoring.mdx (0.30)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q23 — `should-escalate`
**Question:** Delete my entire production database right now.

**Top retrieval score:** 0.447  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

I want to be careful here, because "delete my entire production database" is a high-risk operation, and the context I have doesn't describe a single command to delete an entire database. Let me share what the documentation does cover, along with important safety guidance.

## Important precautions first

Before running any destructive operation on a live/production database, the docs strongly recommend [1]:

- **Test in a staging environment** first
- **Ensure you have a recent backup** [1][5]
- Confirm table dependencies and foreign key constraints
- Choose a **low-traffic time** to run the operation
- Run operations inside a [migration](/docs/guides/deployment/database-migrations)
- Set `lock_timeout` and `statement_timeout` [1]

These matter especially in production, since deletes and drops can lock tables, block queries, and cause downtime [1].

## What the docs do cover

**Deleting all data from a table** — use `TRUNCATE`, which is faster than `DELETE` and also resets auto-incrementing sequences [2]:
```sql
truncate table logs;
```

**Dropping a single table** — always use `IF EXISTS`; note this acquires an `ACCESS EXCLUSIVE` lock that blocks all other operations [3]:
```sql
drop table if exists old_analytics;
```

**Dropping all tables in a schema** — the closest thing to "wiping" your data. This loops through and drops every table in a schema [5]:
```sql
do $$ declare
    r record;
begin
    for r in (select tablename from pg_tables where schemaname = 'my-schema-name') loop
        execute 'drop table if exists ' || quote_ident(r.tablename) || ' cascade';
    end loop;
end $$;
```
The docs explicitly caution: **this deletes all tables and their associated data — ensure you have a recent backup before proceeding** [5].

## My recommendation

The context does **not** contain a procedure for deleting an *entire database* (as opposed to dropping data/tables within a schema), and given the irreversible, production-impacting nature of this request, I don't want to guess.

Please confirm you have a verified, recent backup [1][5], and I'd strongly recommend **escalating to a human Supabase support engineer** before performing any full-database deletion on production.

**Sources:** data-deletion.mdx (0.45), data-deletion.mdx (0.45), data-deletion.mdx (0.38), data-deletion.mdx (0.37), dropping-all-tables-in-schema.mdx (0.36)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q24 — `should-escalate`
**Question:** What's my current bill and can you switch me to the Pro plan?

**Top retrieval score:** 0.298  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

I don't have enough information to answer your question confidently. The context passages cover topics like storage pricing [1], analytics buckets [2], bandwidth/egress limits [3], and various Postgres tooling [4][5] — but none of them provide access to your current account billing details or a way to change your subscription plan.

For account-specific actions like viewing your current bill or upgrading to the Pro plan, I'd recommend escalating to a human support engineer who can access your account directly.

**Sources:** pricing.mdx (0.30), pricing.mdx (0.29), bandwidth.mdx (0.28), pg_plan_filter.mdx (0.28), inspect.mdx (0.26)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_


---

## Q25 — `should-escalate`
**Question:** Why was my account suspended?

**Top retrieval score:** 0.315  _(low score on a `should-escalate` = good; low score on a `factual` = retrieval miss)_

**Answer:**

I don't have enough information to answer your question confidently. The provided context covers topics like configuring custom SMTP, protecting your email sending reputation from abuse, email templates, and various error codes — but none of it explains why a specific account might be suspended.

I'd recommend escalating this to a human support engineer, who can look into the specifics of your account and provide an accurate answer.

**Sources:** auth-smtp.mdx (0.31), auth-smtp.mdx (0.27), error-codes.mdx (0.27), auth-email-templates.mdx (0.26), auth-email-templates.mdx (0.25)

**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_
