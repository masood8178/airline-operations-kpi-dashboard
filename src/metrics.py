import pandas as pd


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["date"] = pd.to_datetime(data["date"])
    data["on_time"] = (~data["cancelled"]) & (data["arrival_delay_min"] <= 15)
    return data


def calculate_kpis(df: pd.DataFrame) -> dict:
    total = len(df)
    operated = df.loc[~df["cancelled"]]
    return {
        "flights": total,
        "on_time_performance": float(operated["on_time"].mean()) if len(operated) else 0.0,
        "avg_arrival_delay": float(operated["arrival_delay_min"].mean()) if len(operated) else 0.0,
        "cancellation_rate": float(df["cancelled"].mean()) if total else 0.0,
        "avg_load_factor": float(operated["load_factor"].mean()) if len(operated) else 0.0,
    }


def route_summary(df: pd.DataFrame) -> pd.DataFrame:
    operated = df.loc[~df["cancelled"]].copy()
    summary = (
        operated.groupby("route", as_index=False)
        .agg(
            flights=("flight_id", "count"),
            on_time_performance=("on_time", "mean"),
            avg_arrival_delay=("arrival_delay_min", "mean"),
            avg_load_factor=("load_factor", "mean"),
        )
        .sort_values(["flights", "on_time_performance"], ascending=[False, False])
    )
    return summary


def data_quality_report(df: pd.DataFrame) -> dict:
    required = [
        "date", "flight_id", "origin", "destination", "arrival_delay_min",
        "cancelled", "delay_cause", "load_factor"
    ]
    missing_columns = [c for c in required if c not in df.columns]
    duplicate_flights = int(df.duplicated(subset=["flight_id"]).sum()) if "flight_id" in df else 0
    missing_values = int(df[required].isna().sum().sum()) if not missing_columns else None
    return {
        "missing_columns": missing_columns,
        "duplicate_flights": duplicate_flights,
        "missing_required_values": missing_values,
    }
