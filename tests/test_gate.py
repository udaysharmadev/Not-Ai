import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "plugins/not-ai/tools"))
sys.path.insert(0, str(ROOT / "scripts"))

from not_ai_core.gate import evaluate  # noqa: E402
from benchmark import extract_deliverable  # noqa: E402
from benchmark import load_metadata, protected_fact_preservation  # noqa: E402


class GateTests(unittest.TestCase):
    def test_typography_is_the_only_hard_failure(self):
        result = evaluate("This is fine — except for the dash.")
        self.assertFalse(result.passed)
        self.assertEqual([item.severity for item in result.findings], ["error"])

    def test_conversational_contract_is_advisory(self):
        text = "This is a formal note about a project. " * 12
        result = evaluate(text, "linkedin")
        self.assertTrue(result.passed)
        self.assertTrue(any(item.rule == "contractions" for item in result.findings))

    def test_academic_profile_does_not_request_contractions(self):
        text = "This study examines a small sample. " * 12
        result = evaluate(text, "academic")
        self.assertFalse(any(item.rule == "contractions" for item in result.findings))

    def test_empty_text_fails(self):
        result = evaluate("", "technical")
        self.assertFalse(result.passed)
        self.assertEqual(result.findings[0].rule, "nonempty")

    def test_benchmark_excludes_editorial_wrappers(self):
        wrapped = "counts: dashes 0\n\n```\nOnly the final prose.\n```\n\n[FLAG: review this]"
        self.assertEqual(extract_deliverable(wrapped), "Only the final prose.")

    def test_benchmark_rejects_non_string_protected_facts(self):
        pair = ROOT / "tests/.metadata-fixture"
        pair.mkdir(exist_ok=True)
        try:
            (pair / "metadata.json").write_text('{"protected_facts": [1]}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_metadata(pair)
        finally:
            (pair / "metadata.json").unlink(missing_ok=True)
            pair.rmdir()

    def test_protected_fact_check_requires_review_for_a_missing_literal(self):
        check = protected_fact_preservation("The event happened on Tuesday.", ["Tuesday", "Nagpur"])
        self.assertEqual(check["missing_literal_facts"], ["Nagpur"])


if __name__ == "__main__":
    unittest.main()
