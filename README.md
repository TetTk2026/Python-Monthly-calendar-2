# Python Monthly Calendar

This repository contains a Python rewrite of a typical PHP monthly-calendar implementation.

## What's included

- `monthly_calendar/date_utils.py` – date/navigation helpers that replace PHP date arithmetic.
- `monthly_calendar/renderer.py` – HTML calendar rendering that replaces PHP template components.
- `monthly_calendar/web.py` – lightweight WSGI web entrypoint that replaces a PHP page controller.
- `run.py` – local launch script.

## Run locally

```bash
python run.py
```

Then open: <http://127.0.0.1:8000/?year=2026&month=2>

## Run tests

```bash
python -m unittest discover -s tests
```
