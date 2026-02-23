# OpenClaw Starter Pack (Course Assets)

This repo contains the minimal "production-shaped" templates used in the 1-hour OpenClaw course:
- memory files (stable behavior + guardrails)
- one reusable skill scaffold
- demo prompts + example output

## Structure
- `memory/about_me.md` — your stable context and preferences
- `memory/operating_rules.md` — safety rules and tool boundaries
- `skills/run_daily_brief.skill.md` — end-to-end workflow scaffold
- `demos/` — copy/paste prompts + "what good looks like" output

## Safety first
✅ Do **not** commit secrets.  
Keep API keys in environment variables / a secrets manager.

## Quick start
1) Start OpenClaw (local Docker or VM)
2) Load memory files from `/memory`
3) Add the skill from `/skills`
4) Run: **`run_daily_brief for today (draft only)`**

## License
MIT (see LICENSE)
