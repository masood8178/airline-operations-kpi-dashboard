# Airline Operations KPI Dashboard
<img width="942" height="527" alt="Screenshot 2026-08-26 013148" src="https://github.com/user-attachments/assets/1fec6afd-e477-4cbb-acb1-cee1dfe35503" />



A compact data-platform portfolio project built to demonstrate **operational analysis, KPI reporting, dashboard development, data quality checks, and process-oriented thinking**.

> **Data note:** All flight-operation records in this repository are synthetic and generated locally. No Lufthansa internal, customer, or confidential data is used.

## What it shows

- On-time performance (arrival within 15 minutes)
- Average arrival delay
- Cancellation rate
- Average load factor
- Daily performance trend
- Delay-cause distribution
- Route-level performance table
- Basic data-quality checks
- Interactive filters for date, origin, and route
<img width="955" height="528" alt="image" src="https://github.com/user-attachments/assets/4501ff25-554b-4be2-a079-e043d6ce6e3c" />
## Tech stack

- Python
- Pandas / NumPy
- Plotly
- Streamlit
- Pytest

## Why I built it

The project mirrors a common IT/data-platform workflow: take operational data, validate it, define meaningful KPIs, create repeatable reporting, and expose the results in a simple tool that helps users identify performance issues quickly.

It is intentionally small. The goal is not to build a full airline platform, but to demonstrate how I approach an analytical request from **data → metrics → dashboard → validation**.

## Project structure

```text
lufthansa-it-data-dashboard/
├── app.py
├── data/
│   └── flight_operations.csv
├── src/
│   ├── generate_data.py
│   └── metrics.py
├── tests/
│   └── test_metrics.py
├── requirements.txt
└── README.md
```

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/generate_data.py
streamlit run app.py
```

## Run tests

```bash
pytest -q
```

## Possible next steps

- Add automated CSV schema validation
- Add configurable KPI thresholds and alerts
- Store historical runs in SQLite/PostgreSQL
- Export a weekly KPI report
- Add a small API endpoint for downstream reporting tools
