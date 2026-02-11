from __future__ import annotations

from datetime import datetime, timezone


def physics_claim_report(payload: dict) -> str:
    lines = [
        f"# Physics Claim Report\n",
        f"Generated: {datetime.now(timezone.utc).isoformat()}\n",
        f"## Query\n{payload['query']}\n",
        f"## Consensus status\n{payload['consensus_status']}\n",
        "## Categorized claims",
    ]
    for claim in payload["claims"]:
        lines.append(f"- **{claim['type']}**: {claim['text']}")

    lines.append("\n## DPT axis scoring")
    for axis, detail in payload["dpt_scores"].items():
        lines.append(f"- **{axis}** = {detail['score']:.3f}: {detail['rationale']}")

    lines.append("\n## What would change this score")
    for item in payload["what_would_change_score"]:
        lines.append(f"- {item}")

    lines.append("\n## Citations")
    for c in payload["citations"]:
        lines.append(
            f"- {c['title']} ({c['source_type']}, quality={c['quality']}, published={c['published']}, accessed={c['accessed_utc']}): {c['url']}"
        )
    return "\n".join(lines) + "\n"


def clock_session_report(payload: dict) -> str:
    lines = [
        "# Clock Session Physics Report\n",
        f"Generated: {datetime.now(timezone.utc).isoformat()}\n",
        f"Session ID: {payload['session_id']}\n",
        "## Computed stats",
    ]
    for k, v in payload.items():
        if k == "session_id":
            continue
        lines.append(f"- **{k}**: {v}")

    lines.append("\n## Limitations and uncertainty")
    lines.append("- This pipeline characterizes timing persistence and confounders; it does not directly measure SR effects at terrestrial hobby-grade scales.")
    lines.append("- Report confidence depends on sensor quality, sampling cadence, and metadata completeness.")
    return "\n".join(lines) + "\n"
