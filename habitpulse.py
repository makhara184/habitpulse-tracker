#!/usr/bin/env python3
"""HabitPulse — Terminal Habit & Daily Streak Tracker with ASCII Heatmap."""

import argparse
import csv
import json
from datetime import date, timedelta
from pathlib import Path

DEFAULT_DB = Path("habits_data.json")


def load_db(db_path: Path) -> dict[str, list[str]]:
    if not db_path.exists():
        return {}
    return json.loads(db_path.read_text(encoding="utf-8"))


def save_db(db_path: Path, data: dict[str, list[str]]) -> None:
    db_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def log_habit(db_path: Path, name: str, day: str | None = None) -> list[str]:
    day_str = day or date.today().isoformat()
    data = load_db(db_path)
    entries = set(data.get(name, []))
    entries.add(day_str)
    data[name] = sorted(entries)
    save_db(db_path, data)
    return data[name]


def compute_streak(dates: list[str], reference: date | None = None) -> int:
    if not dates:
        return 0
    ref = reference or date.today()
    date_set = set(dates)
    streak = 0
    cursor = ref
    while cursor.isoformat() in date_set:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def render_heatmap(dates: list[str], days: int = 14, reference: date | None = None) -> str:
    ref = reference or date.today()
    date_set = set(dates)
    cells = []
    for offset in range(days - 1, -1, -1):
        d = (ref - timedelta(days=offset)).isoformat()
        cells.append("█" if d in date_set else "░")
    return "".join(cells)


def export_csv(db_path: Path, out_csv: Path) -> int:
    data = load_db(db_path)
    rows = 0
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Habit", "Date"])
        for habit, dates in sorted(data.items()):
            for d in dates:
                writer.writerow([habit, d])
                rows += 1
    return rows


def main():
    parser = argparse.ArgumentParser(description="HabitPulse — CLI Habit & Streak Tracker")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Path to JSON data file")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_log = sub.add_parser("log", help="Log a habit completion")
    p_log.add_argument("habit", help="Habit name")
    p_log.add_argument("--date", help="ISO date YYYY-MM-DD (defaults to today)")

    sub.add_parser("status", help="Show streaks and 14-day ASCII heatmaps")

    p_exp = sub.add_parser("export", help="Export all logs to CSV")
    p_exp.add_argument("output", type=Path, help="Output CSV path")

    args = parser.parse_args()
    if args.cmd == "log":
        entries = log_habit(args.db, args.habit, args.date)
        print(f"Logged '{args.habit}'. Total completions: {len(entries)} | Current streak: {compute_streak(entries)} day(s)")
    elif args.cmd == "status":
        data = load_db(args.db)
        if not data:
            print("No habits logged yet. Run: python3 habitpulse.py log 'Read 20 mins'")
            return
        for habit, dates in sorted(data.items()):
            streak = compute_streak(dates)
            bar = render_heatmap(dates, days=14)
            print(f"{habit:<22} {bar}  streak: {streak}d  total: {len(dates)}")
    elif args.cmd == "export":
        count = export_csv(args.db, args.output)
        print(f"Exported {count} log entries to {args.output}")


if __name__ == "__main__":
    main()
