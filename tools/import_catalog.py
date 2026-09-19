#!/usr/bin/env python3
"""Convert db-brasilia records into the stable offline iOS catalog contract."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_records(path: Path) -> list[dict]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise ValueError(f"expected an array: {path}")
    return value


def restaurant(record: dict) -> dict:
    return {
        "id": record.get("slug"),
        "name": record.get("nome"),
        "category": record.get("subcategoria"),
        "neighborhood": record.get("bairro"),
        "address": record.get("endereco"),
        "phone": record.get("telefone"),
        "website": record.get("site_oficial"),
        "rating": record.get("rating"),
        "review_count": record.get("review_count"),
        "source": record.get("source"),
        "source_url": record.get("source_url"),
        "last_verified": (record.get("scraped_at") or "")[:10],
        "data_status": "pending-rights-review",
    }


def clinic(record: dict) -> dict:
    return {
        "id": record.get("slug"),
        "name": record.get("nome"),
        "specialties": record.get("especialidades") or [],
        "neighborhood": record.get("bairro"),
        "address": record.get("endereco"),
        "city": record.get("cidade"),
        "state": record.get("uf"),
        "phone": record.get("telefone"),
        "whatsapp": record.get("whatsapp"),
        "email": record.get("email"),
        "maps_ref": record.get("maps_ref"),
        "source": record.get("source"),
        "source_url": record.get("source_url"),
        "last_verified": (record.get("scraped_at") or "")[:10],
        "data_status": "pending-editorial-review",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=("restaurants", "clinics"), required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    transform = restaurant if args.kind == "restaurants" else clinic
    output = [transform(record) for record in read_records(args.source)]
    output = [record for record in output if record["id"] and record["name"]]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(output)} records to {args.output}")


if __name__ == "__main__":
    main()
