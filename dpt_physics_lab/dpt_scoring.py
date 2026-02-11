from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class DPTAxisScore:
    name: str
    score: float
    rationale: str


@dataclass
class DPTScoreCard:
    s_p: DPTAxisScore
    omega_e: DPTAxisScore
    c_s: DPTAxisScore
    r_i: DPTAxisScore
    r_s: DPTAxisScore


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _consistency_score(definitions: Iterable[str]) -> float:
    defs = [d.strip().lower() for d in definitions if d.strip()]
    if not defs:
        return 0.3
    unique = len(set(defs))
    total = len(defs)
    return _clamp(1 - ((unique - 1) / max(total, 1)) * 0.4)


def score_claim_persistence(
    *,
    definitions: list[str],
    counterarguments_strength: float,
    argument_chain_quality: float,
    replication_count: int,
    decades_observed: int,
) -> DPTScoreCard:
    s_p_score = _consistency_score(definitions)
    omega_score = _clamp(1.0 - counterarguments_strength)
    c_s_score = _clamp(argument_chain_quality)
    r_i_score = _clamp(min(replication_count / 8.0, 1.0))
    r_s_score = _clamp(min(decades_observed / 5.0, 1.0))

    return DPTScoreCard(
        s_p=DPTAxisScore(
            name="S_p",
            score=s_p_score,
            rationale="Definitional consistency across cited, reputable sources.",
        ),
        omega_e=DPTAxisScore(
            name="Ω_e",
            score=omega_score,
            rationale="Lower unresolved counterargument pressure yields higher score.",
        ),
        c_s=DPTAxisScore(
            name="C_s",
            score=c_s_score,
            rationale="Internal coherence of theory-to-evidence argument chain.",
        ),
        r_i=DPTAxisScore(
            name="R_i",
            score=r_i_score,
            rationale="Independent cross-source and cross-team replication support.",
        ),
        r_s=DPTAxisScore(
            name="R_s",
            score=r_s_score,
            rationale="Persistence over decades and through method changes.",
        ),
    )
