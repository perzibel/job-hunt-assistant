# Cover letters

Recruiters skim. A good cover letter is short (250–350 words), specific to the company, and every sentence is true.

## Process
1. Read the posting and a bit about the company (careers page, product, recent news). Find 1–2 genuine reasons this role fits the candidate. Ask the candidate why they want it. Their own reason is better than one you invent.
2. Pick the 2–3 strongest **verified** matches between the posting's requirements and `profile.md`.
3. Draft:
   - **Opening (2–3 sentences):** the role, who they are in one line, and why this company specifically.
   - **Body (1–2 short paragraphs):** the 2–3 matches, each as something concrete they did, phrased the way the posting talks about it.
   - **Honest bridge (optional, 1 sentence):** if there's an obvious gap, frame what they bring that's adjacent, without pretending.
   - **Close (1–2 sentences):** availability, location or work authorization if relevant, and thanks.
4. Show the draft to the candidate. Apply their edits. Never send a letter they haven't seen.
5. Build:
```
python <skill>/scripts/build_letter.py "Cover Letters/<Company> - <Role>.json" "Cover Letters/Cover Letter - <Company> - <Role>.docx" --pdf
```
JSON: `{"name": "...", "contact": ["email", "phone", "linkedin"], "date": "16 October 2026", "recipient": ["Hiring Team", "Company"], "salutation": "Dear Hiring Team,", "paragraphs": ["...", "..."], "closing": "Kind regards,"}`

## Avoid
- Clichés: "I am writing to express my interest…", "passionate", "perfect fit", "hit the ground running", "dynamic"
- Repeating the CV line by line
- Claims or numbers not in the profile
- Reusing an older letter without re-checking every claim against the current profile
- Flattery about the company that could apply to any company
