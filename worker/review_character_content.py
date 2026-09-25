#!/usr/bin/env python3
"""JERV editorial review for character facts and shared game questions.

This worker evaluates submitted claims against supplied source excerpts and
rates question clarity. It does not discover facts or treat model confidence as
proof. Deterministic app validation remains a separate release gate.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API = os.environ.get("TYPESAFE_ENDPOINT", "https://api.typesafe.ai/v1/systemone")
MODEL = "jev-latest"
RELATION_OPTIONS = {
    "supports": "The cited source excerpt explicitly supports the proposed factual claim.",
    "contradicts": "The cited source excerpt explicitly states a conflicting fact.",
    "insufficient": "The excerpt does not establish the claim either way, or is too ambiguous.",
}
CLARITY_OPTIONS = {
    "clear": "A casual player can understand the question and answer it about a person without specialized knowledge.",
    "ambiguous": "Key wording has multiple reasonable meanings, or the answer depends on interpretation.",
    "not_answerable": "The question asks for opinion, a changing fact without a reference date, or information a player cannot reasonably know.",
}


def load_input(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("input root must be an object")
    questions = data.get("questions")
    claims = data.get("claims")
    if not isinstance(questions, list) or not isinstance(claims, list):
        raise ValueError("input must contain questions and claims arrays")

    question_ids: set[str] = set()
    for item in questions:
        if not isinstance(item, dict):
            raise ValueError("each question must be an object")
        for field in ("id", "text", "category", "attribute"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(f"question is missing {field}")
        if item["id"] in question_ids:
            raise ValueError(f"duplicate question id: {item['id']}")
        question_ids.add(item["id"])

    claim_ids: set[str] = set()
    for item in claims:
        if not isinstance(item, dict):
            raise ValueError("each claim must be an object")
        for field in ("id", "person_id", "person_name", "claim", "source_url", "source_title", "source_excerpt", "source_license", "source_license_url", "last_verified"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(f"claim is missing {field}")
        if item["id"] in claim_ids:
            raise ValueError(f"duplicate claim id: {item['id']}")
        if item.get("question_id") and item["question_id"] not in question_ids:
            raise ValueError(f"claim {item['id']} references unknown question {item['question_id']}")
        if not item["source_url"].startswith(("https://", "http://")):
            raise ValueError(f"claim {item['id']} source_url must be http(s)")
        if not item["source_license_url"].startswith(("https://", "http://")):
            raise ValueError(f"claim {item['id']} source_license_url must be http(s)")
        if item.get("answer") not in (0, 0.0, 0.5, 1, 1.0):
            raise ValueError(f"claim {item['id']} answer must be 0, 0.5 or 1")
        claim_ids.add(item["id"])
    return data


def build_payload(questions: list[dict[str, Any]], claims: list[dict[str, Any]]) -> dict[str, Any]:
    state = {"questions": questions, "claims": claims}
    typed_questions: dict[str, dict[str, Any]] = {}
    for index, question in enumerate(questions):
        typed_questions[f"clarity_{index}"] = {
            "type": "choice",
            "instructions": {
                "question": f"Evaluate the player-facing wording of `questions[{index}].text` for `questions[{index}].category`.",
                "criterion": "Judge whether an ordinary player can answer it based on the person they have in mind. Do not judge factual values in the catalog.",
            },
            "criteria": CLARITY_OPTIONS,
        }
    for index, claim in enumerate(claims):
        typed_questions[f"evidence_{index}"] = {
            "type": "choice",
            "instructions": {
                "question": f"How does `claims[{index}].source_excerpt` relate to `claims[{index}].claim`?",
                "criterion": "Use only the supplied excerpt. A person's unsourced absence from a page is not evidence that a claim is false.",
            },
            "criteria": RELATION_OPTIONS,
        }
    return {"state": state, "model": MODEL, "questions": typed_questions}


def call_typesafe(payload: dict[str, Any], *, api_key: str | None = None, timeout: int = 180) -> dict[str, Any]:
    key = api_key or os.environ.get("TYPESAFE_API_KEY", "")
    if not key:
        raise RuntimeError("TYPESAFE_API_KEY is not configured")
    request = Request(
        API,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(4):
        try:
            with urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code not in (429, 529) or attempt == 3:
                raise
            delay = int(error.headers.get("Retry-After", "0") or 0)
            time.sleep(delay or (2**attempt))
        except URLError:
            if attempt == 3:
                raise
            time.sleep(2**attempt)
    raise RuntimeError("TypeSafe request retries exhausted")


def evaluate(
    data: dict[str, Any],
    request: Callable[[dict[str, Any]], dict[str, Any]] = call_typesafe,
    *,
    confidence_threshold: float = 0.8,
    batch_size: int = 12,
) -> dict[str, Any]:
    questions = data["questions"]
    claims = data["claims"]
    claim_reviews: dict[str, dict[str, Any]] = {}
    question_reviews: dict[str, dict[str, Any]] = {}

    for start in range(0, max(len(claims), len(questions)), batch_size):
        claim_batch = claims[start : start + batch_size]
        question_batch = questions[start : start + batch_size]
        if not claim_batch and not question_batch:
            continue
        response = request(build_payload(question_batch, claim_batch))
        answers = response.get("answers", {})
        for index, question in enumerate(question_batch):
            answer = answers.get(f"clarity_{index}", {})
            decision = answer.get("choice", "insufficient")
            confidence = float(answer.get("confidence", 0.0) or 0.0)
            question_reviews[question["id"]] = {
                "decision": decision,
                "confidence": confidence,
                "status": "accepted" if decision == "clear" and confidence >= confidence_threshold else "human-review",
            }
        for index, claim in enumerate(claim_batch):
            answer = answers.get(f"evidence_{index}", {})
            decision = answer.get("choice", "insufficient")
            confidence = float(answer.get("confidence", 0.0) or 0.0)
            claim_reviews[claim["id"]] = {
                "decision": decision,
                "confidence": confidence,
                "status": "accepted" if decision == "supports" and confidence >= confidence_threshold else "human-review",
                "source_url": claim["source_url"],
                "source_license": claim["source_license"],
                "source_license_url": claim["source_license_url"],
                "last_verified": claim["last_verified"],
            }

    return {
        "model": MODEL,
        "confidence_threshold": confidence_threshold,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "question_reviews": question_reviews,
        "claim_reviews": claim_reviews,
        "summary": {
            "questions_accepted": sum(item["status"] == "accepted" for item in question_reviews.values()),
            "questions_for_human": sum(item["status"] != "accepted" for item in question_reviews.values()),
            "claims_accepted": sum(item["status"] == "accepted" for item in claim_reviews.values()),
            "claims_for_human": sum(item["status"] != "accepted" for item in claim_reviews.values()),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--confidence-threshold", type=float, default=0.8)
    parser.add_argument("--batch-size", type=int, default=12)
    args = parser.parse_args(argv)
    if not 0 <= args.confidence_threshold <= 1:
        parser.error("--confidence-threshold must be between 0 and 1")
    if args.batch_size < 1:
        parser.error("--batch-size must be at least 1")
    try:
        report = evaluate(load_input(args.input), confidence_threshold=args.confidence_threshold, batch_size=args.batch_size)
    except (OSError, ValueError, RuntimeError, HTTPError, URLError) as error:
        print(f"JERV character review failed: {error}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False))
    print(f"JERV review report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
