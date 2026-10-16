# Job Hunt Assistant: a Claude skill

A [Claude skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that runs your job search with you:

1. **Reviews and tailors your CV** to specific jobs and role types, using only facts you've confirmed
2. **Writes cover letters**: short, specific, and honest
3. **Applies to jobs for you** in your own Chrome via the [Claude in Chrome](https://claude.com/chrome) extension. You approve every submission.
4. **Runs a weekly review**: scans company job boards (Greenhouse / Ashby / Lever), checks each new posting against your requirements, and writes a report with fit %, chance %, and which CV to use. Optionally sends it to Telegram.

## Install

**Claude Code**
```bash
git clone https://github.com/perzibel/job-hunt-assistant ~/.claude/skills/job-hunt-assistant
pip install python-docx
```

**Claude.ai / Claude Desktop:** download `job-hunt-assistant.skill` from the [latest release](../../releases/latest) and upload it under *Settings → Capabilities → Skills*.

For applying in the browser, install the **Claude in Chrome** extension and log in to Chrome normally.

## Get started
Tell Claude:
> set up my job search

It interviews you (targets, location, pay, verified experience, standard form answers) and creates a workspace (`~/JobHunt/` by default) with your profile, application kit, tracker, and scan settings. Then try:

- `review my CV against this job: <link>`
- `write a cover letter for <company> <role>`
- `apply to <company>` / `apply to these 3 jobs: …`
- `run my weekly job review` (or ask it to schedule one every week)

## Ground rules built in
- Only verified facts: nothing invented, inflated, or merged into bigger claims
- You write your own essay or free-text answers. Forms that ban AI are left for you.
- It never creates accounts or enters passwords
- It shows you a summary and waits for your yes before each submission
- Every apply or skip decision is logged in your tracker

## What's inside
```
SKILL.md                  # entry point: modes and ground rules
references/               # setup, cv-tailoring, cover-letter, applying, weekly-review
assets/                   # profile / kit / tracker templates, example scan config
scripts/                  # weekly_scan.py, build_cv.py, build_letter.py, Telegram helpers
```
Your personal data stays in your own workspace folder. Nothing is stored in the skill.
