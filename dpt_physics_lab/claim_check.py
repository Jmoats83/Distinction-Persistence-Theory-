from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from .dpt_scoring import score_claim_persistence


@dataclass
class Citation:
    title: str
    url: str
    source_type: str
    quality: str
    published: str
    accessed_utc: str


CLAIM_DB = {
    "gps time dilation": {
        "query_terms": ["gps", "time dilation", "sr", "clock"],
        "consensus": "mainstream consensus",
        "definitions": [
            "Special relativity predicts moving clocks run slower relative to inertial frame observers.",
            "GPS requires relativistic clock corrections (special and general relativity) to maintain navigation accuracy.",
        ],
        "claims": [
            {
                "type": "Definition",
                "text": "Time dilation is the rate difference between clocks in relative motion.",
            },
            {
                "type": "Theoretical prediction",
                "text": "Satellite clocks accumulate SR and GR offsets relative to Earth-bound clocks and need correction.",
            },
            {
                "type": "Experimental result",
                "text": "Operational GNSS systems continuously apply relativistic corrections verified by system performance.",
            },
            {
                "type": "Interpretation / narrative",
                "text": "Working GNSS timing provides real-world engineering confirmation of relativistic timing models.",
            },
        ],
        "counterarguments_strength": 0.05,
        "argument_chain_quality": 0.95,
        "replication_count": 10,
        "decades_observed": 5,
        "what_changes_score": [
            "A reproducible navigation/timing model that outperforms relativistic correction models across fleets.",
            "Consistent multi-lab evidence that relativistic corrections are unnecessary under equivalent precision tests.",
        ],
        "citations": [
            Citation(
                title="NIST: Relativity and the Global Positioning System",
                url="https://www.nist.gov/pml/time-and-frequency-division/popular-links/relativity-and-global-positioning-system",
                source_type="standards lab",
                quality="high",
                published="2010-01-01",
                accessed_utc=datetime.now(timezone.utc).isoformat(),
            ),
            Citation(
                title="Ashby (2003), Relativity in the Global Positioning System",
                url="https://doi.org/10.12942/lrr-2003-1",
                source_type="peer-reviewed review",
                quality="high",
                published="2003-02-01",
                accessed_utc=datetime.now(timezone.utc).isoformat(),
            ),
        ],
    },
    "entanglement ftl": {
        "query_terms": ["entanglement", "faster-than-light", "signaling", "no-signaling"],
        "consensus": "mainstream consensus",
        "definitions": [
            "Entanglement describes non-factorizable joint quantum states.",
            "No-signaling theorem forbids controllable superluminal information transfer via entanglement alone.",
        ],
        "claims": [
            {
                "type": "Definition",
                "text": "Entangled systems exhibit correlations exceeding classical bounds under Bell tests.",
            },
            {
                "type": "Theoretical prediction",
                "text": "Quantum theory predicts Bell inequality violations while still preserving no-signaling constraints.",
            },
            {
                "type": "Experimental result",
                "text": "Loophole-reduced Bell tests confirm nonclassical correlations without operational FTL signaling channels.",
            },
            {
                "type": "Interpretation / narrative",
                "text": "Entanglement challenges local realism interpretations but does not enable FTL messaging.",
            },
        ],
        "counterarguments_strength": 0.2,
        "argument_chain_quality": 0.9,
        "replication_count": 8,
        "decades_observed": 4,
        "what_changes_score": [
            "Demonstration of controllable one-way information transfer exceeding light-speed bounds.",
            "A replicated violation of no-signaling constraints under strict loophole controls.",
        ],
        "citations": [
            Citation(
                title="Nobel Prize 2022: Experiments with entangled photons",
                url="https://www.nobelprize.org/prizes/physics/2022/advanced-information/",
                source_type="scientific academy",
                quality="high",
                published="2022-10-01",
                accessed_utc=datetime.now(timezone.utc).isoformat(),
            ),
            Citation(
                title="Stanford Encyclopedia: Bell's Theorem",
                url="https://plato.stanford.edu/entries/bell-theorem/",
                source_type="scholarly reference",
                quality="medium-high",
                published="2023-01-01",
                accessed_utc=datetime.now(timezone.utc).isoformat(),
            ),
        ],
    },
    "decoherence": {
        "query_terms": ["decoherence", "classical emergence", "measurement problem"],
        "consensus": "active research",
        "definitions": [
            "Decoherence is environment-induced suppression of phase coherence in reduced system states.",
            "Decoherence explains emergence of effectively classical statistics in many contexts.",
        ],
        "claims": [
            {
                "type": "Definition",
                "text": "Decoherence is dynamical entanglement with environment causing interference terms to become inaccessible.",
            },
            {
                "type": "Theoretical prediction",
                "text": "Open-system dynamics predict basis-dependent decoherence times and pointer-state behavior.",
            },
            {
                "type": "Experimental result",
                "text": "Interference visibility decays with controlled coupling in many experimental platforms.",
            },
            {
                "type": "Interpretation / narrative",
                "text": "Decoherence addresses classical appearance but leaves foundational interpretation questions open.",
            },
        ],
        "counterarguments_strength": 0.35,
        "argument_chain_quality": 0.8,
        "replication_count": 6,
        "decades_observed": 3,
        "what_changes_score": [
            "A broadly replicated theory unifying decoherence with unique outcome selection.",
            "Experimental contradictions showing coherence persistence where decoherence predicts rapid loss.",
        ],
        "citations": [
            Citation(
                title="Schlosshauer (2005) Decoherence, the measurement problem, and interpretations",
                url="https://arxiv.org/abs/quant-ph/0312059",
                source_type="peer-reviewed review",
                quality="high",
                published="2005-01-01",
                accessed_utc=datetime.now(timezone.utc).isoformat(),
            ),
            Citation(
                title="MIT OpenCourseWare: Decoherence notes",
                url="https://ocw.mit.edu/",
                source_type="university",
                quality="medium",
                published="2020-01-01",
                accessed_utc=datetime.now(timezone.utc).isoformat(),
            ),
        ],
    },
}


def _choose_record(query: str) -> dict:
    q = query.lower()
    for record in CLAIM_DB.values():
        if any(term in q for term in record["query_terms"]):
            return record
    return CLAIM_DB["gps time dilation"]


def evaluate_query(query: str) -> dict:
    record = _choose_record(query)
    score = score_claim_persistence(
        definitions=record["definitions"],
        counterarguments_strength=record["counterarguments_strength"],
        argument_chain_quality=record["argument_chain_quality"],
        replication_count=record["replication_count"],
        decades_observed=record["decades_observed"],
    )

    return {
        "query": query,
        "consensus_status": record["consensus"],
        "claims": record["claims"],
        "dpt_scores": {
            "S_p": asdict(score.s_p),
            "Ω_e": asdict(score.omega_e),
            "C_s": asdict(score.c_s),
            "R_i": asdict(score.r_i),
            "R_s": asdict(score.r_s),
        },
        "what_would_change_score": record["what_changes_score"],
        "citations": [asdict(c) for c in record["citations"]],
    }
