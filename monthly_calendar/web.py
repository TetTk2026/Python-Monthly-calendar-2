"""WSGI app entrypoint for the monthly calendar."""

from __future__ import annotations

from urllib.parse import parse_qs

from .renderer import CalendarRenderer


def app(environ, start_response):
    params = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=False)

    def parse_int(name: str):
        raw = params.get(name, [None])[0]
        if raw in (None, ""):
            return None
        try:
            return int(raw)
        except ValueError:
            return None

    year = parse_int("year")
    month = parse_int("month")

    html = CalendarRenderer().render(year=year, month=month)
    body = html.encode("utf-8")

    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(body)))])
    return [body]
