# Internship Watcher

Emails you the moment a new **Summer 2027 embedded software / ML / SWE
internship** opens, and sends a weekly digest of competitions, fellowships and
research programs whose applications just opened.

It runs entirely on GitHub's servers for free. Your computer can be off.

- **Every hour** — checks ~166 sources (company job boards, plus ~270 more
  auto-discovered from community trackers) and emails only what's *new*
- **Sundays 10am ET** — a digest of programs and scholarships whose pages changed

Roles are ranked: **embedded / firmware / robotics** first, **ML / AI / CV**
second, **general software engineering** as a fallback tier.

---

## Setup

Roughly 15 minutes, all point-and-click. Do these in order.

### 1. Get a Gmail App Password

The watcher sends email through Gmail. Your normal password will not work —
Google blocks that.

1. Go to <https://myaccount.google.com/apppasswords>
2. If the page says it isn't available, turn on 2-Step Verification first at
   <https://myaccount.google.com/security>, then come back
3. Name it anything (`internship watcher`), click **Create**
4. Copy the 16-character code it shows. **It is shown only once.** Delete the
   spaces, so `abcd efgh ijkl mnop` becomes `abcdefghijklmnop`

### 2. Add the secrets

In this repo: **Settings** → **Secrets and variables** → **Actions** →
**New repository secret**. Add all three. Names must match exactly.

| Name | Value |
|---|---|
| `SMTP_USERNAME` | the Gmail address it sends *from* |
| `SMTP_PASSWORD` | the 16-character App Password from step 1 |
| `EMAIL_TO` | the address that should receive the alerts |

Optional but worth it — this unlocks NASA, DOE national labs, NSA and Navy
postings, which is where a lot of embedded and autonomy work lives. Get a free
key at <https://developer.usajobs.gov/apirequest/> and add:

| Name | Value |
|---|---|
| `USAJOBS_API_KEY` | the key they email you |
| `USAJOBS_EMAIL` | the address you registered with |

### 3. Check the sources are alive

**Actions** tab → **Watcher** in the left sidebar → **Run workflow** → set
**What to run** to `verify` → green **Run workflow**.

This takes about a minute and does two things: probes every source and reports
which are broken, and runs the filter tests.

Why it matters: a mistyped job-board address doesn't crash anything — it just
silently returns zero jobs forever, which looks exactly like "nothing is open".
This is the only way to tell the difference.

Read the `DEAD` list and delete those entries from `config.json`. **Ignore the
`EMPTY` list** — that just means a company has no openings right now.

### 4. Run it for real

**Run workflow** again with **What to run** set to `internships`.

Takes a few minutes. You should get an email titled
`[Internship Watcher] Baseline: N open role(s)` listing everything currently
open that matches. **Check your spam folder the first time** — mail you send to
yourself often lands there.

After that first email, you only hear about genuinely new postings.

---

## Things that will bite you eventually

**GitHub disables scheduled workflows after 60 days of no repository activity.**
It emails a warning first, and re-enabling is one button in the Actions tab. But
if you stop getting emails and nothing looks broken, check this first. The risk
window is the quiet stretch after recruiting season ends.

**Scheduled runs can be late or skipped.** GitHub's hourly scheduling is
best-effort, not a guarantee. Nothing is lost — the next run catches whatever
the skipped one would have found.

**Recruiting is seasonal.** August through January is busy; expect near-silence
outside that. A quiet inbox in May is the system working, not a broken filter.
Check the run log's `Filter drops this run:` line to confirm postings are being
seen and rejected for sensible reasons rather than not fetched at all.

---

## Changing what it looks for

Almost everything lives in `config.json`, not in code:

| To change | Edit |
|---|---|
| What job titles count | `filters.title_require_any` |
| What to reject | `filters.title_exclude` |
| Which cycle | `filters.years` and `filters.summer_2027_only` |
| Which companies | the `firms` list |

After **any** filter change, run the workflow in `verify` mode. It runs
`test_filters.py`, which checks ~118 real posting titles still sort correctly.
Filters are easy to break in ways you won't notice for weeks — that's what the
tests are for.

`CLAUDE.md` has the full architecture notes and a list of traps that have
already caught people. Read it before changing anything in `watcher.py`.

---

## Files

| File | Purpose |
|---|---|
| `watcher.py` | All logic: fetch → filter → dedupe → email |
| `config.json` | Sources and filters. **Most changes belong here.** |
| `verify_sources.py` | Probes every source, reports the dead ones |
| `test_filters.py` | Filter regression tests over real posting titles |
| `CLAUDE.md` | Architecture notes and hard-won gotchas |
| `PROGRAMS.md` | Hand-maintained deadline calendar; appended to the digest |
| `seen_jobs.json` | State. Auto-committed each run. Never hand-edit |
| `OPEN_ROLES.md` / `TOP_PICKS.md` | Auto-generated each sweep. Never hand-edit |
