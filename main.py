"""Job Posting Cleaner — main entry point.

Usage:
    python main.py                          # runs all postings in data/sample_postings.txt
    python main.py "paste a posting here"   # runs a single inline posting
"""

import sys
from pathlib import Path

from src.job_cleaner.graph import app


SAMPLE_FILE = Path(__file__).parent / "data" / "sample_postings.txt"


def initial_state(raw: str) -> dict:
    """Every key the graph reads must be seeded here."""
    return {
        "raw": raw,
        "role": "",
        "skills": [],
        "red_flags": [],
        "polished": "",
        "feedback": "",
        "score": 0,
        "attempts": 0,
    }


def clean_one(raw: str, label: str = "") -> dict:
    """Run the graph on a single posting, print a summary, return the state."""
    if label:
        print(f"\n{'=' * 60}\n{label}\n{'=' * 60}")

    result = app.invoke(initial_state(raw))

    print(f"\n[role]     {result['role']}")
    print(f"[skills]   {', '.join(result['skills']) or '(none)'}")
    print(f"[score]    {result['score']}   attempts={result['attempts']}")

    print(f"\n[flags]    {len(result['red_flags'])} found")
    for f in result["red_flags"]:
        print(f"           - {f}")

    print(f"\n[polished]\n{result['polished']}\n")
    return result


def main() -> None:
    # Case 1: inline posting from command line
    if len(sys.argv) > 1:
        raw = " ".join(sys.argv[1:])
        clean_one(raw, label="INLINE POSTING")
        return

    # Case 2: run every posting in the sample file
    if not SAMPLE_FILE.exists():
        print(f"Sample file not found: {SAMPLE_FILE}", file=sys.stderr)
        sys.exit(1)

    blocks = [
        b.strip()
        for b in SAMPLE_FILE.read_text(encoding="utf-8").split("\n---\n")
        if b.strip()
    ]

    print(f"Running {len(blocks)} sample postings from {SAMPLE_FILE.name}...")
    for i, block in enumerate(blocks, 1):
        clean_one(block, label=f"POSTING {i}/{len(blocks)}")


if __name__ == "__main__":
    main()