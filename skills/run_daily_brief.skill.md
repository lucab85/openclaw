# Skill: run_daily_brief
# Goal: produce a useful Daily Brief + Action Queue safely.

## Trigger
- "run_daily_brief"
- "Run my daily brief"
- "Create my daily brief and actions"

## Inputs
- Time window: default = last 24 hours
- Focus: default = top priorities from about_me.md
- Output mode: default = "draft" (never auto-send)

## Preconditions / safety checks
- Load memory: about_me.md and operating_rules.md
- Use tools minimally and read-only where possible
- Never send/post externally without explicit confirmation

## Tools
1) Search tool (web/search)
   - Max 4 queries
   - Collect max 8 items total
2) Draft tool (email or chat draft)
   - Draft only

## Workflow
1) Read memory files and restate today's focus in 1 line.
2) Run up to 4 search queries aligned to focus areas.
3) Extract signals: what changed, why it matters, confidence level.
4) Produce Daily Brief (max 12 bullets).
5) Produce Action Queue (max 8 items) with owner/effort/next step/confidence.
6) If output mode = draft:
   - Create draft message/email with the result.
   - Ask for confirmation before sending/posting.

## Output contract
### Outcome
<1–2 lines>

### Daily Brief (max 12 bullets)
- Priorities (Top 3):
  1) …
  2) …
  3) …
- Risks / blockers:
  - …
- Opportunities:
  - …

### Action Queue (max 8 items)
| # | Action | Owner | Effort | Next step | Confidence |
|---|--------|-------|--------|-----------|------------|
| 1 | …      | …     | S/M/L  | …         | High/Med/Low |

### Assumptions
- Assumption: …

### What I need from you
- …

### Confirm to proceed
- Reply "CONFIRM SEND" to send/post, or "REVISE" with changes.
