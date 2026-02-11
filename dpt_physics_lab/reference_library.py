from __future__ import annotations

import json
from pathlib import Path


LIB_PATH = Path(__file__).resolve().parent / "data" / "reference_library.json"


def _load() -> list[dict]:
    if not LIB_PATH.exists():
        return []
    return json.loads(LIB_PATH.read_text(encoding="utf-8"))


def _save(items: list[dict]) -> None:
    LIB_PATH.parent.mkdir(parents=True, exist_ok=True)
    LIB_PATH.write_text(json.dumps(items, indent=2), encoding="utf-8")


def add_reference(item: dict) -> dict:
    items = _load()
    item["id"] = len(items) + 1
    items.append(item)
    _save(items)
    return item


def list_references(tag: str | None = None) -> list[dict]:
    items = _load()
    if tag:
        return [i for i in items if tag.lower() in [t.lower() for t in i.get("tags", [])]]
    return items
