from pathlib import Path
import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
AIRPORTS = ["FRA", "MUC", "BER", "HAM", "DUS", "VIE", "ZRH", "AMS"]
DELAY_CAUSES = ["Weather", "Late inbound", "ATC", "Technical", "Ground handling", "No delay"]


def generate_dataset(rows: int = 900) -> pd.DataFrame:
    dates = pd.date_range("2026-06-01", periods=60, freq="D")
    scheduled = RNG.choice(dates, rows)
    origins = RNG.choice(AIRPORTS, rows)
    destinations = RNG.choice(AIRPORTS, rows)
    same = origins == destinations
    while same.any():
        destinations[same] = RNG.choice(AIRPORTS, same.sum())
        same = origins == destinations

    cancelled = RNG.random(rows) < 0.035
    departure_delay = np.maximum(0, RNG.normal(11, 17, rows)).round(0)
    arrival_delay = np.maximum(0, departure_delay + RNG.normal(-2, 9, rows)).round(0)
    departure_delay[cancelled] = np.nan
    arrival_delay[cancelled] = np.nan

    delay_cause = RNG.choice(DELAY_CAUSES, rows, p=[0.12, 0.24, 0.15, 0.10, 0.14, 0.25])
    delay_cause[(~cancelled) & (np.nan_to_num(arrival_delay) <= 15)] = "No delay"
    delay_cause[cancelled] = RNG.choice(["Weather", "Technical", "ATC"], cancelled.sum())

    passengers = RNG.integers(70, 220, rows)
    load_factor = np.clip(RNG.normal(0.84, 0.08, rows), 0.55, 0.99)

    df = pd.DataFrame({
        "date": scheduled,
        "flight_id": [f"LH{1000+i}" for i in range(rows)],
        "origin": origins,
        "destination": destinations,
        "scheduled_minutes": RNG.integers(55, 210, rows),
        "departure_delay_min": departure_delay,
        "arrival_delay_min": arrival_delay,
        "cancelled": cancelled,
        "delay_cause": delay_cause,
        "passengers": passengers,
        "load_factor": load_factor.round(3),
    })
    df["route"] = df["origin"] + "-" + df["destination"]
    df = df.sort_values(["date", "flight_id"]).reset_index(drop=True)
    return df


def main() -> None:
    out = Path(__file__).resolve().parents[1] / "data" / "flight_operations.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df = generate_dataset()
    df.to_csv(out, index=False)
    print(f"Wrote {len(df)} synthetic rows to {out}")


if __name__ == "__main__":
    main()
