
# gnawledge-prompts
### The Useful Prompt Library, Tailored for You

Fork of prompts.chat (167k+ stars) but rebuilt for actual work: **expired domain hunting, Spamzilla cleaning, GitHub Actions fixes, n8n automation, and faceless creator kits**.

> Original: [prompts.chat](https://prompts.chat) / [f/awesome-chatgpt-prompts](https://github.com/f/prompts.chat) - 24 curated from 167k

### What's different?
- **Old:** Largest = best, generic "Act as..."
- **New:** Smallest useful = 24 prompts you actually use daily
- Organized by your stack: Domain Hunting / SEO / GitHub Automation / Creator Kits / Lead Gen

### Quick Start

#### Use directly in Meta AI / Claude / ChatGPT
Copy any prompt from `prompts.csv` or `PROMPTS.md`, replace {variables}.

#### Self-host (like prompts.chat)
```bash
npx prompts.chat new my-library
# copy prompts.csv into it
cd my-library
npm install && npm run setup
```

#### MCP Server
```json
{
  "mcpServers": {
    "gnawledge-prompts": {
      "command": "npx",
      "args": ["-y", "prompts.chat", "mcp"]
    }
  }
}
```
Then point it at ./prompts.json

### Structure
- `prompts.csv` - spreadsheet version
- `prompts.json` - for MCP / apps
- `PROMPTS.md` - human-readable
- `index.html` - searchable web UI (from artifact)
- `.github/workflows/` - sample daily hunter that uses these prompts

### Categories
- **Domain Hunting**: 5 prompts
- **SEO & Spam Filter**: 3 prompts
- **Automation & GitHub**: 4 prompts
- **Automation & n8n**: 1 prompts
- **Creator & Faceless**: 4 prompts
- **Lead Gen**: 3 prompts
- **Work Smarter**: 4 prompts

### License
Code MIT, prompt content CC0 1.0 (same as upstream prompts.chat)

Built with prompts.chat ❤️


## hunter.py v4 Integrated (NEW)
This repo now includes your actual hunter - no more separate repo needed.

- **Spam filter (prompts #3 + #5)**: auto-drops `seoexpress`, `pbn`, `casino` + Wayback <3 snapshots
- **Quality score (prompt #1)**: REAL / MAYBE / SPAM + reason + year range
- **Collision-proof**: writes `daily-YYYY-MM-DD.csv`, `cad-YYYY-MM-DD.csv`, `audio-YYYY-MM-DD.csv` - 3 workflows can run at same time
- **Report (prompt #24)**: auto summary in Actions log

### How it fixes your last errors
- `No event triggers defined in on` -> fixed indents, LF, workflow_dispatch + schedule both present
- Audio worked but Daily+CAD failed -> fixed with unique filenames + concurrency groups
- seoexpress promo like audioproductionhub.com -> now filtered by Wayback count (2 snapshots = spam) + substring block

### Run locally
```
python hunter.py --facility daily
python hunter.py --facility cad
python hunter.py --facility audio
```
Finds in `finds/` folder.
