# Competitions, programs & scholarships calendar

Emailed every Sunday 10am ET, appended to the digest. Tuned for **embedded
software engineering with ML / AI / CV second, graduating May 2028, Summer 2027
cycle**. The `digest: true` pagewatchers in `config.json` alert when these pages
change — this file is the hand-maintained calendar that goes out alongside them.

> **Edit this file by hand.** Everything else in the repo is auto-generated.
> Dates below are the historical pattern for each program, not a promise — the
> pagewatchers are what actually catch a window opening.

---

## ⏰ NEXT 90 DAYS — Aug–Oct 2026

Software internship recruiting for Summer 2027 runs earlier and faster than
most people expect. The large-volume employers open in **August–October** and
some close within weeks of opening.

- **NOW — set native job alerts** at Google, Meta, Microsoft and Apple. Their
  careers pages are JavaScript shells, so the watcher can only weakly detect
  changes on them. This is the highest-value manual step in the setup.
- **Aug–Sept: big tech opens.** Google STEP and SWE internships, Microsoft
  Explore, Meta, Amazon. These fill fast and several are first-come-first-served
  in practice.
- **Sept–Oct: robotics and autonomy open.** Zoox, Skydio, Waymo, Kodiak,
  Applied Intuition, Figure. Smaller teams, later postings, far less applicant
  volume than big tech — historically the best effort-to-outcome ratio for an
  embedded profile.
- **~Sept–Oct: NSA Codebreaker Challenge** launches and runs through the fall.
  School-ranked, reverse-engineering and embedded-security flavoured, and a
  clean resume line.
- **Oct 1 – Dec: DoD SMART Scholarship** — full tuition, stipend and a
  guaranteed DoD job. Strong fit if defense work is acceptable; embedded and
  autonomy placements are common. Note it commits post-graduation years to DoD.
- **Oct: IEEEXtreme** — 24-hour global programming contest, run through a
  student IEEE branch.
- **Nov–Jan: defense primes post summer reqs** — Anduril, Shield AI, Northrop,
  RTX, Draper, Leidos. Later than commercial tech and less contested.
- **Dec–Feb: national lab REU deadlines** — DOE SULI, NREIP (Navy), MIT Lincoln
  Lab, Sandia. Lincoln Lab and NREIP both do heavy embedded and autonomy work.
- **Jan: MIT Battlecode** — month-long AI programming competition over IAP.
  Unusually good portfolio piece for an ML-leaning candidate.

---

## 🤖 Robotics, embedded & autonomy

The part of the market where a strong embedded portfolio beats a strong GPA,
and where applicant volume is lowest relative to role quality.

- **Zoox, Skydio, Kodiak, Waabi, Field AI, Sanctuary, Woven by Toyota** — all
  polled directly by the hourly sweep.
- **Figure, Apptronik, 1X** — humanoid robotics; small intern classes, heavy
  real-time and controls work.
- **Anduril, Shield AI, Saronic** — defense autonomy; large intern programs and
  genuinely hard embedded problems.
- **NASA OSTEM / JPL** — flight software and avionics. Deadlines are early and
  rigid; JPL in particular closes well before spring.
- **Build something that runs on real hardware.** For embedded roles
  specifically, a project on an actual board — STM32, ESP32, Raspberry Pi Pico,
  a drone flight controller — is worth more than another web app. Screeners
  look for the target MCU, the RTOS or bare-metal choice, and the buses used.

---

## 🏆 Competitions & hackathons

- **ICPC** — the classic competitive-programming route. Regionals in the fall.
- **MIT Battlecode** — January, AI/strategy, month-long.
- **Kaggle featured competitions** — the most direct ML portfolio signal.
- **MLH season** — <https://mlh.io/> — the hackathon circuit index.
- **HackMIT · TreeHacks · PennApps · Hack the North** — the large ones;
  applications open roughly Aug–Sept for the fall events.
- **picoCTF · CSAW · National Cyber League · DOE CyberForce · MITRE eCTF** —
  security competitions. eCTF is *embedded* CTF specifically, so it is the one
  that doubles as embedded portfolio work.
- **Google Summer of Code** — <https://summerofcode.withgoogle.com/> — paid
  open-source work; organisations are announced in late winter, applications
  in spring. A real alternative if an internship does not land.
- **MLH Fellowship** — <https://fellowship.mlh.io/> — same idea, open-source,
  runs multiple cohorts a year.
- **Outreachy** — <https://www.outreachy.org/> — paid open-source internships
  for people subject to under-representation in tech.

---

## 💰 Fellowships & scholarships

- **DoD SMART** — see the 90-day list. Largest award here.
- **Neo Scholars · Z Fellows · Thiel · 8VC · Soma · Interact · Contrary** —
  the startup-fellowship circuit. Most are not summer programs, so they do not
  conflict with an internship. Neo in particular targets strong CS
  underclassmen.
- **Goldwater** — research-track; needs a faculty research narrative, which is
  the long pole. Campus internal deadlines run ~Dec. Worth starting a year out.
- **IEEE CS Merwin** — requires a 3-month IEEE + Computer Society membership
  clock, so join well before the ~Sept 30 deadline.
- **UPE (CS honor society) awards** — requires ACM and chapter membership first.
- **AFCEA STEM Majors** — national, defense-adjacent, low-friction application.
- **DoD Cyber Service Academy** — full ride plus service commitment.
- **Hertz · Churchill** — for later years, but the research narrative they need
  is the same one Goldwater needs, so the work compounds.

---

## 🏛️ Labs & research programs

Less contested than industry internships, and the work is often more technically
open-ended.

- **DOE SULI** — <https://science.osti.gov/wdts/suli> — every DOE national lab,
  two cycles a year.
- **NREIP (Navy)** — Navy labs; autonomy, embedded and signal work.
- **MIT Lincoln Laboratory summer program** — large, well-run, heavy on
  autonomy and embedded systems.
- **Sandia student internships** — including robotics and embedded security.
- **JHU Applied Physics Lab** — large intern program, page-watched.
- **NSF ETAP** — <https://etap.nsf.gov/> — the searchable index of every NSF
  REU. Filter for CS and robotics; many sites run ML and autonomy projects.
- **Pathways to Science** — a second REU database with different coverage.

---

## Notes

- **US-only.** The watcher drops non-US roles including Canada, since several
  robotics and silicon employers post heavily in Toronto, Ottawa and Vancouver
  and would otherwise dominate the list.
- **Clearance.** Many defense and lab programs require US citizenship, and some
  require a clearance the employer sponsors. Roles asking for either are flagged
  🇺🇸 in `TOP_PICKS.md`. If you hold or can obtain a clearance, say so — it
  changes which of these are worth prioritising.
- **General SWE roles are kept but ranked last** in the email. If the volume
  becomes annoying, the fix is one edit: remove the broad SWE terms from
  `title_require_any` in `config.json`.
