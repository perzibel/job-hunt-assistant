# Weekly review: find new jobs and assess the pipeline

The weekly review is **research only. Never apply during it.** The candidate reads the report and then says "apply to X".

## Steps
1. Read `profile.md`, `Application Kit.md`, `Application Tracker.md`.
2. Run the scanner:
   ```
   python <skill>/scripts/weekly_scan.py --workspace <workspace>
   ```
   It reads `job_scan/config.json`, queries the public Greenhouse, Ashby and Lever job boards of the companies listed there, filters by title, location and pay, and writes `job_scan/scan_results.json`. Roles marked `new: true` haven't been reviewed yet.
3. Optionally widen the search with WebSearch for the target titles and locations (LinkedIn, Indeed, local job boards, niche boards for the candidate's field). Treat these as candidates too.
4. For **each new candidate**, open the actual posting (WebFetch) and check:
   - real remote, hybrid or on-site arrangement and the allowed countries
   - pay and its period (if published) against the floor
   - level/seniority vs. the candidate's level
   - deal-breakers from the profile (shifts, travel, language, visa)
   Keep it only if it passes the hard requirements. Otherwise list it under "Rejected" with a one-line reason.
5. For each kept role: list 5–8 key requirements marked **have / partial / gap** (verified experience only), then a **fit %**, a **chance %**, which CV variant to use, and the pay to ask for.
6. Pipeline check: from the tracker, list applications with no update in 14+ days (suggest a polite follow-up), and any upcoming interviews.
7. Write `Weekly Reports/YYYY-MM-DD.md`:
   ```
   # Weekly job review: YYYY-MM-DD
   **Summary:** N scanned · K new matches · M recommended · P follow-ups due

   ## Recommended roles
   | # | Company | Role | Where | Pay (period) | Fit | Chance | CV | Link |

   ## Role details
   ### 1. Company: Role
   - ✅ requirement … / 🟡 partial … / ❌ gap …
   - Why it fits / risks

   ## Follow-ups due
   ## Rejected this week (reason)
   ```
8. Add every reviewed key to `job_scan/seen.json` (the scanner's `key` field, `company|title`), so it isn't reported again.
9. Write a ≤25-line `job_scan/summary.txt` that ends with: `To apply, ask Claude: "apply to <company>"`. If Telegram is configured, run:
   ```
   python <skill>/scripts/send_telegram.py --workspace <workspace> job_scan/summary.txt --file "Weekly Reports/YYYY-MM-DD.md"
   ```
   Otherwise, show the summary in chat.

## Scheduling it weekly
Offer the candidate one of these, in order of preference:
- **Claude Code scheduled task:** if the `schedule` skill or the `create_trigger` tool is available, create a weekly task (e.g. Sunday morning in their time zone) whose prompt is: "Use the job-hunt-assistant skill to run the weekly review for the workspace at <path>. Research only, do not apply." A cloud task can't see local files, so for cloud runs the workspace must be in a git repo the task can access. Otherwise use a local option.
- **Local:** Windows Task Scheduler or cron running `claude -p "Use the job-hunt-assistant skill to run the weekly review for <path>. Research only."`
- **Manual:** the candidate types "weekly review" once a week.

## `job_scan/config.json` reference
```json
{
  "greenhouse": ["gitlab", "cloudflare"],          // board slugs
  "ashby": ["posthog", "notion"],
  "lever": ["spotify"],
  "exclude_companies": [],                         // slugs to skip entirely
  "high_payers": [],                               // keep these even if pay is unpublished
  "title_include": "backend|platform engineer",    // regex, case-insensitive
  "title_exclude": "staff|principal|manager|intern|junior",
  "description_require": "",                       // optional regex the posting text must match
  "location_include": "remote|europe|emea|germany|berlin",
  "location_exclude": "united states|usa|canada|apac",
  "target_locations": "germany|berlin|spain",      // non-remote roles must match this
  "allow_remote": true,
  "currency": "EUR",
  "pay_floor_annual": 80000,                       // in `currency`; 0 disables the pay filter
  "keep_unpublished_pay": false,                   // true = keep every role with no published pay
  "fx_to_currency": {"€": 1.0, "EUR": 1.0, "$": 0.86, "USD": 0.86, "£": 1.17, "GBP": 1.17}
}
```
(The real file is plain JSON with no comments. See `assets/scan-config-example.json`.)
Tune it after the first run. Too many results → tighten `title_include` or `title_exclude`. Too few → add companies or loosen the location filters. Keep the FX rates roughly current.
