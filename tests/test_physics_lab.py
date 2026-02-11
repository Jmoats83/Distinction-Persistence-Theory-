from pathlib import Path

from dpt_physics_lab.claim_check import evaluate_query
from dpt_physics_lab.data_ingest import ingest_clock_csv, report_for
from dpt_physics_lab.experiment_templates import list_templates


def test_claim_check_structure():
    result = evaluate_query("Does SR predict time dilation for GPS satellites?")
    assert result["consensus_status"] in {"mainstream consensus", "active research", "disputed"}
    assert len(result["claims"]) >= 4
    assert "S_p" in result["dpt_scores"]
    assert result["citations"]


def test_csv_ingest_and_report():
    path = Path(__file__).parent / "sample_clock.csv"
    report = ingest_clock_csv(path)
    loaded = report_for(report.session_id)
    assert loaded["sample_count"] == 5
    assert loaded["holdover_intervals"] == 2


def test_templates_include_required_items():
    templates = list_templates("SR")
    ids = {t["id"] for t in templates}
    assert {"holdover-vs-signal", "environment-perturbation", "multi-source-phase"}.issubset(ids)
