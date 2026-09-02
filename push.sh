#!/bin/bash
# Quick push script - run this inside gnawledge-prompts folder
# Usage: ./push.sh YOUR_GITHUB_USERNAME

USER=${1:-YOUR_USERNAME}
REPO="gnawledge-prompts"

git init
git add .
git commit -m "feat: tailored 24 prompts - domain hunting + automation + creator kits"
git branch -M main
git remote add origin https://github.com/$USER/$REPO.git 2>/dev/null || git remote set-url origin https://github.com/$USER/$REPO.git
echo "Now create empty repo https://github.com/new named $REPO then run:"
echo "git push -u origin main"
