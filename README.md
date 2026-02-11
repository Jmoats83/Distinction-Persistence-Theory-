# DPT Physics & Reality Lab (MVP)

This update adds a modular physics/science workspace that applies the existing DPT scoring lens to claims, references, and clock data.

## Included modes

- Physics Claim Check (QM/SR/GR-oriented queries)
- Experiment Designer (SR/timekeeping templates)
- Data Ingest + Compare (CSV/log analysis)
- Reference Library (saved source records with tags)
- Clock → Physics Bridge (educational SR context + timing indicators)

## Run

```bash
pip install fastapi uvicorn pydantic python-multipart
uvicorn dpt_physics_lab.app:app --reload --port 8000
```

Open: <http://localhost:8000>

## API endpoints

- `POST /api/physics/claim_check`
- `GET /api/physics/experiment_templates`
- `POST /api/physics/ingest_log`
- `GET /api/physics/report/{session_id}`
- `POST /api/physics/compare_sessions`
- `GET /api/physics/clock_bridge`
- `GET /api/physics/qm/glossary`
- `POST /api/physics/reference`
- `GET /api/physics/reference`
- `POST /api/physics/export/claim_markdown`
- `GET /api/physics/export/session_markdown/{session_id}`

## Notes

- Claim checking is citation-driven and explicitly separates definition/prediction/result/interpretation.
- Scores are uncertainty-aware and include “what would change this score.”
- Clock reports are framed as persistence/noise characterization and do not overstate direct SR detectability.
