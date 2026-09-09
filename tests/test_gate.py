import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "plugins/not-ai/tools"))
sys.path.insert(0, str(ROOT / "scripts"))

from not_ai_core.gate import evaluate  # noqa: E402
from benchmark import extract_deliverable  # noqa: E402
from benchmark import (  # noqa: E402
    expected_action_check,
    load_metadata,
    protected_fact_preservation,
    validate_metadata,
)
from scan_prose import scan as scan_repository_prose  # noqa: E402


class GateTests(unittest.TestCase):
    def test_typography_is_advisory_by_default(self):
        result = evaluate("She called it “finished” — then revised it.")
        self.assertTrue(result.passed)
        self.assertEqual([item.severity for item in result.findings], ["review", "review"])

    def test_ascii_house_style_can_make_typography_blocking(self):
        result = evaluate("This is fine — except for the dash.", ascii_punctuation=True)
        self.assertFalse(result.passed)
        self.assertEqual([item.severity for item in result.findings], ["error"])

    def test_missing_explicitly_protected_text_is_blocking(self):
        result = evaluate(
            "The deploy finished on Tuesday.",
            "technical",
            protected_terms=["Tuesday", "Nagpur"],
        )
        self.assertFalse(result.passed)
        missing = [item.span for item in result.findings if item.rule == "protected-content"]
        self.assertEqual(missing, ["Nagpur"])

    def test_protected_terms_must_be_nonempty_strings(self):
        with self.assertRaises(ValueError):
            evaluate("Text", protected_terms=[""])

    def test_conversational_contract_is_advisory(self):
        text = "This is a formal note about a project. " * 12
        result = evaluate(text, "linkedin")
        self.assertTrue(result.passed)
        self.assertTrue(any(item.rule == "contractions" for item in result.findings))

    def test_academic_profile_does_not_request_contractions(self):
        text = "This study examines a small sample. " * 12
        result = evaluate(text, "academic")
        self.assertFalse(any(item.rule == "contractions" for item in result.findings))

    def test_student_profile_flags_choppy_report_prose(self):
        text = (
            "The input was noisy. Slang caused problems. Typos broke the parser. "
            "Emojis confused the tokenizer. The classifier still returned a label."
        )
        result = evaluate(text, "student")
        self.assertTrue(result.passed)
        self.assertEqual(result.counts["max_consecutive_short"], 5)
        self.assertTrue(any(item.rule == "choppy-run" for item in result.findings))

    def test_social_profile_allows_a_short_sentence_run(self):
        text = "It failed. We waited. Nothing changed. So we rolled back."
        result = evaluate(text, "social")
        self.assertFalse(any(item.rule == "choppy-run" for item in result.findings))

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

    def test_metadata_validates_human_output_context(self):
        validate_metadata({
            "genre": "technical",
            "purpose": "Explain why the deploy was rolled back.",
            "audience": "On-call engineers",
            "expected_action": "preserve",
            "intervention_mode": "preserve",
            "source": {"kind": "synthetic"},
            "review": {"fidelity": 5, "editorial_restraint": 4},
        })

    def test_metadata_rejects_fabricated_review_scale(self):
        with self.assertRaises(ValueError):
            validate_metadata({"review": {"reader_usefulness": 100}})

    def test_no_change_case_records_unwanted_rewrite(self):
        check = expected_action_check("Keep this.", "Rewrite this.", "no-change")
        self.assertEqual(check["assessment"], "review required: text changed")

    def test_repository_scan_allows_style_and_catches_generator_residue(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.md"
            path.write_text("A nuanced answer — with “curly quotes”.", encoding="utf-8")
            self.assertEqual(scan_repository_prose(path), [])
            path.write_text("Leaked token: turn4search2", encoding="utf-8")
            self.assertEqual(len(scan_repository_prose(path)), 1)

    def test_repository_scan_skips_input_specimens_cleanly(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.md"
            path.write_text("Leaked specimen token: turn4search2", encoding="utf-8")
            self.assertEqual(scan_repository_prose(path), [])


if __name__ == "__main__":
    unittest.main()
