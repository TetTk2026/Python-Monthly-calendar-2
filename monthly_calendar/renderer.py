"""HTML rendering for a monthly calendar."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from urllib.parse import urlencode

from .date_utils import MonthView, adjacent_month, normalize_year_month


@dataclass
class CalendarRenderer:
    week_labels: tuple[str, ...] = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

    def render(self, year: int | None = None, month: int | None = None) -> str:
        view = normalize_year_month(year, month)
        return self._build_page(view)

    def _build_page(self, view: MonthView) -> str:
        prev_view = adjacent_month(view, -1)
        next_view = adjacent_month(view, 1)
        body = self._build_calendar_table(view)

        title = f"{view.year:04d}-{view.month:02d}"
        prev_href = self._query_href(prev_view)
        next_href = self._query_href(next_view)

        return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />
  <title>{escape(title)} Monthly Calendar</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; color: #222; }}
    .header {{ display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }}
    .header a {{ text-decoration: none; color: #0b61ff; }}
    table {{ border-collapse: collapse; width: 100%; max-width: 780px; }}
    th, td {{ border: 1px solid #ccc; padding: 0.65rem; text-align: center; }}
    th {{ background: #f5f7fa; }}
    td.empty {{ background: #fafafa; }}
  </style>
</head>
<body>
  <div class=\"header\">
    <a href=\"{escape(prev_href)}\">&larr; Prev</a>
    <h1>{escape(title)}</h1>
    <a href=\"{escape(next_href)}\">Next &rarr;</a>
  </div>
  {body}
</body>
</html>"""

    def _query_href(self, view: MonthView) -> str:
        return f"/?{urlencode({'year': view.year, 'month': view.month})}"

    def _build_calendar_table(self, view: MonthView) -> str:
        headers = "".join(f"<th>{escape(label)}</th>" for label in self.week_labels)
        days_html = self._build_day_cells(view)
        return f"<table><thead><tr>{headers}</tr></thead><tbody>{days_html}</tbody></table>"

    def _build_day_cells(self, view: MonthView) -> str:
        start_offset = view.start_weekday_monday_first
        total_cells = start_offset + view.days_in_month
        trailing = (7 - total_cells % 7) % 7
        full_cells = total_cells + trailing

        rows: list[str] = []
        current_day = 1
        for cell_index in range(full_cells):
            if cell_index % 7 == 0:
                rows.append("<tr>")

            if cell_index < start_offset or current_day > view.days_in_month:
                rows.append('<td class="empty"></td>')
            else:
                rows.append(f"<td>{current_day}</td>")
                current_day += 1

            if cell_index % 7 == 6:
                rows.append("</tr>")

        return "".join(rows)
