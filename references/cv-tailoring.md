# CV review and tailoring

## Strategy: role-type variants, not one CV per job
Build **one CV variant per role type** the candidate targets (usually 2–4, e.g. "Backend Engineer", "Platform / DevOps", "Team Lead path"), each in `CVs/<Role type>/`. Then, for a specific posting, either pick the closest variant or make a small per-job tweak. A full rewrite for every job is slow and leads to drift and inconsistent claims.

## Reviewing an existing CV
Check, and report as a short numbered list:
1. **Claims vs. profile**: anything not backed by `profile.md` → ask the candidate, or remove it.
2. **Missing verified strengths**: things in the profile, or things the target postings ask for that the candidate *has* done, which the CV doesn't show. This is usually the biggest win.
3. **Relevance ordering**: the most relevant experience first, both in each role's bullets and in the skills section.
4. **Language of the target postings**: use the postings' own terms where they truthfully apply. ATS keyword match matters.
5. **Clarity**: one line per bullet where possible; start with a strong verb; say what the candidate did, not what the team did.
6. **Format**: 1–2 pages, no photos (unless that's the local norm), no tables or text boxes that break ATS parsing, consistent dates.

## Tailoring to a specific posting
1. Fetch the posting (WebFetch, or `get_page_text` in Chrome).
2. Pull out its 5–10 real requirements, both must-have and nice-to-have.
3. Map each to **have / partial / gap**, using only verified experience. Show this table to the candidate.
4. Pick the variant that matches best. If a per-job tweak would help (reordering bullets, surfacing a relevant verified project), propose the exact changes, apply them after approval, and save in `CVs/<Role type>/<Company>/`.
5. For "partial" items, ask if there's more to it. People often undersell themselves. Never upgrade "partial" to "have" without their confirmation.

## Honesty rules for CV text
- Every claim must be something the candidate personally did. Use "led" only if they led it. Use "built" only if they built it.
- Avoid invented or unverifiable numbers. If the candidate gives a real number, use it. Otherwise describe the impact in words. (Some candidates prefer no numbers at all. Respect that.)
- Don't put a target job title in the header or file name. Show the candidate's real titles.
- Sensitive employers can be described generically if the candidate asks.

## Building the document
Write the content to `CVs/<Role type>/cv.json`, then run:
```
python <skill>/scripts/build_cv.py "CVs/<Role type>/cv.json" "CVs/<Role type>/<Name> CV.docx" --pdf
```
JSON schema:
```json
{
  "name": "Full Name",
  "contact": ["City, Country", "email@example.com", "+1 555 0100", "linkedin.com/in/…", "github.com/…"],
  "summary": "2–4 sentence profile.",
  "sections": [
    {"title": "Skills", "type": "skills", "items": [{"label": "Languages", "text": "Python, Go"}]},
    {"title": "Experience", "type": "jobs", "items": [
      {"title": "Senior Engineer", "org": "Company", "location": "City", "dates": "Jan 2022 – Present",
       "intro": "optional one-line context", "bullets": ["Did X", "Built Y"]}
    ]},
    {"title": "Education", "type": "jobs", "items": [{"title": "B.Sc. Computer Science", "org": "University", "dates": "2016 – 2019", "bullets": []}]},
    {"title": "Languages", "type": "text", "text": "English (native), Spanish (fluent)"}
  ]
}
```
`--pdf` uses Microsoft Word (Windows, via `docx2pdf` if installed) or LibreOffice (`soffice`). If neither is available, deliver the .docx and say so.

After building, render the PDF to an image or read it back to check the layout (page breaks, overflow) before showing the candidate.
