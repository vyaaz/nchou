# Internship Watcher

**Profile: embedded software engineering, with ML / AI / CV second.**
Summer 2027 cycle, graduating May 2028, anywhere in the US, defense included.

This repo is descended from a watcher originally built for a quant/SWE profile
and later retuned for chip design. If a stray comment mentions quant firms or
FPGA design, that is the lineage, not the current setup.

Two crons, both live:

1. **Hourly role sweep** — polls robotics, AI, embedded, silicon and defense
   sources plus the community trackers, and emails the moment a new **Summer
   2027** embedded / ML / SWE internship opens. Gated by `summer_2027_only` in
   `config.json → filters`; `top_firms_only` is **off**.
2. **Sunday 14:00 UTC digest** (`DIGEST_MODE=1`) — competitions, hackathons,
   fellowships, scholarships and lab REUs. See "Weekly digest".

**Coverage note.** The community trackers this repo polls are SWE-oriented, so
for this profile they are unusually productive — the auto-discovery source
alone reaches ~270 company boards and pulls tens of thousands of raw postings
per run. Expect meaningfully more volume than a hardware-focused setup, which
is why the filters matter more than the source list here.

## Who this is for (drives all filtering)

- **Graduating May 2028** — eligible for essentially every Summer 2027 intern req
- **Primary target: embedded software.** Firmware, RTOS, bare-metal, drivers,
  BSP, bootloaders, motor control, avionics and flight software, robotics and
  autonomy.
- **Secondary target: ML / AI / CV.** Machine learning, perception, computer
  vision, applied science, LLM work.
- **General SWE is a deliberate fallback tier**, not an accident. Backend,
  infrastructure, platform and similar roles are kept but always rank *below*
  embedded and ML, so a generic SWE posting can never push a firmware role down
  the email.
- **Pure hardware design is OUT.** "FPGA Design Intern", "Hardware ASIC Design
  Intern" and "RTL Design Engineer" are dropped — this is a software profile.
  A hybrid title survives on its other half: "Hardware/Software Integration
  Intern" passes on the word "software". `title_require_any` deliberately does
  **not** contain "hardware", "fpga", "asic" or "silicon".
- **Email is ranked into 4 categories, in this exact order:**
  ① Embedded / firmware / robotics ② ML / AI / CV ③ General SWE
  ④ everything else that matched. See `build_email_html` and `_role_category`.
  Order inside `_role_category` is load-bearing: EMBEDDED_RE is tested first,
  so "Embedded Machine Learning Intern" is embedded, not ML.
- **Anywhere in the US.** No city is promoted — `priority_locations` is empty
  and `_loc_rank` only pushes roles with a recognisable hub location above ones
  whose location is vague. **US-only** is enforced by `_is_us_location()`;
  Canada is excluded deliberately, since several robotics and silicon employers
  post heavily in Toronto, Ottawa and Vancouver.
- **Defense and national labs are IN** — Anduril, Shield AI, Northrop, RTX,
  Draper, Leidos, Sandia, MIT Lincoln Lab. A very large share of embedded and
  perception internships sit here. No clearance is assumed, so `is_clearance()`
  does not drive the email layout; it flags roles with 🇺🇸 in `TOP_PICKS.md`.

## Weekly digest (the live feature)

Sunday 14:00 UTC → `DIGEST_MODE=1` → `send_weekly_digest()`, which:

1. Runs `run_digest_sweep()` over the **competition / hackathon / fellowship /
   scholarship / lab** sources only (parallel, 12 workers) and reports pages
   that **changed since last Sunday** — usually meaning applications just opened.
