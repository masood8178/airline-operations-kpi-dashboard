import pandas as pd
from src.metrics import calculate_kpis, prepare_data


def test_kpis():
    df = pd.DataFrame({
        "date": ["2026-01-01", "2026-01-01", "2026-01-01"],
        "flight_id": ["A", "B", "C"],
        "arrival_delay_min": [5, 30, None],
        "cancelled": [False, False, True],
        "load_factor": [0.8, 0.9, 0.7],
    })
    df = prepare_data(df)
    kpis = calculate_kpis(df)
    assert kpis["flights"] == 3
    assert kpis["on_time_performance"] == 0.5
    assert round(kpis["avg_arrival_delay"], 1) == 17.5
    assert round(kpis["cancellation_rate"], 3) == 0.333
