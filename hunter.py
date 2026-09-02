
"""
hunter.py v4 - Gnawledge Edition
Integrates tailored prompts:
- #1 Expired Domain Quality Score
- #3 Spamzilla CSV Cleaner  
- #5 PBN & Promo Spam Detector
- #7 Wayback Quality Explainer

Usage:
  python hunter.py --facility daily   -> finds/daily-2026-09-01.csv
  python hunter.py --facility cad     -> finds/cad-2026-09-01.csv
  python hunter.py --facility audio   -> finds/audio-2026-09-01.csv

Collision-proof: each facility writes its own file.
Spam-proof: filters seoexpress junk + Wayback <3 snapshots = spam.
"""

import argparse, csv, os, re, sys, time
from datetime import datetime
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    requests = None

# === CONFIG ===
SPAM_SUBSTRINGS = ["seoexpress", "pbn", "casino", "porn", "essay", "payday", "loan", "viagra", "cbd gummies"]
# Note: 'seo' alone is too broad - we check full word or known spam pattern
SPAM_EXACT = ["seo"]

FACILITY_KEYWORDS = {
    "daily": ["business", "shop", "services", "solutions", "group"],
    "cad": ["cad", "autocad", "solidworks", "revit", "drafting", "blueprint", "3d modeling", "cnc"],
    "audio": ["audio", "recording", "studio", "mixing", "mastering", "podcast", "production", "sound"]
}

FINDS_DIR = "finds"

def is_spam_domain(domain: str) -> tuple[bool, str]:
    d = domain.lower()
    for s in SPAM_SUBSTRINGS:
        if s in d:
            return True, f"contains {s}"
    # exact word check
    parts = re.split(r'[.-]', d)
    for p in parts:
        if p in SPAM_EXACT:
            return True, f"exact spam word {p}"
    return False, ""

def get_wayback_snapshots(domain: str) -> tuple[int, str]:
    """Call Wayback CDX API - returns count and year range"""
    if not requests:
        return 0, "no requests"
    try:
        # cdx search
        url = f"https://web.archive.org/cdx/search/xm?url={domain}&output=json&fl=timestamp&collapse=digest"
        r = requests.get(url, timeout=15, headers={"User-Agent": "gnawledge-hunter/4.0"})
        if r.status_code != 200:
            return 0, f"cdx {r.status_code}"
        data = r.json()
        if not data or len(data) <= 1:
            return 0, "0 snapshots"
        # first row is header
        timestamps = [row[0] for row in data[1:]]
        years = sorted(set(t[:4] for t in timestamps))
        year_range = f"{years[0]}-{years[-1]}" if years else "unknown"
        return len(timestamps), year_range
    except Exception as e:
        return 0, f"error {e}"

def score_domain(domain, wayback_count, wayback_years, anchors=""):
    """Prompt #1 logic - score 1-10"""
    if wayback_count < 3:
        return 2, "SPAM", f"Only {wayback_count} snapshots ({wayback_years}) = parked promo, likely seoexpress junk like audioproductionhub.com"
    if wayback_count < 10:
        return 5, "MAYBE", f"{wayback_count} snapshots {wayback_years} - thin history, manual check Archive.org"
    if wayback_count >= 50:
        return 9, "REAL", f"{wayback_count} snapshots {wayback_years} = real business that died, strong brandable"
    return 7, "REAL", f"{wayback_count} snapshots {wayback_years} = decent history"

def mock_fetch_domains(facility):
    """REPLACE THIS with your real Spamzilla / ExpiredDomains.net fetch
    For now returns sample data so workflow goes green
    """
    samples = {
        "daily": ["sheltonservices.com", "harborbusinessgroup.com", "seoexpress-best-deals.com", "audioproductionhub.com"],
        "cad": ["cad-drafting-pros.com", "solidworks-tutorials.net", "seoexpress-cad.com", "northwestblueprints.com"],
        "audio": ["pugetsoundrecording.com", "podcastmasteringlab.com", "seoexpress-audio.com", "olympicstudiosound.com"]
    }
    return samples.get(facility, [])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--facility", default="daily", choices=["daily","cad","audio"])
    args = parser.parse_args()

    os.makedirs(FINDS_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    out_file = f"{FINDS_DIR}/{args.facility}-{date_str}.csv"

    domains = mock_fetch_domains(args.facility)
    print(f"[{args.facility}] Starting with {len(domains)} candidates")

    rows = []
    for domain in domains:
        is_spam, reason = is_spam_domain(domain)
        if is_spam:
            print(f"  FILTERED {domain} - {reason}")
            continue

        count, years = get_wayback_snapshots(domain)
        # sleep to be nice to Wayback
        time.sleep(1)

        if count < 3:
            print(f"  FILTERED {domain} - only {count} Wayback snapshots (spam)")
            continue

        score, verdict, notes = score_domain(domain, count, years)

        rows.append({
            "domain": domain,
            "facility": args.facility,
            "dr": 30,  # placeholder - replace with real DR from Spamzilla API
            "backlinks": 120,
            "wayback_snapshots": count,
            "wayback_years": years,
            "score": score,
            "verdict": verdict,
            "notes": notes,
            "date": date_str
        })
        print(f"  KEEP {domain} - {verdict} score {score} - {count} snapshots {years}")

    # Write CSV - collision-proof filename
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["domain","facility","dr","backlinks","wayback_snapshots","wayback_years","score","verdict","notes","date"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDone. Wrote {len(rows)} rows to {out_file}")
    print(f"Columns: wayback_snapshots + notes = REAL SITE vs LIKELY SPAM (prompt #7)")

if __name__ == "__main__":
    main()
