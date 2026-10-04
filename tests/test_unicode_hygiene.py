"""Unicode hygiene tests: defensive measurement integrity, never bypass.

Covers the viral U+200B-join pattern plus multilingual negative controls
(Persian ZWNJ, emoji ZWJ, Thai ZWSP), mirror sync across the three normalize
implementations, and gate/diagnose/benchmark invariance under attack.
"""

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "plugins/not-ai/tools"))
sys.path.insert(0, str(ROOT / "scripts"))

from not_ai_core.unicode_hygiene import (  # noqa: E402
    normalize_for_analysis,
    render_report,
    scan,
)
from not_ai_core.gate import evaluate  # noqa: E402
from diagnose import diagnose as diagnose_text  # noqa: E402
from benchmark import token_overlap_similarity  # noqa: E402


def _load_measure():
    spec = importlib.util.spec_from_file_location(
        "measure_mirror", str(ROOT / "scripts" / "measure.py")
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["measure_mirror"] = module
    spec.loader.exec_module(module)
    return module


class UnicodeHygieneCoreTests(unittest.TestCase):
    def test_viral_zero_width_join_restores_visible_ascii_text_for_analysis(self):
        clean = "This assignment explains cache invalidation in simple terms."
        attacked = "\u200b".join(clean)
        self.assertNotEqual(clean, attacked)
        self.assertEqual(normalize_for_analysis(attacked), clean)
        report = scan(attacked)
        self.assertGreater(report["suspicious_for_analysis"], 0)
        self.assertEqual(report["by_kind"]["zero-width"], len(clean) - 1)

    def test_persian_zwnj_is_preserved(self):
        text = "می\u200cروم"
        self.assertEqual(normalize_for_analysis(text), text)
        report = scan(text)
        self.assertEqual(report["findings"][0]["risk"], "contextual")

    def test_emoji_zwj_is_preserved(self):
        text = "👩\u200d💻"
        self.assertEqual(normalize_for_analysis(text), text)
        self.assertEqual(scan(text)["findings"][0]["risk"], "contextual")

    def test_non_ascii_space_is_canonicalized_for_analysis(self):
        self.assertEqual(normalize_for_analysis("hello\u00a0world"), "hello world")

    def test_soft_hyphen_inside_ascii_word_is_removed_for_analysis(self):
        text = "cache\u00adcontrol"
        self.assertEqual(normalize_for_analysis(text), "cachecontrol")
        self.assertEqual(scan(text)["findings"][0]["risk"], "warning")

    def test_thai_zwsp_is_not_globally_removed(self):
        text = "ภาษา\u200bไทย"
        self.assertEqual(normalize_for_analysis(text), text)

    def test_normalize_is_idempotent(self):
        attacked = "\u200b".join("Cache keys expire nightly.")
        once = normalize_for_analysis(attacked)
        self.assertEqual(normalize_for_analysis(once), once)

    def test_clean_text_scans_empty(self):
        report = scan("The deploy finished on Tuesday. All 14 services healthy.")
        self.assertEqual(report["total"], 0)
        self.assertEqual(report["suspicious_for_analysis"], 0)

    def test_bidi_and_tag_controls_are_reviewed_and_removed_for_analysis(self):
        text = "Hello\u202eWorld\U000e0061"
        report = scan(text)
        self.assertTrue(all(item["risk"] == "review" for item in report["findings"]))
        self.assertEqual(normalize_for_analysis(text), "HelloWorld")

    def test_scripts_wrapper_reexports_core(self):
        import unicode_hygiene as wrapper

        self.assertIs(wrapper.normalize_for_analysis, normalize_for_analysis)
        self.assertIs(wrapper.scan, scan)


class UnicodeMirrorSyncTests(unittest.TestCase):
    BATTERY = [
        "Plain ASCII prose with no tricks.",
        "\u200b".join("This assignment explains cache invalidation in simple terms."),
        "hello\u00a0world",
        "cache\u00adcontrol",
        "می\u200cروم",
        "👩\u200d💻",
        "ภาษา\u200bไทย",
        "Hello\u202eWorld",
        "a\u200bb\u200cc\u200dd",
        "",
    ]

    def test_shared_fallback_and_measure_mirror_agree_with_core(self):
        from _shared import _fallback_normalize
        from not_ai_core.unicode_hygiene import (
            normalize_for_analysis as core_normalize,
        )

        measure = _load_measure()
        for text in self.BATTERY:
            self.assertEqual(
                _fallback_normalize(text), core_normalize(text), f"shared: {text!r}"
            )
            self.assertEqual(
                measure._normalize_for_analysis(text),
                core_normalize(text),
                f"measure: {text!r}",
            )


class UnicodeGateIntegrationTests(unittest.TestCase):
    CLEAN = "This assignment explains cache invalidation in simple terms."

    def test_gate_counts_invariant_under_zwsp_attack(self):
        attacked = "\u200b".join(self.CLEAN)
        clean = evaluate(self.CLEAN, "technical")
        under_attack = evaluate(attacked, "technical")
        self.assertEqual(under_attack.word_count, clean.word_count)
        self.assertEqual(
            under_attack.counts["sentences"], clean.counts["sentences"]
        )

    def test_gate_reports_hygiene_as_review_not_error(self):
        attacked = "\u200b".join(self.CLEAN)
        result = evaluate(attacked, "technical")
        hygiene = [item for item in result.findings if item.rule == "unicode-hygiene"]
        self.assertEqual(len(hygiene), 1)
        self.assertEqual(hygiene[0].severity, "review")
        self.assertTrue(result.passed)

    def test_gate_clean_text_has_no_hygiene_finding(self):
        result = evaluate(self.CLEAN, "technical")
        self.assertFalse(
            [item for item in result.findings if item.rule == "unicode-hygiene"]
        )
        self.assertNotIn("unicode-hygiene", render_report(scan(self.CLEAN)))

    def test_gate_provenance_explains_unicode_hygiene(self):
        from not_ai_core.rules import explain

        text = explain("unicode-hygiene")
        self.assertIn("What Not-AI does NOT do", text)


class UnicodeDiagnoseIntegrationTests(unittest.TestCase):
    CLEAN = "This assignment explains cache invalidation in simple terms."

    def test_diagnose_reports_hygiene_and_measures_clean_view(self):
        attacked = "\u200b".join(self.CLEAN)
        entry = diagnose_text(attacked, "technical")
        self.assertGreater(entry["unicode_hygiene"]["total"], 0)
        clean_entry = diagnose_text(self.CLEAN, "technical")
        self.assertEqual(entry["word_count"], clean_entry["word_count"])
        self.assertEqual(
            entry["measured"]["nominalizations_per_1000"],
            clean_entry["measured"]["nominalizations_per_1000"],
        )

    def test_diagnose_clean_text_reports_zero_hygiene(self):
        entry = diagnose_text(self.CLEAN, "technical")
        self.assertEqual(entry["unicode_hygiene"]["total"], 0)

    def test_benchmark_overlap_invariant_under_zwsp_attack(self):
        attacked = "\u200b".join(self.CLEAN)
        self.assertAlmostEqual(
            token_overlap_similarity(self.CLEAN, attacked), 1.0, places=3
        )


if __name__ == "__main__":
    unittest.main()
