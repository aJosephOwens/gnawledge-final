
# How to Push - 2 options

## Option 1: GitHub Desktop (easiest, you already use it)
1. Open GitHub Desktop -> File -> Add Local Repository -> Choose the `gnawledge-prompts` folder
2. It will say "This directory does not appear to be a Git repository" -> click "create a repository"
3. Bottom: Commit message: `feat: tailored 24 prompts - domain hunting + automation`
4. Top: Click "Publish repository" -> Name: `gnawledge-prompts` -> Uncheck Private if you want public -> Publish
5. Done. Your site will be at https://USERNAME.github.io/gnawledge-prompts/ if you enable Pages

## Option 2: Git CLI
```bash
cd gnawledge-prompts
git init
git add .
git commit -m "feat: tailored 24 prompts - domain hunting + automation"
git branch -M main
# Create empty repo on github.com first named gnawledge-prompts, then:
git remote add origin https://github.com/YOUR_USERNAME/gnawledge-prompts.git
git push -u origin main
```

## Enable GitHub Pages for the UI
Repo -> Settings -> Pages -> Source: Deploy from main branch / root -> Save
Then your searchable library lives at https://YOUR_USERNAME.github.io/gnawledge-prompts/

## Self-host like prompts.chat
```bash
npx prompts.chat new my-library
cp prompts.csv my-library/data/
cd my-library
npm install && npm run setup
```

## MCP (use inside Claude / Cursor)
```json
{
  "mcpServers": {
    "gnawledge-prompts": {
      "command": "npx",
      "args": ["-y", "prompts.chat", "mcp"],
      "env": {
        "PROMPTS_FILE": "./prompts.json"
      }
    }
  }
}
```
