"""Not-AI 4.0 regression and unit tests: punctuation & prosody engine,
controlled robustness lab (Conditions A-H), tricky token-protection edge cases,
7-layer intervention selector, and evaluation/score-sheet analytics."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "plugins/not-ai/tools"))
sys.path.insert(0, str(ROOT / "scripts"))

from not_ai_core.evaluation import (  # noqa: E402
    analyze_score_sheet,
    bootstrap_ci,
    check_vendor_length_eligibility,
    evaluate_passage_pair,
    load_score_rows,
    word_edit_distance_ratio,
)
from not_ai_core.gate import evaluate as gate_evaluate  # noqa: E402
from not_ai_core.intervention import select_intervention  # noqa: E402
from not_ai_core.punctuation import (  # noqa: E402
    analyze_punctuation,
    compare_punctuation_voice,
    detect_boundary_anomalies,
    prosody_profile,
)
from not_ai_core.robustness import (  # noqa: E402
    exact_diff,
    generate_experimental_conditions,
    measure_variant_impact,
    punctuation_variants,
    tokens,
    verify_word_sequence,
)
from not_ai_core.rules import explain  # noqa: E402
from not_ai_core.voice import compare as compare_voice, profile as voice_profile  # noqa: E402


class PunctuationAndProsodyEngineTests(unittest.TestCase):
    def test_modi_70_vs_80_boundary_and_prosody_diagnosis(self):
        modi_70 = (ROOT / "benchmarks/robustness/modi_case_study/modi_70_human.txt").read_text(encoding="utf-8")
        modi_80 = (ROOT / "benchmarks/robustness/modi_case_study/modi_80_human.txt").read_text(encoding="utf-8")

        p70 = analyze_punctuation(modi_70, "student")
        p80 = analyze_punctuation(modi_80, "student")

        self.assertFalse(p70["boundaries"]["has_boundary_damage"])
        self.assertTrue(p80["boundaries"]["has_boundary_damage"])
        self.assertTrue(p80["boundaries"]["fused_sentences"])
        self.assertTrue(p80["boundaries"]["tight_ellipsis_boundaries"])
        self.assertEqual(p80["boundaries"]["terminal_omission_status"], "boundary_loss")

        # Gate also surfaces punctuation-boundary-damage on modi_80 but not modi_70
        g70 = gate_evaluate(modi_70, "student")
        g80 = gate_evaluate(modi_80, "student")
        self.assertFalse(any(f.rule == "punctuation-boundary-damage" for f in g70.findings))
        self.assertTrue(any(f.rule == "punctuation-boundary-damage" for f in g80.findings))

    def test_intentional_informality_in_social_vs_academic_boundary_loss(self):
        casual = "missed the 7:40 local from Dadar... still made the 9 a.m. review on time"
        social_res = analyze_punctuation(casual, "social")
        x_res = analyze_punctuation(casual, "x")
        acad_res = analyze_punctuation(casual, "academic")

        self.assertEqual(social_res["boundaries"]["terminal_omission_status"], "intentional_informality")
        self.assertFalse(social_res["boundaries"]["has_boundary_damage"])
        self.assertFalse(x_res["boundaries"]["has_boundary_damage"])
        self.assertEqual(acad_res["boundaries"]["terminal_omission_status"], "boundary_loss")
        self.assertTrue(acad_res["boundaries"]["has_boundary_damage"])
        self.assertTrue(any(f["rule"] == "punctuation-genre-mismatch" for f in acad_res["findings"]))

    def test_prosody_detects_uniform_period_only_cadence_and_intro_commas(self):
        uniform = (
            "The script started at midnight on Sunday. "
            "The worker copied the database to storage. "
            "The network saturated after twelve minutes. "
            "The replica lag climbed on the follower. "
            "The engineer throttled the batch worker. "
            "The replica lag dropped within four minutes. "
            "The migration finished with zero lost rows."
        )
        rep = analyze_punctuation(uniform, "technical")
        self.assertTrue(rep["prosody"]["uniform_cadence"])

        front_loaded = (
            "In the morning, we checked the logs. "
            "After lunch, we rotated the keys. "
            "Before dinner, we drained the node. "
            "During the night, we watched the alerts. "
            "By Tuesday, we closed the ticket."
        )
        rep_intro = analyze_punctuation(front_loaded, "technical")
        self.assertGreaterEqual(rep_intro["prosody"]["introductory_comma_rate"], 0.8)
        self.assertTrue(any(f["rule"] == "prosodic-cadence" for f in rep_intro["findings"]))

    def test_punctuation_voice_comparison_and_voice_profile_integration(self):
        ref = (
            "We shipped the patch; it held under load, and p99 stayed below 4.2 ms (even in ap-south-1). "
            "Why guess when the trace is right there? Check the log; verify the epoch; move on. "
        ) * 14
        draft_aligned = (
            "We tested the replica; it held under load, and lag stayed below 5.0 ms (even on node 2). "
            "Why wait when the metric is clear? Check the trace; verify the lock; ship it. "
        ) * 4
        draft_flat = (
            "The system was tested under load. The latency remained low across all nodes. "
            "The logs were inspected by the team. The deployment completed on schedule. "
        ) * 4

        cmp_aligned = compare_punctuation_voice(ref, draft_aligned, "technical")
        cmp_flat = compare_punctuation_voice(ref, draft_flat, "technical")
        self.assertEqual(cmp_aligned["overall"], "aligned")
        self.assertEqual(cmp_flat["overall"], "drifted")

        v_prof = voice_profile(ref)
        self.assertIn("punctuation_habits", v_prof)
        v_cmp = compare_voice(ref, draft_flat)
        self.assertIn("punctuation_habits", v_cmp)


class RobustnessAndEdgeCaseTests(unittest.TestCase):
    def test_ablation_prototype_compatibility(self):
        a = "Narendra Modi is in India. Many people think so, but not all."
        variants = punctuation_variants(a)
        self.assertTrue(all(tokens(v) == tokens(a) for v in variants.values()))
        self.assertGreaterEqual(len(set(variants.values())), 6)
        self.assertTrue(all("\u200b" not in v and "\u200d" not in v for v in variants.values()))

    def test_tricky_edge_cases_preserve_decimals_dates_urls_citations_abbreviations_code(self):
        tricky = (
            "On 17 September 1950 (and 2026-10-30 at 2:14 a.m.), Dr. J. K. Rao and Prof. U.S. Patel "
            "measured 3.14% packet loss across 1,420 nodes (Dugan et al., 2024; Huang et al., 2024) [1, 2]. "
            "They ran `cachectl --rate 0.05` against https://internal.example.org/v2.4/status.json, "
            'and Mira called the result "boring, but 100.0% deterministic."'
        )
        variants = punctuation_variants(tricky)
        for name, candidate in variants.items():
            check = verify_word_sequence(tricky, candidate)
            self.assertTrue(check["words_identical"], f"Failed word sequence on {name}: {candidate}")
            self.assertTrue(check["decimals_intact"], f"Corrupted decimals on {name}: {candidate}")
            self.assertIn("3.14%", candidate, f"Lost 3.14% in {name}")
            self.assertIn("1,420", candidate, f"Lost 1,420 in {name}")
            self.assertIn("https://internal.example.org/v2.4/status.json", candidate, f"Corrupted URL in {name}")
            self.assertIn("`cachectl --rate 0.05`", candidate, f"Corrupted code span in {name}")

    def test_experimental_conditions_A_through_H_generation(self):
        modi_70 = (ROOT / "benchmarks/robustness/modi_case_study/modi_70_human.txt").read_text(encoding="utf-8")
        conds = generate_experimental_conditions(modi_70, genre="student")
        for expected_key in (
            "A_control",
            "B1_delete_commas",
            "B2_delete_terminal_period",
            "B3_double_terminal_period",
            "B4_replace_stop_with_ellipsis",
            "B5_drop_one_sentence_stop",
            "B6_remove_all_periods",
            "B_punctuation_only",
            "C_lexical_syntactic",
            "D_combined_edits",
            "E_whitespace_only",
            "F_sentence_segmentation",
            "G_genre_aware_editorial",
            "H_voice_matched",
        ):
            self.assertIn(expected_key, conds)

        # Every word-preserving condition must have exact token identity
        for name, item in conds.items():
            if item["preserves_word_sequence_by_design"]:
                self.assertTrue(item["impact"]["word_sequence_preserved"], name)

    def test_modi_comparison_reproduces_exact_segmentation_and_cv_shift(self):
        modi_70 = (ROOT / "benchmarks/robustness/modi_case_study/modi_70_human.txt").read_text(encoding="utf-8")
        modi_80 = (ROOT / "benchmarks/robustness/modi_case_study/modi_80_human.txt").read_text(encoding="utf-8")
        impact = measure_variant_impact(modi_70, modi_80, genre="student")
        self.assertTrue(impact["word_sequence_preserved"])
        self.assertEqual(impact["word_count_before"], 100)
        self.assertEqual(impact["word_count_after"], 100)
        self.assertEqual(impact["sentence_count_before"], 8)
        self.assertEqual(impact["sentence_count_after"], 6)
        self.assertGreater(impact["sentence_cv_after"], impact["sentence_cv_before"] + 0.15)
        self.assertTrue(impact["damages_grammar"])
        self.assertFalse(impact["damages_meaning"])


class SevenLayerInterventionAndEvaluationTests(unittest.TestCase):
    def test_seven_layer_intervention_selector_modes_and_levels(self):
        clean_social = "missed the 7:40 local from Dadar... caught the 7:52 instead, still made the 9 a.m. review"
        sel_clean = select_intervention(clean_social, genre="social", mode="rewrite")
        self.assertEqual(sel_clean["level"], "NONE")
        self.assertIn("layer_4_punctuation_prosody", sel_clean["layers"])

        blocked_notes = "Deploy [metric 1] on [date 2] for [team 3] after [event 4]."
        sel_blocked = select_intervention(blocked_notes, genre="technical", mode="from-notes")
        self.assertEqual(sel_blocked["short_level"], "BLOCKED")
        self.assertEqual(sel_blocked["level"], "BLOCKED_BY_MISSING_INFORMATION")

        preserve_plan = select_intervention(
            "Furthermore, the team utilized a robust solution on Tuesday.",
            genre="linkedin",
            mode="preserve",
        )
        self.assertIn(preserve_plan["level"], ("LIGHT", "MODERATE"))

    def test_vendor_length_eligibility_enforces_turnitin_300w_floor(self):
        short_elig = check_vendor_length_eligibility(100, "Turnitin")
        self.assertFalse(short_elig["eligible_for_detector"])
        self.assertFalse(short_elig["eligible_for_official_turnitin"])
        self.assertIn("300", short_elig["caution"])

        long_elig = check_vendor_length_eligibility(340, "Turnitin")
        self.assertTrue(long_elig["eligible_for_detector"])
        self.assertTrue(long_elig["eligible_for_official_turnitin"])

    def test_score_sheet_analysis_and_bootstrap_ci(self):
        rows = load_score_rows(ROOT / "benchmarks/robustness/modi_case_study/observed_scores.csv")
        summary = analyze_score_sheet(rows)
        self.assertEqual(summary["scored_rows"], 5)
        self.assertEqual(len(summary["punctuation_isolated_deltas"]), 1)
        self.assertEqual(summary["punctuation_isolated_deltas"][0]["human_score_delta"], 10.0)
        self.assertEqual(len(summary["between_detector_disagreement"]), 2)

        ci = bootstrap_ci([0.10, 0.14, 0.18, 0.12, 0.16], stat="mean")
        self.assertIsNotNone(ci["estimate"])
        self.assertLessEqual(ci["ci95_low"], ci["estimate"])
        self.assertGreaterEqual(ci["ci95_high"], ci["estimate"])

    def test_new_rules_have_provenance_explanations(self):
        for rule_id in (
            "punctuation-boundary-damage",
            "punctuation-genre-mismatch",
            "punctuation-fragment-review",
            "punctuation-uniformity",
            "prosodic-cadence",
        ):
            text = explain(rule_id)
            self.assertIn("What Not-AI does NOT do", text)
            self.assertIn("Research:", text)

    def test_cli_punctuation_audit_and_robustness_lab(self):
        proc1 = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/punctuation_audit.py"),
                str(ROOT / "benchmarks/robustness/modi_case_study/modi_80_human.txt"),
                "--genre",
                "student",
                "--json",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc1.returncode, 0, proc1.stderr)
        data1 = json.loads(proc1.stdout)
        self.assertTrue(data1["boundaries"]["has_boundary_damage"])

        with tempfile.TemporaryDirectory() as tmpdir:
            proc2 = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/robustness_lab.py"),
                    "generate",
                    str(ROOT / "benchmarks/robustness/modi_case_study/modi_70_human.txt"),
                    "--out",
                    tmpdir,
                    "--genre",
                    "student",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc2.returncode, 0, proc2.stderr)
            gen_info = json.loads(proc2.stdout)
            self.assertTrue(gen_info["words_unchanged_on_punctuation_probes"])
            # Blank score sheet analysis returns awaiting_manual_observations cleanly
            blank_summary = analyze_score_sheet(load_score_rows(Path(tmpdir) / "score_sheet.csv"))
            self.assertEqual(blank_summary["status"], "awaiting_manual_observations")


if __name__ == "__main__":
    unittest.main()
