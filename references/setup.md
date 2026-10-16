# Setup (first run)

Goal: create the workspace and fill in `profile.md`, `Application Kit.md`, `Application Tracker.md` and `job_scan/config.json` from what the candidate tells you. Everything that follows depends on this, so take the time to get it right.

## 1. Create the workspace
Ask where to put it (default `~/JobHunt/`). Create the folders listed in SKILL.md. Copy:
- `assets/profile-template.md` → `profile.md`
- `assets/application-kit-template.md` → `Application Kit.md`
- `assets/tracker-template.md` → `Application Tracker.md`
- `assets/scan-config-example.json` → `job_scan/config.json`

## 2. Gather source material
Ask for:
- Their current CV (path to a .docx/.pdf). Read it.
- Their LinkedIn profile URL. If Claude in Chrome is available and they're logged in, you can read it there. Read only; don't edit anything.
- Optionally, 2–3 job postings they'd love to get. These show the target role and level.

## 3. Interview in rounds
Ask **numbered questions in small batches** (5–8 at a time) so they can answer quickly, e.g. "1. yes 2. no, only once 3. …". Cover:

**Targets (hard requirements)**
- Target role titles and level (and which levels are too senior or too junior)
- Locations: remote, which countries or cities, hybrid OK where, places to exclude; work authorization / citizenship / visa needs
- Pay: current pay (with period), minimum acceptable, the number to ask for
- Companies or industries to avoid; deal-breakers (shifts, travel, on-call, contract vs. permanent)

**Experience (verify, don't assume)**
- For each job on the CV: what did they *personally* own, build, lead or improve? Which tools did they use? What was the scope?
- Skills that recruiters in their field screen for. Use the sample postings to ask "have you done X?" for each common requirement. Many people did things their CV doesn't mention. Finding these is the most valuable part of setup.
- Honest gaps (things the postings ask for that they haven't done)
- Anything sensitive that must be worded carefully (e.g. a defense employer → "Defence aerospace company")

**Form answers** (for the Kit)
- Full name, preferred name, email, phone with country code, city, LinkedIn, GitHub or portfolio, pronouns (optional)
- Education and languages
- Notice period, earliest start date, willingness to relocate
- How to answer the voluntary demographic questions (default: "I do not wish to answer")

## 4. Write the files
- `profile.md`: hard requirements, verified strengths, known gaps, role types → CV folders, "Already applied or decided".
- `Application Kit.md`: ground rules, personal details, standard answers, salary, CV-per-role-type table.
- `job_scan/config.json`: see `references/weekly-review.md`. Set the title keywords, location regexes, pay floor and currency, and companies to exclude from the interview. Suggest companies to scan that hire for their role (you can research which ones use Greenhouse, Ashby or Lever. The board slug is the part of the URL, e.g. `boards.greenhouse.io/<slug>`, `jobs.ashbyhq.com/<slug>`, `jobs.lever.co/<slug>`).

Show them each file and ask them to correct anything wrong. **Only then** mark the profile "verified by candidate on <date>".

## 5. Next steps
Offer to: (a) build the role-type CV variants (`cv-tailoring.md`), (b) run a first job scan now (`weekly-review.md`), (c) schedule the weekly review.
