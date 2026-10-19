#!/usr/bin/env python3
"""Filter regression tests.

Every title below is a REAL posting title observed in the community trackers
(or a close variant), so this pins the behaviour most likely to break: embedded
and ML roles must survive and rank correctly, general SWE must land in the
fallback tier rather than the top, and non-engineering noise must be dropped.

Run:  python3 test_filters.py
"""
import json
import sys

import watcher as w

FILTERS = json.load(open("config.json"))["filters"]

# (title, expected_category)
#   0 = embedded/firmware/robotics, 1 = ML/AI/CV, 2 = general SWE, 3 = other
KEEP = [
    # --- embedded / firmware: the primary target (real tracker titles) ---
    ("Embedded Software Engineering Intern", 0),
    ("Software Engineer Intern, Embedded", 0),
    ("Firmware Engineer Intern", 0),
    ("Firmware Engineering Co-op", 0),
    ("Embedded Software Engineer Intern, Keys & Authentication", 0),
    ("Software Engineer Intern - Embedded Platforms", 0),
    ("Long Range Platform Embedded Firmware Intern - Summer 2027", 0),
    ("Motor Control Firmware Intern", 0),
    ("RTOS Engineering Intern", 0),
    ("Device Driver Engineering Intern", 0),
    ("Bootloader and BSP Intern", 0),
    ("Flight Software Engineering Intern", 0),
    ("Avionics Software Intern", 0),
    ("Robotics Software Engineering Intern", 0),
    ("Autonomy Engineering Intern", 0),
    ("Sensor Fusion Engineer Intern", 0),
    ("Controls Engineering Intern", 0),
    # --- ML / AI / CV: the secondary target ---
    ("Machine Learning Engineer Intern", 1),
    ("Deep Learning Research Intern", 1),
    ("Computer Vision Engineering Intern", 1),
    ("Perception Engineer Intern", 1),
    ("Applied Scientist Intern", 1),
    ("LLM Research Engineer Intern", 1),
    ("Reinforcement Learning Intern", 1),
    ("Data Science Intern", 1),
    # --- general SWE: the fallback tier, must NOT outrank the above ---
    ("Software Engineer Intern, Backend", 2),
    ("Full Stack Developer Intern", 2),
    ("Site Reliability Engineering Intern", 2),
    ("Cloud Infrastructure Intern", 2),
    ("Compiler Engineer Intern", 2),
    ("Security Engineering Intern", 2),
    ("iOS Developer Intern", 2),
]

DROP = [
    # --- wrong discipline ---
    "Mechanical Engineer Intern",
    "Manufacturing Engineer Intern",
    "Chemical Engineer Intern",
    "Industrial Engineer Intern",
    "Materials Engineer Intern",
    "Process Engineer Intern",
    # --- not engineering ---
    "Business Development Intern",
    "Sales Engineering Intern",
    "Marketing Intern",
    "Human Resources Intern",
    "Supply Chain Intern",
    "Internal Audit Manager",
    "International Sales Director",
    "Quality Assurance Intern",
    "Manual Test Engineer Intern",
    # --- wrong seniority ---
    "Senior Embedded Software Engineer",
    "Principal Machine Learning Engineer",
    "Director of Engineering",
    # --- wrong cycle ---
    "Fall 2027 Software Engineering Co-op",
    "Spring 2027 Embedded Intern",
    "Summer 2026 Firmware Intern",
    "Embedded Software Engineer Intern - Fall 2026",
    "2026 Silicon Engineering Intern",
    # --- pure hardware design: this is a software profile ---
    "Hardware ASIC Design Intern",
    "FPGA Design Intern",
    "RTL Design Engineer Intern",
]

# (title, content, expected_is_summer_2027)
CYCLE = [
    ("Embedded Software Engineering Intern", "", True),   # no cycle -> keep
    ("Summer 2027 Firmware Intern", "", True),
    ("Firmware Intern", "Summer 2027 program, 12 weeks", True),
    ("Fall 2027 Embedded Co-op", "", False),
    ("Spring 2027 Robotics Intern", "", False),
    ("Summer 2026 ML Intern", "", False),
    ("Summer 2028 SWE Intern", "", False),
    ("Perception Intern", "This is our Fall 2027 co-op rotation.", False),
]

# Ordering guarantees: embedded outranks ML, ML outranks general SWE. A title
# naming two categories must resolve to the higher-priority one.
ORDERING = [
    ("Embedded Machine Learning Intern", 0),     # embedded beats ML
    ("ML Infrastructure Software Intern", 1),    # ML beats general SWE
    ("Robotics Perception Software Intern", 0),  # embedded beats both
    ("Embedded Software Engineer", 0),           # embedded beats "software"
    ("Hardware/Software Integration Intern", 2),  # survives on "software"
]

fails = []
checks = 0


def check(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


print("=== titles that MUST pass, in the right category ===")
for title, want in KEEP:
    job = {"title": title, "location": "Austin, TX", "content": ""}
    ok = w.is_relevant(job, FILTERS)
    cat = w._role_category(title)
    good = ok and cat == want
    print(f"  {'ok ' if good else 'FAIL'} [cat {cat}, want {want}] {title[:60]}")
    check(ok, f"KEEP dropped: {title}")
    check(cat == want, f"KEEP wrong category: {title} -> {cat}, want {want}")

print("\n=== titles that MUST be dropped ===")
for title in DROP:
    job = {"title": title, "location": "Austin, TX", "content": ""}
    ok = w.is_relevant(job, FILTERS)
    print(f"  {'FAIL' if ok else 'ok '} {title[:66]}")
    check(not ok, f"DROP kept: {title}")

print("\n=== Summer-2027 cycle gate ===")
for title, content, want in CYCLE:
    got = w._is_summer_2027({"title": title, "content": content})
    print(f"  {'ok ' if got == want else 'FAIL'} {str(got):5} (want {want}) "
          f"| {title[:52]}")
    check(got == want, f"CYCLE {title!r} -> {got}, want {want}")

print("\n=== priority ordering when a title matches two categories ===")
for title, want in ORDERING:
    got = w._role_category(title)
    print(f"  {'ok ' if got == want else 'FAIL'} cat {got} (want {want}) "
          f"| {title[:52]}")
    check(got == want, f"ORDERING {title!r} -> {got}, want {want}")

print("\n=== TOP_PICKS want/skip gate ===")
for title, _ in KEEP:
    inpick = bool(w.WANT_RE.search(title) and not w.SKIP_RE.search(title))
    if not inpick:
        print(f"  note: not in TOP_PICKS (matched no WANT term): {title}")
for title in DROP[:15]:
    inpick = bool(w.WANT_RE.search(title) and not w.SKIP_RE.search(title))
    check(not inpick, f"TOP_PICKS kept an excluded role: {title}")

print("\n" + "=" * 62)
if fails:
    print(f"{len(fails)} FAILURE(S) out of {checks} checks:")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print(f"All {checks} filter assertions passed.")