2. Appends the `PROGRAMS.md` master calendar, then a clickable index of every
   watched page (generated from config, so it can't go stale).

A source is in the digest iff `_is_digest_source()`: explicit `"digest": true`
in config wins, else the `name:` prefix is one of Competition / Hackathon /
Scholarship / Fellowship / Abroad / Program / NatSec / Lab / Conference / Grant.
Company job boards (`AI:`, `Robotics:`, `Embedded:`, `Silicon:`, `Defense:`,
`Page:`) are internship-hunting and stay OUT — they carry `"digest": false`.

**Pagewatch keying (gotcha #9):** pagewatch state keys are
`pw::<url>::#<content-hash>` via `_pw_key()`. Keyed by URL alone a watcher fires
**exactly once, ever**, then goes silent, so "tell me when applications open"
never fires again. A URL with no recorded hash yet is baselined **silently**, so
a keying change can't flood the first email.

## Layout

| File | Purpose |
|---|---|
| `.github/workflows/watch.yml` | Hourly cron + manual "Run workflow" button |
| `watcher.py` | All logic. Fetchers → filters → dedup → email |
| `config.json` | Sources + filters. **Most changes belong here, not in code.** |
| `seen_jobs.json` | State. Auto-committed each run. Never hand-edit. |
| `OPEN_ROLES.md` | Auto-generated snapshot of every role currently open, rewritten each full sweep and committed. Never hand-edit. |
| `TOP_PICKS.md` | Curated shortlist: embedded / ML / SWE roles, ranked. Auto-generated; never hand-edit. |
| `PROGRAMS.md` | Hand-maintained deadline calendar, appended to the Sunday digest. **Edit this one by hand.** |
| `verify_sources.py` | Probes every source and reports the dead ones. Run it in CI — a mistyped token returns 0 jobs silently. |
| `test_filters.py` | Filter regression tests over real posting titles. Run before any filter change lands. |
| `applications.md` | **Private, gitignored** (repo is public!). Application tracker: one section per role — company, status, resume used, notes. Claude edits this directly on request. Never commit it. |

**Secrets (repo → Settings → Secrets → Actions):** `SMTP_USERNAME` (a Gmail
address), `SMTP_PASSWORD` (Gmail **App Password**, not the account password),
`EMAIL_TO`. Optional: `USAJOBS_API_KEY` + `USAJOBS_EMAIL`.

## Architecture

Every entry in `config.json` → `firms[]` has an `ats` field that routes it to a
fetcher in `watcher.py`'s `FETCHERS` dict. Every fetcher returns normalized dicts:
`{id, title, company, location, url, content, ...}`.

| `ats` | What it does |
|---|---|
| `greenhouse` `lever` `ashby` `smartrecruiters` `workable` | Public ATS JSON APIs. `token` = the slug in the board URL. |
| `workday` | Undocumented-but-public CXS endpoint. Needs `host` / `tenant` / `site` — get them from the careers page's DevTools → Network → the POST to `/wday/cxs/.../jobs`. Use `search_text` to filter server-side and `max_pages` to cap. |
| `amazon` | Undocumented `amazon.jobs/en/search.json`. Covers AWS / Robotics / all. |
| `usajobs` | Federal: NASA, DOE labs, NSA, Army/Navy research, Pathways. Needs a free key. |
| `github_json` | Tracker repos publishing `listings.json` (vanshb03). |
| `github_md` | Tracker repos whose data is a markdown **table** (sndsh404, speedyapply). |
| `autodiscover` | **The big one.** Harvests every apply URL from all trackers, decodes each company's ATS board, and polls ~270 boards **in parallel**. Self-expanding: any company a tracker adds gets polled from then on. |
| `pagewatch` | Change-detector for feed-less pages. Used for the big chip employers with no pollable API — AMD, Qualcomm, Apple, TI, Synopsys, Arm, Lattice — plus the labs (NASA OSTEM, SULI, JHU APL, Sandia). Alerts when watched keywords appear/change. |

Failed sources are **skipped and logged** (`x <name> skipped`), never crash the run.
Read the Actions log to see which sources actually resolved.

## Filtering (`config.json` → `filters`)

1. `title_keywords` — must look like an internship
2. `title_require_any` — must be an embedded / ML / SWE domain (83 keywords:
   embedded, firmware, rtos, driver, robotics, autonomy, machine learning,
   computer vision, software, backend, ...). Deliberately excludes "hardware",
   "fpga", "asic" and "silicon".
3. `title_exclude` — PhD/Masters, wrong seniority, off-cycle, non-software
   engineering disciplines, and QA/manual-test roles.
4. **Cycle check** — see gotcha #1 below
5. **US-only gate** (`_is_us_location`) — clearly-non-US roles are dropped after the
   relevance check; empty/ambiguous locations are kept (never silent-drop a US role)
6. `clearance_keywords` — still computed by `is_clearance()` for the run log and the
   🇺🇸 flag in TOP_PICKS, but no longer creates an email section (see "Who this is for")

Then, at ranking time (not a filter — nothing is dropped here):

7. `_role_category()` sorts a title into embedded → ML/CV → general SWE → other.
   The order of the three `if` statements is the ranking; changing it changes
   the email.

## HARD-WON GOTCHAS — read before changing anything

1. **NEVER require the year in the job title.** Most companies don't put it there
   (Palantir: `"Forward Deployed Software Engineer - Internship - Intel"`). An
   earlier version required `"2027"` in the title and **silently discarded every
   such role** across all direct ATS sources for weeks.
   Current logic: if the title names *any* year, one of them must be ours; else
   check the description; **if no year appears anywhere, KEEP it** — a live intern
   posting is almost always the current cycle, since recruiting runs a year ahead.

2. **Silent drops are the most dangerous bug class.** #1 went unnoticed because a
   filtered-out role produces no log line. **If you add a filter, log what it drops.**

3. **Auto-discovery must stay parallel.** 211 boards polled sequentially takes
   *hours* (Workday paginates 20 at a time). Keep `ThreadPoolExecutor`,
   `max_pages=3`, and `budget_seconds`. A sequential version hung a run for 20+ min.

4. **`git push` must rebase first.** The `Save state` step does
   `git pull --rebase` before pushing — otherwise editing files via the GitHub web
   UI moves `main` and the run's state-commit fails with a non-fast-forward error.

5. **Community trackers go stale.** `sharunkumar` is really a *2026* repo; its few
   "2027" tags produced dead links and closed roles. It's disabled. **Verify a
   tracker's actual cycle before enabling it.**

6. **Trackers lag; boards don't.** Polling a company's board directly beats reading
   a tracker — you see the posting the hour it goes up instead of when a maintainer
   adds it. That's the whole point of `autodiscover`.

7. **Substring keyword matching floods the email with garbage.** `"intern" in
   title` matches Intern**al**, Intern**ational**, Intern**als**, Intern**et** —
   one baseline email had 100+ "Internal Audit" / "International Sales" directors.
   Same trap: `"systems"` matched "Eco**systems**". `_title_is_internship()` and
   `_has_term()` use word-boundary regexes; keep it that way for any new keyword
   gate. Filters now count every drop by reason (`DROP_COUNTS`) and print a
   summary at the end of each run — check it after any filter change.

8. **Emails show one line per role.** `_collapse_locations()` merges the same
   company+title posted in N cities into one entry ("NYC · Palo Alto +2 more").
   Display-only: every posting URL is still tracked individually in
   `seen_jobs.json`, so a role opening in a new city later still alerts.

9. **Pagewatch keys must include the content hash.** `_pw_key()` builds
   `pw::<url>::#<hash>`. Keyed by URL alone, a watcher fires exactly once ever and
   then goes silent forever — which defeats the entire point of "tell me when
   applications open". A URL with no recorded hash is baselined silently.

10. **General SWE must stay a *tier*, not a peer.** Most intern postings in the
    world are generic SWE, so if `GENERAL_SWE_RE` is ever checked before
    `EMBEDDED_RE` or `ML_RE`, the email fills with backend roles and the
    firmware roles this repo exists to find sink to the bottom. The ordering is
    pinned by `test_filters.py`; do not reorder without re-running it.

11. **"Embedded" and "software" overlap by design.** Almost every embedded
    posting also contains the word "software", so category order — not keyword
    exclusivity — is what separates them. That is why "Embedded Software
    Engineer Intern" lands in category 0 and not category 2.

## Pending / next upgrades

- **Run `verify_sources.py` first.** The ATS tokens and Workday host/site pairs
  in `config.json` were harvested from live tracker URLs rather than typed from
  memory, but a few are unverified and carry no `"verified": true`. One CI run
  (workflow mode `verify`) tells you which to drop.
- **`SimplifyJobs/Summer2027-Internships`**, if and when it launches, is the
  single biggest coverage upgrade available for this profile — ~17k listings,
  SWE-heavy. Add it as a `github_json` source. (Probe:
  `https://raw.githubusercontent.com/<owner>/<repo>/dev/.github/scripts/listings.json`)
- **Google, Meta, Microsoft and Apple have no pollable feed** — their page
  watchers are JS shells and the signal is weak. Set *native* job alerts on those
  careers sites as the real backup; that is the highest-value manual step.
- **USAJOBS is configured but inert** until `USAJOBS_API_KEY` / `USAJOBS_EMAIL`
  secrets are set. Free key: <https://developer.usajobs.gov/apirequest/>
- **iCIMS fetcher** — several defense contractors and Lattice use it; no clean
  public API, so they are `pagewatch` only.
- **Eightfold fetcher** — Netflix and others.
- **FAANG page-watchers are weak** (JS single-page apps; the static HTML doesn't
  change when a job posts). Set *native* job alerts at Google / Meta / Apple /
  Microsoft / Netflix as the real backup.
- LinkedIn / Indeed have **no public API** and scraping them gets IP-blocked from
  Actions runners. They mostly re-list ATS postings anyway, so polling the ATS
  directly is both earlier and cleaner. Don't go down this road.

## Testing

Filters are pure functions, so the regression suite needs no network. **Run it
before changing any filter** — every title in it is a real posting observed in
the community trackers:

```bash
python3 test_filters.py
```

It pins what is most likely to break: embedded roles must survive and rank
first (`Embedded Software Engineering Intern`, `Firmware Engineer Intern`,
`Motor Control Firmware Intern`), ML must rank second, general SWE must land in
the fallback tier and never above them, and pure hardware design must be
dropped (`FPGA Design Intern`, `Hardware ASIC Design Intern`).

Check the sources are actually alive (needs network; run it in CI):

```bash
python3 verify_sources.py           # human-readable
python3 verify_sources.py --json    # machine-readable
python3 verify_sources.py --prune   # drop dead entries from config.json
```

A mistyped Greenhouse token or renamed Workday site does **not** raise — the
fetcher returns zero jobs and the log says "0 relevant", which is
indistinguishable from "nothing is open". That is what this script is for.

Full local run (sends a real email):

```bash
pip install -r requirements.txt
SMTP_USERNAME=... SMTP_PASSWORD=... EMAIL_TO=... python watcher.py
```

Delete `seen_jobs.json` locally to force a fresh baseline. **Don't commit that
deletion** unless you want a full catch-up email.
