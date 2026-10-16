# Applying in Chrome (Claude in Chrome extension)

You fill in application forms in the candidate's own, logged-in Chrome. They can watch, take over at any time, and approve before anything is submitted.

## Before you start
- Load the Chrome tools in one ToolSearch call (`tabs_context_mcp, tabs_create_mcp, navigate, read_page, find, form_input, computer, file_upload, get_page_text`). If a `chrome-browser` or `claude-in-chrome` skill is listed, read it first.
- Call `tabs_context_mcp`, then open a **new tab** for each application. Don't touch the candidate's existing tabs.
- If the Chrome extension isn't connected, tell the candidate how to install and connect it (Claude in Chrome from the Chrome Web Store, then sign in) and stop.

## Pre-flight check (per job)
1. Read the posting. Check it against `profile.md` hard requirements (level, location, pay, deal-breakers). If it fails, say why and log it as "Skipped: <reason>" in the tracker. Don't apply.
2. Check the tracker. Don't apply twice.
3. Pick the CV variant (Kit → "Which CV"). Decide whether a cover letter is needed. It's needed if the form requires one or the candidate wants one (see `cover-letter.md`).
4. Give a quick **fit summary** for the candidate: requirements have / partial / gap, a rough chance estimate, and the pay to ask for (with its period).

## Filling the form
- Fill factual fields from the Kit (name, contact, links, work authorization, location, notice period, salary expectation, how they heard about the role).
- Upload files with `file_upload`, using the absolute path to the PDF.
- Answer yes/no and dropdown screening questions only from the Kit or profile. If one isn't covered, **ask the candidate**. Don't guess. Add the answer to the Kit for next time.
- Voluntary demographic questions: follow the Kit (default "I do not wish to answer").
- Consents: accept only the required privacy or processing consent. Decline marketing and non-essential cookies.
- **Free-text or essay questions:** leave them empty. Collect them and give them to the candidate word for word (unless they've explicitly asked you to draft). If the form says not to use AI, stop and tell the candidate to do the whole application themselves.

## Stop conditions (hand the job to the candidate)
- Account creation, login, password, 2FA, CAPTCHA
- AI-use restrictions on the form
- Anything that asks for ID numbers, bank details, or payment
- Assessment tests or video interviews
- The page is broken, or you've tried the same step 2–3 times without success

## Submit
1. Show a summary: every field and its value, attached files, and unanswered questions.
2. Wait for an explicit "yes, submit" for **this** application.
3. Submit and capture the confirmation (screenshot or confirmation text). If the candidate has given you access to Gmail, you can check for the confirmation email.
4. Update `Application Tracker.md` (date, company, role, CV used, pay + period, where, status "Applied", link) and the "Already applied or decided" list in `profile.md`.

## Batches
For "apply to these 5 jobs": do the pre-flight check on all of them first and show one table. Then apply one at a time, confirming each before submitting. Finish with a summary table: applied, waiting for the candidate's essays, skipped and why.
