import unittest

from worker.review_character_content import build_payload, evaluate, load_input


def sample():
    return {
        "questions": [{
            "id": "basketball",
            "text": "É jogador profissional de basquete?",
            "category": "Outros esportes",
            "attribute": "basketball",
        }],
        "claims": [{
            "id": "lebron-basketball",
            "person_id": "lebron-james",
            "person_name": "LeBron James",
            "question_id": "basketball",
            "answer": 1,
            "claim": "LeBron James é jogador profissional de basquete.",
            "source_url": "https://example.org/lebron",
            "source_title": "LeBron James biography",
            "source_excerpt": "LeBron James is an American professional basketball player.",
            "source_license": "CC BY-SA 4.0",
            "source_license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "last_verified": "2026-09-24",
        }],
    }


class CharacterContentReviewTests(unittest.TestCase):
    def test_payload_uses_typed_question_for_both_clarity_and_evidence(self):
        payload = build_payload(sample()["questions"], sample()["claims"])
        self.assertEqual(payload["model"], "jev-latest")
        self.assertEqual(payload["questions"]["clarity_0"]["type"], "choice")
        self.assertEqual(payload["questions"]["evidence_0"]["type"], "choice")
        self.assertIn("source_excerpt", payload["questions"]["evidence_0"]["instructions"]["question"])

    def test_input_requires_source_and_question_reference(self):
        data = sample()
        self.assertEqual(len(load_input_value(data)["claims"]), 1)
        data["claims"][0]["source_excerpt"] = ""
        with self.assertRaisesRegex(ValueError, "source_excerpt"):
            load_input_value(data)

    def test_uncertain_or_contradictory_answers_route_to_human(self):
        response = {
            "answers": {
                "clarity_0": {"choice": "clear", "confidence": 0.95},
                "evidence_0": {"choice": "insufficient", "confidence": 0.91},
            }
        }
        report = evaluate(sample(), lambda _: response)
        self.assertEqual(report["question_reviews"]["basketball"]["status"], "accepted")
        self.assertEqual(report["claim_reviews"]["lebron-basketball"]["status"], "human-review")

    def test_supported_high_confidence_claim_is_accepted(self):
        response = {
            "answers": {
                "clarity_0": {"choice": "clear", "confidence": 0.91},
                "evidence_0": {"choice": "supports", "confidence": 0.93},
            }
        }
        report = evaluate(sample(), lambda _: response)
        self.assertEqual(report["claim_reviews"]["lebron-basketball"]["status"], "accepted")


def load_input_value(data):
    import json
    from pathlib import Path
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as directory:
        path = Path(directory) / "review.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return load_input(path)


if __name__ == "__main__":
    unittest.main()
