"""Date helpers for monthly calendar rendering."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class MonthView:
    year: int
    month: int

    @property
    def first_day(self) -> date:
        return date(self.year, self.month, 1)

    @property
    def days_in_month(self) -> int:
        if self.month == 12:
            next_month = date(self.year + 1, 1, 1)
        else:
            next_month = date(self.year, self.month + 1, 1)
        return (next_month - self.first_day).days

    @property
    def start_weekday_monday_first(self) -> int:
        """Return weekday index with Monday as 0 and Sunday as 6."""
        return self.first_day.weekday()


def normalize_year_month(year: int | None, month: int | None, today: date | None = None) -> MonthView:
    """Normalize incoming year/month to a valid month view.

    If either value is missing, current date is used.
    """
    current = today or date.today()
    normalized_year = current.year if year is None else int(year)
    normalized_month = current.month if month is None else int(month)

    while normalized_month < 1:
        normalized_year -= 1
        normalized_month += 12
    while normalized_month > 12:
        normalized_year += 1
        normalized_month -= 12

    return MonthView(year=normalized_year, month=normalized_month)


def adjacent_month(view: MonthView, offset: int) -> MonthView:
    """Return adjacent month by offset (-1 for previous, +1 for next)."""
    return normalize_year_month(view.year, view.month + offset)
