import unittest

from monthly_calendar.date_utils import MonthView, adjacent_month, normalize_year_month
from monthly_calendar.renderer import CalendarRenderer


class DateUtilsTests(unittest.TestCase):
    def test_normalize_handles_overflow_month(self):
        view = normalize_year_month(2025, 13)
        self.assertEqual((view.year, view.month), (2026, 1))

    def test_previous_month_wraps_year(self):
        dec = MonthView(2025, 1)
        prev_month = adjacent_month(dec, -1)
        self.assertEqual((prev_month.year, prev_month.month), (2024, 12))


class RendererTests(unittest.TestCase):
    def test_renders_header_and_navigation_links(self):
        html = CalendarRenderer().render(year=2026, month=2)
        self.assertIn("2026-02", html)
        self.assertIn("year=2026&amp;month=1", html)
        self.assertIn("year=2026&amp;month=3", html)

    def test_renders_expected_day_count(self):
        html = CalendarRenderer().render(year=2024, month=2)  # leap year
        # count literal day cells; ensure 29 appears and 30 doesn't
        self.assertIn(">29<", html)
        self.assertNotIn(">30<", html)


if __name__ == "__main__":
    unittest.main()
