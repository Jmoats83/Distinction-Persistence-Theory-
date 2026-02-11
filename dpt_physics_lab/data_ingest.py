from __future__ import annotations

import csv
import math
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import median


@dataclass
class SessionReport:
    session_id: str
    sample_count: int
    drift_slope_per_step: float
    rmse: float
    mad_sigma: float
    holdover_intervals: int
    regime_changes: int
    stable_plateaus: int
    recoveries_after_dropout: int
    sensitivity_to_enclosure: str
    dpt_interpretation: str


SESSIONS: dict[str, SessionReport] = {}


def _linear_slope(values: list[float]) -> float:
    n = len(values)
    if n < 2:
        return 0.0
    xs = list(range(n))
    x_mean = sum(xs) / n
    y_mean = sum(values) / n
    num = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, values))
    den = sum((x - x_mean) ** 2 for x in xs)
    return num / den if den else 0.0


def _rmse(values: list[float]) -> float:
    if not values:
        return 0.0
    mu = sum(values) / len(values)
    return math.sqrt(sum((v - mu) ** 2 for v in values) / len(values))


def _mad_sigma(values: list[float]) -> float:
    if not values:
        return 0.0
    med = median(values)
    mad = median([abs(v - med) for v in values])
    return 1.4826 * mad


def _regime_changes(values: list[float], threshold: float) -> int:
    if len(values) < 2:
        return 0
    return sum(1 for a, b in zip(values, values[1:]) if abs(b - a) > threshold)


def _holdover_count(quality_flags: list[str]) -> int:
    return sum(1 for f in quality_flags if f.lower() == "holdover")


def _recoveries(quality_flags: list[str]) -> int:
    drops = 0
    for prev, cur in zip(quality_flags, quality_flags[1:]):
        if prev.lower() == "holdover" and cur.lower() == "ok":
            drops += 1
    return drops


def ingest_clock_csv(path: str | Path) -> SessionReport:
    path = Path(path)
    offsets: list[float] = []
    quality_flags: list[str] = []
    enclosure: list[float] = []

    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            offsets.append(float(row.get("offset", 0.0)))
            quality_flags.append(row.get("state", "ok"))
            enclosure.append(float(row.get("enclosure_temp_c", 25.0)))

    slope = _linear_slope(offsets)
    rmse = _rmse(offsets)
    mad_sigma = _mad_sigma(offsets)
    change_threshold = max(mad_sigma * 3, 1e-9)
    regimes = _regime_changes(offsets, change_threshold)
    holdover = _holdover_count(quality_flags)
    recoveries = _recoveries(quality_flags)

    temp_rmse = _rmse(enclosure)
    sensitivity = "low" if temp_rmse < 1.0 else "medium" if temp_rmse < 3.0 else "high"

    stable_plateaus = max(0, len(offsets) // 50 - regimes)
    interpretation = (
        "Persistence signature indicates robust disciplined behavior with bounded noise."
        if rmse < 1e-3 and holdover < max(1, len(offsets) * 0.1)
        else "Persistence signature suggests environment or signal fragility dominates observed behavior."
    )

    report = SessionReport(
        session_id=str(uuid.uuid4()),
        sample_count=len(offsets),
        drift_slope_per_step=slope,
        rmse=rmse,
        mad_sigma=mad_sigma,
        holdover_intervals=holdover,
        regime_changes=regimes,
        stable_plateaus=stable_plateaus,
        recoveries_after_dropout=recoveries,
        sensitivity_to_enclosure=sensitivity,
        dpt_interpretation=interpretation,
    )

    SESSIONS[report.session_id] = report
    return report


def report_for(session_id: str) -> dict:
    report = SESSIONS[session_id]
    return asdict(report)


def compare_sessions(session_ids: list[str]) -> dict:
    reports = [SESSIONS[s] for s in session_ids]
    best = min(reports, key=lambda r: r.rmse)
    worst = max(reports, key=lambda r: r.rmse)
    return {
        "sessions": [asdict(r) for r in reports],
        "best_rmse_session": best.session_id,
        "worst_rmse_session": worst.session_id,
        "rmse_spread": worst.rmse - best.rmse,
    }
