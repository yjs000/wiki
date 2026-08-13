#!/usr/bin/env python3
"""Pick one study question from the compact question bank."""
from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BANK_PATH = ROOT / "docs" / "question-bank" / "question-bank.json"
HISTORY_PATH = ROOT / "docs" / "question-bank" / "question-history.jsonl"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def recent_ids(limit: int) -> set[str]:
    if not HISTORY_PATH.exists():
        return set()
    lines = [line for line in HISTORY_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    ids = []
    for line in lines[-limit:]:
        try:
            ids.append(json.loads(line).get("id"))
        except json.JSONDecodeError:
            continue
    return {x for x in ids if x}


def choose_question(seed: int | None = None, recent_limit: int = 5) -> dict:
    payload = load_json(BANK_PATH)
    items = [q for q in payload.get("items", []) if q.get("status") != "passed" and not q.get("blocked_by")]
    if not items:
        raise SystemExit("No non-passed questions available")

    recent = recent_ids(recent_limit)
    candidates = [q for q in items if q.get("id") not in recent] or items
    earliest = min(int(q.get("stage_order", 999)) for q in candidates)
    stage_items = [q for q in candidates if int(q.get("stage_order", 999)) == earliest]
    top3 = sorted(stage_items, key=lambda q: (-int(q.get("weight", 1)), q.get("id", "")))[:3]
    rng = random.Random(seed)
    return rng.choice(top3)


def append_history(question: dict) -> None:
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "picked_at": datetime.now(timezone.utc).isoformat(),
        "id": question["id"],
        "stage_order": question["stage_order"],
        "axis": question["axis"],
        "status": question["status"],
        "question": question["question"],
    }
    with HISTORY_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int)
    parser.add_argument("--no-history", action="store_true", help="Do not append to question-history.jsonl")
    parser.add_argument("--recent-limit", type=int, default=5)
    args = parser.parse_args()

    q = choose_question(seed=args.seed, recent_limit=args.recent_limit)
    if not args.no_history:
        append_history(q)
    print(json.dumps(q, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
