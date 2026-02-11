from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .claim_check import evaluate_query
from .data_ingest import compare_sessions, ingest_clock_csv, report_for
from .experiment_templates import list_templates
from .qm_module import CLAIM_EXPLORER, QM_GLOSSARY
from .reference_library import add_reference, list_references
from .reporting import clock_session_report, physics_claim_report

app = FastAPI(title="DPT Physics & Reality Lab", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ClaimQuery(BaseModel):
    query: str = Field(..., description="Physics claim question")


class CompareQuery(BaseModel):
    session_ids: list[str]


class ReferenceIn(BaseModel):
    title: str
    url: str
    tags: list[str] = []
    notes: str = ""
    dpt_notes: str = ""


@app.get("/")
def home() -> FileResponse:
    return FileResponse(Path(__file__).resolve().parent / "static" / "index.html")


@app.post("/api/physics/claim_check")
def physics_claim_check(payload: ClaimQuery) -> dict:
    return evaluate_query(payload.query)


@app.get("/api/physics/experiment_templates")
def experiment_templates(domain: str | None = None) -> dict:
    return {"templates": list_templates(domain)}


@app.post("/api/physics/ingest_log")
async def ingest_log(file: UploadFile = File(...)) -> dict:
    suffix = Path(file.filename or "upload.csv").suffix or ".csv"
    temp_path = Path("/tmp") / f"dpt_upload_{file.filename or 'clock'}{suffix}"
    content = await file.read()
    temp_path.write_bytes(content)

    try:
        report = ingest_clock_csv(temp_path)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {exc}") from exc
    return {"session_id": report.session_id, "report": report_for(report.session_id)}


@app.get("/api/physics/report/{session_id}")
def session_report(session_id: str) -> dict:
    try:
        return report_for(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Unknown session_id") from exc


@app.post("/api/physics/compare_sessions")
def compare(payload: CompareQuery) -> dict:
    try:
        return compare_sessions(payload.session_ids)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown session_id: {exc}") from exc


@app.get("/api/physics/clock_bridge")
def clock_bridge() -> dict:
    return {
        "local_utc_geo_time": "Expose from Master Clock adapter in production.",
        "discipline_state": "disciplined / holdover / reacquire",
        "propagation_latency_sensitivity_indicator": "derived from NTP/GNSS divergence",
        "environment_stress_indicator": "composite(temp variance, motion index, dropout rate)",
        "sr_expectations": {
            "label": "Educational context; not direct detection claim",
            "summary": "SR predicts moving clocks run slower; terrestrial everyday speeds produce tiny shifts below common hobby-grade detection thresholds.",
            "citations": [
                "https://www.nist.gov/pml/time-and-frequency-division/popular-links/relativity-and-global-positioning-system",
                "https://doi.org/10.12942/lrr-2003-1",
            ],
        },
    }


@app.get("/api/physics/qm/glossary")
def qm_glossary() -> dict:
    return {"glossary": QM_GLOSSARY, "claim_explorer": CLAIM_EXPLORER}


@app.post("/api/physics/reference")
def create_reference(payload: ReferenceIn) -> dict:
    return add_reference(payload.model_dump())


@app.get("/api/physics/reference")
def get_reference(tag: str | None = None) -> dict:
    items = list_references(tag)
    return {"items": items}


@app.post("/api/physics/export/claim_markdown")
def export_claim_markdown(payload: ClaimQuery) -> dict:
    result = evaluate_query(payload.query)
    return {"markdown": physics_claim_report(result)}


@app.get("/api/physics/export/session_markdown/{session_id}")
def export_session_markdown(session_id: str) -> dict:
    data = report_for(session_id)
    return {"markdown": clock_session_report(data)}
