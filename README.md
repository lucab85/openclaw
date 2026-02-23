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
- `docker-compose.yml` — one-command deploy
- `docs/azure-deploy.md` — full Azure VM walkthrough

## Safety first
✅ Do **not** commit secrets.  
Keep API keys in `.env` (excluded via `.gitignore`).  
Copy `.env.example` → `.env` and fill in your values.

## Quick start (Docker Compose)
1) Clone this repo
2) `cp .env.example .env` and fill in your API keys
3) `docker compose up -d`
4) Open `http://localhost:3000`
5) Load memory files, add the skill, run: **`run_daily_brief for today (draft only)`**

For a full Azure VM deploy, see [docs/azure-deploy.md](docs/azure-deploy.md).

## License
MIT (see LICENSE)
