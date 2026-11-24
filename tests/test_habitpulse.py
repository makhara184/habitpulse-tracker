import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from habitpulse import compute_streak, export_csv, log_habit, render_heatmap


class TestHabitPulse(unittest.TestCase):
    def test_streak_and_heatmap(self):
        today = date(2026, 11, 24)
        days = [(today - timedelta(days=i)).isoformat() for i in range(3)]
        self.assertEqual(compute_streak(days, reference=today), 3)
        bar = render_heatmap(days, days=5, reference=today)
        self.assertEqual(bar, "░░███")

    def test_log_and_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "db.json"
            out = Path(tmp) / "out.csv"
            log_habit(db, "Walk 5km", "2026-11-23")
            log_habit(db, "Walk 5km", "2026-11-24")
            count = export_csv(db, out)
            self.assertEqual(count, 2)
            self.assertIn("Walk 5km,2026-11-24", out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
