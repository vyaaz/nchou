#!/usr/bin/env python3
"""Filter regression tests.

Every title below is a real or representative posting title, so this pins the
behaviour most likely to break: each target role (SWE, FDE, ML, robotics / autonomy / CV, PM,
design, consulting) must survive and land in the right category, and non-target
noise must be dropped.

Run:  python3 test_filters.py
"""
import json
import sys

import watcher as w

FILTERS = json.load(open("config.json"))["filters"]

# (title, expected_category)
#   0 = SWE / forward deployed, 1 = ML engineering,
#   2 = robotics / autonomy / computer vision, 3 = product mgmt / design,
#   4 = technical / functional consulting, 5 = other
KEEP = [
    # --- software engineering ---
    ("Software Engineer Intern, Backend", 0),
    ("Full Stack Developer Intern", 0),
    ("Site Reliability Engineering Intern", 0),
    ("Cloud Infrastructure Intern", 0),
    ("Security Engineering Intern", 0),
    ("iOS Developer Intern", 0),
    ("Embedded Software Engineering Intern", 0),
    ("SWE Intern - Summer 2027", 0),
    # --- forward deployed engineering ---
    ("Forward Deployed Engineer Intern", 0),
    ("Forward Deployed Software Engineer, Internship", 0),
    ("Forward-Deployed AI Engineer Intern", 0),
    ("Deployment Engineer Intern", 0),
    # --- ML engineering ---
    ("Machine Learning Engineer Intern", 1),
    ("ML Engineering Intern", 1),
    ("Deep Learning Research Intern", 1),
    ("Computer Vision Engineering Intern", 2),
    ("Applied Scientist Intern", 1),
    ("LLM Research Engineer Intern", 1),
    ("Data Science Intern", 1),
    ("MLOps Engineer Intern", 1),
    # --- robotics, autonomy & computer vision ---
    ("Robotics Software Engineering Intern", 2),
    ("Robotics Engineer Intern", 2),
    ("Autonomy Engineering Intern", 2),
    ("Autonomous Vehicles Software Intern", 2),
    ("Perception Engineer Intern", 2),
    ("Machine Learning Intern, Perception", 2),
    ("Computer Vision Intern - Summer 2027", 2),
    ("Motion Planning Intern", 2),
    ("Controls Engineering Intern", 2),
    ("GNC Engineering Intern", 2),
    ("Guidance, Navigation & Control Intern", 2),
    ("SLAM / State Estimation Intern", 2),
    ("Drone Software Intern", 2),
    ("UAV Autonomy Intern", 2),
    ("Mechatronics Engineering Intern", 2),
    ("Humanoid Robot Learning Intern", 2),
    ("Sensor Fusion Intern", 2),
    # --- product management ---
    ("Product Manager Intern", 3),
    ("Associate Product Manager Intern", 3),
    ("APM Intern", 3),
    ("Technical Program Manager Intern", 3),
    ("Product Management Internship", 3),
    ("AI Product Manager Intern", 3),
    # --- product design ---
    ("Product Design Intern", 3),
    ("Product Designer Intern", 3),
    ("UX Design Intern", 3),
    ("User Experience Research Intern", 3),
    # --- technical consulting ---
    ("Technology Consulting Intern", 4),
    ("Technical Consultant Intern", 4),
    ("Solutions Engineer Intern", 4),
    ("Solutions Architect Intern", 4),
    ("Machine Learning Consultant Intern", 4),
    ("Deployment Strategist Intern", 4),
    ("Customer Engineer Intern", 4),
    # --- functional consulting ---
    ("Functional Consultant Intern", 4),
    ("SAP Functional Consulting Intern", 4),
    ("Workday Consultant Intern", 4),
    ("Business Analyst Intern", 4),
    ("Business Technology Analyst Intern", 4),
    ("Advisory Intern - Technology Risk", 4),
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
    "Robotics Technician Intern",
    "Financial Controls Intern",
    "Robot Operator Intern",
    "Humanoid Robot Teleoperator Intern",
    "Robotic Welder Intern",
    "3D & LiDAR Data Annotation Analyst Intern",
    "Data & Operations Intern - Vision Zero",
    # --- wrong seniority ---
    "Senior Embedded Software Engineer",
    "Principal Machine Learning Engineer",
    "Director of Engineering",
    # --- wrong cycle ---
    "Product Marketing Intern",
    "Sales Engineering Intern - Solutions",
    "Business Development Intern, Consulting",
    "Mechanical Engineering Intern",
    "Graphic Designer Intern",
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

# Ordering guarantees: a title naming two categories must resolve to the
# right one. Product and consulting beat robotics and ML; forward deployed beats
# robotics and ML; robotics beats ML and SWE.
ORDERING = [
    ("AI Product Manager Intern", 3),               # product beats ML
    ("Machine Learning Consultant Intern", 4),      # consulting beats ML
    ("Forward Deployed ML Engineer Intern", 0),     # FDE beats ML
    ("ML Infrastructure Software Intern", 1),       # ML beats general SWE
    ("Software Engineer Intern, Machine Learning", 1),
    ("Technical Program Manager, Software", 3),     # product beats SWE
    ("Solutions Engineer, Cloud Platform", 4),      # consulting beats SWE
    ("Hardware/Software Integration Intern", 0),    # survives on "software"
    ("Robotics Software Engineer Intern", 2),       # robotics beats SWE
    ("ML Engineer Intern - Autonomy", 2),           # robotics beats ML
    ("Product Manager Intern, Robotics", 3),        # product beats robotics
    ("Solutions Engineer Intern, Autonomy", 4),     # consulting beats robotics
    ("Forward Deployed Engineer, Robotics", 0),     # FDE beats robotics
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
