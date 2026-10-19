The user gives a job-posting URL (or pasted JD text) as: $ARGUMENTS

Run this pipeline:

1. **Fetch the JD.** WebFetch the URL (fall back to `curl -sL` if blocked).
Extract: company, exact role title, location, cycle/season, required
qualifications, preferred qualifications, any short-answer/essay questions.
Flag immediately if the role is pure **hardware design** (RTL/ASIC/FPGA
design) — this profile is software, so confirm before continuing.
2. **Load context.** Read `applications.md` (integrity issues at the top are
binding) and skim the relevant parts of `career-history.md`. Style rules
(non-negotiable): no em-dashes, no “this, not that” constructions, every
bullet exactly 1 or exactly 2 rendered lines, human voice. NEVER fabricate
metrics or claims; if a preferred qualification is almost-true, name the
small task that would make it true instead of writing it.
3. **Pick the base resume** from `resumes/`. Targets for this profile:
embedded/firmware · robotics & autonomy · ML/AI/CV · general SWE ·
defense-cleared. Ask only if genuinely ambiguous. Confirm the local `.tex`
is current if the role is high-priority.
4. **Tailor with minimal targeted edits** — reorder, bold, or swap bullets
rather than rewrite. Make these legible at a glance when truthfully
claimable, since they are what screeners look for. For **embedded**:
language (C / C++ / Rust), target MCU or SoC, RTOS or bare-metal, the
peripherals and buses used (I2C / SPI / UART / CAN), and whether it ran on
**real hardware** rather than a simulator. For **ML/CV**: framework, model
family, dataset scale, and whether anything reached **production or a
deployed system**. Cover every preferred qualification
that is truthfully claimable and **bold** those phrases. Save as
`resumes/out/<LastName>_<FirstName>_<Company>_<Role>.tex` (never overwrite
the base version).
5. **Compile:** `tectonic <file>.tex` in `resumes/out/`. Fix LaTeX errors
(common: bare `&` must be `\&`). Verify it stays ONE page (`pdfinfo` or a
page count via python). Open the PDF for review.
6. **Report a coverage table:** each JD requirement / preferred qualification →
where the resume now addresses it, or “gap (honest)” / “gap (30-min task
would fix)”.
7. **Draft any short-answer/essay questions** in the user’s voice (see
`career-history.md` for voice samples). Show as drafts for their edit —
never auto-submit prose.
8. **Log it:** add or update the entry in `applications.md` with status
`prepared`, the resume filename, the date, and any deadline found in the JD.
When the user later says “sent” or “applied”, flip the status to `applied`.
9. **Hand off:** give the PDF path. If they want wording changes they edit the
`.tex` directly and say “recompile”, or tell you the change.

**Note:** this command expects `applications.md`, `career-history.md` and
`resumes/` to exist. They are gitignored (the repo is public) and are not in the
repo yet — create them before the first run, or this command will have no
context to work from.
