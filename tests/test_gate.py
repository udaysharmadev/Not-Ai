import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "plugins/not-ai/tools"))
sys.path.insert(0, str(ROOT / "scripts"))

from not_ai_core.gate import evaluate  # noqa: E402
from not_ai_core.voice import compare as compare_voice  # noqa: E402
from not_ai_core.voice import profile as voice_profile  # noqa: E402
from benchmark import extract_deliverable  # noqa: E402
from benchmark import (  # noqa: E402
    expected_action_check,
    load_metadata,
    protected_fact_preservation,
    validate_metadata,
)
from diagnose import diagnose as diagnose_text  # noqa: E402
from flag_response import flag_table, ppv  # noqa: E402
from pairwise import append_record, blind_pair, build_display, protection_aid  # noqa: E402
from package_skill import bundle_bytes, read_frontmatter, validate as validate_skill  # noqa: E402
from longdoc import review as review_longdoc, split_sections  # noqa: E402
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

    def test_extended_participial_opener_is_reported(self):
        result = evaluate("By leveraging the cache, the team shipped on Tuesday.")
        rules = [item.rule for item in result.findings]
        self.assertIn("participial-opener-extended", rules)

    def test_mid_sentence_participle_is_reported(self):
        result = evaluate("It worked, ensuring faster loads for everyone today.")
        rules = [item.rule for item in result.findings]
        self.assertIn("mid-sentence-participle", rules)

    def test_vocab_stemming_counts_inflections(self):
        result = evaluate("She kept grappling with scale while showcasing the logs.")
        spans = {item.span for item in result.findings if item.rule == "tier-1-vocabulary"}
        self.assertIn("grapple", spans)
        spans_two = {item.span for item in result.findings if item.rule == "tier-2-vocabulary"}
        self.assertIn("showcase", spans_two)

    def test_markdown_links_are_not_bracket_slots(self):
        result = evaluate("See [the guide](https://example.com) for details on Tuesday.")
        self.assertFalse(any(item.rule == "bracket-slot" for item in result.findings))

    def test_bracket_prompts_are_still_reported(self):
        result = evaluate("The deploy improved [specific result] for the team on Tuesday.")
        self.assertTrue(any(item.rule == "bracket-slot" for item in result.findings))

    def test_code_is_masked_from_vocab_counts(self):
        result = evaluate("```\nresult = delve(x)\n```\n\nPlain prose here is calm.")
        self.assertFalse(any(item.rule == "tier-2-vocabulary" for item in result.findings))

    def test_abbreviation_does_not_split_sentence(self):
        result = evaluate("Dr. Smith arrived on Tuesday. She stayed for lunch.")
        self.assertEqual(result.counts["sentences"], 2)

    def test_short_conversational_post_has_no_contraction_prompt(self):
        result = evaluate("This is a formal note about a project.", "linkedin")
        self.assertFalse(any(item.rule == "contractions" for item in result.findings))

    def test_preserve_mode_matches_a_minimal_edit(self):
        original = (
            "The deploy finished on Tuesday. It is worth noting that the migration "
            "ran without errors. All 14 services reported healthy within four minutes. "
            "No customer traffic was affected during the window."
        )
        rewritten = (
            "The deploy finished on Tuesday. The migration ran without errors. "
            "All 14 services reported healthy within four minutes. "
            "No customer traffic was affected during the window."
        )
        check = expected_action_check(original, rewritten, "preserve")
        self.assertEqual(check["assessment"], "matched")

    def test_voice_comparison_reports_drift_dimensions(self):
        reference = "We shipped the fix after the alert. I checked the logs twice. "
        reference += "You can see the retry storm in the dashboard. It failed fast. " * 12
        draft = "Furthermore, the implementation of the methodology was comprehensive. " * 6
        comparison = compare_voice(reference, draft)
        self.assertIn("overall", comparison)
        self.assertGreaterEqual(comparison["drifted_dimensions"], 1)
        profile = voice_profile(reference)
        self.assertTrue(profile["word_count"] > 0)

    def test_diagnose_shape_without_rewriting(self):
        entry = diagnose_text("Furthermore, the team utilized a robust solution.", "linkedin")
        for key in ("genre", "keep", "revise", "missing", "intervention", "measured"):
            self.assertIn(key, entry)
        self.assertTrue(any(item["rule"] == "tier-2-vocabulary" for item in entry["revise"]))

    def test_longdoc_sections_split_on_headings(self):
        text = "# Alpha\n\n" + ("Prose here is calm and steady. " * 40) + "\n\n# Beta\n\nShort tail."
        sections = split_sections(text, 100)
        self.assertGreaterEqual(len(sections), 2)
        entry = review_longdoc(text, "technical", 100)
        self.assertEqual(entry["sections"], len(sections))
        self.assertIn("cross_section_repeats", entry)

    def test_flag_math_matches_worked_example(self):
        # 99% TPR, 1% FPR, 5% prevalence: 49.5 TP vs 9.5 FP -> PPV 0.839.
        self.assertAlmostEqual(ppv(0.99, 0.01, 0.05), 0.839, places=3)

    def test_flag_math_is_undefined_without_expected_flags(self):
        self.assertIsNone(ppv(0.0, 0.0, 0.05))

    def test_flag_math_rejects_bad_rates(self):
        with self.assertRaises(ValueError):
            ppv(1.5, 0.01, 0.05)
        with self.assertRaises(ValueError):
            flag_table(0.99, -0.1)

    def test_flag_table_covers_plausible_prevalences(self):
        rows = flag_table(0.95, 0.05)
        self.assertEqual([row["prevalence"] for row in rows], [0.01, 0.05, 0.10, 0.20, 0.50])
        by_prevalence = {row["prevalence"]: row for row in rows}
        # At 5% prevalence with 95%/5% rates, a flag is a coin flip.
        self.assertAlmostEqual(by_prevalence[0.05]["ppv"], 0.5, places=3)

    def test_readability_mismatch_fires_outside_genre_band(self):
        simple = ("The cat sat on the mat. It was warm and soft. " * 25).strip()
        entry = diagnose_text(simple, "technical")
        self.assertIn("flesch_kincaid_grade", entry["measured"])
        self.assertTrue(any(item["rule"] == "readability-mismatch" for item in entry["revise"]))

    def test_readability_band_skipped_on_short_text(self):
        entry = diagnose_text("The cat sat on the mat. It was warm.", "technical")
        self.assertNotIn("flesch_kincaid_grade", entry["measured"])
        self.assertFalse(any(item["rule"] == "readability-mismatch" for item in entry["revise"]))

    def test_pairwise_blinding_is_deterministic_per_seed(self):
        first_shown, first_map = blind_pair("aaa", "bbb", seed=7)
        second_shown, second_map = blind_pair("aaa", "bbb", seed=7)
        self.assertEqual(first_map, second_map)
        self.assertEqual(first_shown, second_shown)
        self.assertEqual(set(first_map.values()), {"A", "B"})

    def test_pairwise_display_hides_candidate_identities(self):
        shown, _ = blind_pair("alpha text here", "beta text here", seed=3)
        display = build_display("source text here", shown, {"purpose": "Test"}, ["alpha"])
        self.assertIn("CANDIDATE X", display)
        self.assertIn("CANDIDATE Y", display)
        self.assertNotIn("CANDIDATE A", display)
        self.assertNotIn("CANDIDATE B", display)
        self.assertIn("SOURCE (not a candidate", display)

    def test_protection_aid_is_literal_casefold(self):
        aid = protection_aid("The API v2 deploy.", ["API v2", "Nagpur"])
        self.assertEqual(aid, {"API v2": True, "Nagpur": False})

    def test_pairwise_record_appends_valid_jsonl(self):
        import json

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "round1.jsonl"
            append_record(path, {"mapping": {"X": "B", "Y": "A"}, "choice": "x"})
            record = json.loads(path.read_text(encoding="utf-8").strip())
            self.assertEqual(record["mapping"], {"X": "B", "Y": "A"})
            self.assertEqual(record["choice"], "x")

    def test_skill_bundle_validates_cleanly(self):
        self.assertEqual(validate_skill(), [])

    def test_skill_frontmatter_names_the_skill(self):
        skill = (ROOT / "plugins/not-ai/skills/not-ai/SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(read_frontmatter(skill).get("name"), "not-ai")

    def test_skill_bundle_is_deterministic(self):
        self.assertEqual(bundle_bytes(), bundle_bytes())


if __name__ == "__main__":
    unittest.main()
