from __future__ import annotations


TEMPLATES = [
    {
        "id": "holdover-vs-signal",
        "domain": "SR/timekeeping",
        "title": "Holdover vs Signal (negative control for SR-scale effects)",
        "goal": "Quantify local oscillator drift and recovery without claiming direct SR detection.",
        "required_gear": ["Master Clock A3", "GNSS antenna", "Laptop with logger"],
        "procedure": [
            "Run disciplined mode for baseline.",
            "Disconnect GNSS for fixed holdover windows (e.g., 5/15/30 min).",
            "Reconnect and log reacquisition behavior.",
        ],
        "data_to_record": ["offset", "state", "n_ok", "temperature", "timestamp"],
        "expected_signal_magnitude": "Holdover drift >> terrestrial SR shift; used to bound instrumentation noise floor.",
        "failure_modes": ["Multipath GNSS errors", "thermal transients", "logging jitter"],
        "dpt_interpretation": "Persistence appears as reproducible recovery and bounded plateau drift.",
    },
    {
        "id": "environment-perturbation",
        "domain": "SR/timekeeping",
        "title": "Temperature / motion / enclosure perturbation",
        "goal": "Estimate environment-driven Ω_e contributions and confounders.",
        "required_gear": ["Clock enclosure", "Temperature sensor", "Phone accelerometer"],
        "procedure": [
            "Record baseline 30 min.",
            "Apply one perturbation at a time (temperature step, light movement).",
            "Return to baseline and repeat for at least 3 cycles.",
        ],
        "data_to_record": ["offset", "enclosure_temp_c", "motion_index", "holdover state"],
        "expected_signal_magnitude": "Environmental effects likely dominate over SR-scale terrestrial effects.",
        "failure_modes": ["Simultaneous confounders", "sensor resolution limits"],
        "dpt_interpretation": "Noise persistence across cycles indicates robust estimate of Ω_e.",
    },
    {
        "id": "multi-source-phase",
        "domain": "SR/timekeeping",
        "title": "Multi-source NTP vs GNSS vs local oscillator phase-field",
        "goal": "Map phase stability and dropout sensitivity across independent time sources.",
        "required_gear": ["NTP-capable laptop", "GNSS receiver", "Local oscillator logs"],
        "procedure": [
            "Collect synchronized measurements from NTP, GNSS, and local oscillator.",
            "Introduce controlled network latency variation.",
            "Compare phase divergence and reconvergence signatures.",
        ],
        "data_to_record": ["ntp_offset", "gnss_offset", "local_offset", "latency_ms", "packet_loss"],
        "expected_signal_magnitude": "Network propagation effects measurable; SR-scale terms not directly resolvable in typical setup.",
        "failure_modes": ["Unsynchronized logging clocks", "NTP server instability"],
        "dpt_interpretation": "Cross-source agreement boosts R_i while dropout fragility lowers Ω_e score.",
    },
]


def list_templates(domain: str | None = None) -> list[dict]:
    if not domain:
        return TEMPLATES
    d = domain.lower()
    return [t for t in TEMPLATES if d in t["domain"].lower()]
