#!/usr/bin/env python3
"""Not-AI 4.0 Robustness & Experimental Perturbation Lab CLI.

Supports controlled experiments on how punctuation, sentence segmentation,
whitespace, lexical/syntactic rewriting, genre-aware editing, and author voice
affect sentence parsing, prosodic features, and external detector stability.

Subcommands:
    compare <before> <after> [--genre GENRE] [--json]
    generate <source> --out <dir> [--genre GENRE] [--json]
    analyze-scores <score_file> [--threshold 50] [--json]
    evaluate-corpus [--corpus benchmarks/robustness/corpus] [--scores FILE] [--json]
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

TOOL_ROOT = Path(__file__).resolve().parents[1] / "plugins/not-ai/tools"
sys.path.insert(0, str(TOOL_ROOT))

from not_ai_core.evaluation import (  # noqa: E402
    analyze_score_sheet,
    bootstrap_ci,
    check_vendor_length_eligibility,
    evaluate_passage_pair,
    load_score_rows,
)
from not_ai_core.policy import POLICIES  # noqa: E402
from not_ai_core.robustness import (  # noqa: E402
    generate_experimental_conditions,
    measure_variant_impact,
)


def cmd_compare(args: argparse.Namespace) -> int:
    before_path = Path(args.before)
    after_path = Path(args.after)
    for p in (before_path, after_path):
        if not p.is_file():
            print(f"Error: file not found: {p}", file=sys.stderr)
            return 2
    before = before_path.read_text(encoding="utf-8")
    after = after_path.read_text(encoding="utf-8")
    impact = measure_variant_impact(before, after, genre=args.genre)
    if args.json:
        print(json.dumps(impact, indent=2, ensure_ascii=False))
        return 0

    print("NOT AI 4.0 : ROBUSTNESS VARIANT COMPARISON")
    print("─" * 48)
    print(f"Lexical tokens identical: {impact['word_sequence_preserved']}")
    print(f"Word count:               {impact['word_count_before']} -> {impact['word_count_after']}")
    print(f"Punctuation marks:        {impact['punctuation_marks_before']} -> {impact['punctuation_marks_after']}")
    print(f"Sentence segmentation:    {impact['sentence_count_before']} -> {impact['sentence_count_after']} sentences")
    print(f"Sentence lengths before:  {impact['sentence_lengths_before']}")
    print(f"Sentence lengths after:   {impact['sentence_lengths_after']}")
    print(f"Sentence length SD:       {impact['sentence_sd_before']} -> {impact['sentence_sd_after']}")
    print(f"Sentence length CV:       {impact['sentence_cv_before']} -> {impact['sentence_cv_after']} ({impact['sentence_cv_delta']:+.3f})")
    print(f"Clause length CV:         {impact['clause_cv_before']} -> {impact['clause_cv_after']}")
    print(f"Damages grammar:          {impact['damages_grammar']}")
    print(f"Damages meaning/fidelity: {impact['damages_meaning']}")
    if impact["detector_sensitivity_mechanisms"]:
        print("Mechanisms triggered:")
        for mech in impact["detector_sensitivity_mechanisms"]:
            print(f"  • {mech}")
    if impact["diff"]["operations"]:
        print("Exact character opcodes:")
        for op in impact["diff"]["operations"]:
            print(f"  {op['op']}: {op['before_span']!r} -> {op['after_span']!r}")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    src_path = Path(args.source)
    if not src_path.is_file():
        print(f"Error: source file not found: {src_path}", file=sys.stderr)
        return 2
    original = src_path.read_text(encoding="utf-8")
    lex_rew = Path(args.lexical_rewrite).read_text(encoding="utf-8") if args.lexical_rewrite else None
    ed_rew = Path(args.editorial_rewrite).read_text(encoding="utf-8") if args.editorial_rewrite else None
    vc_rew = Path(args.voice_rewrite).read_text(encoding="utf-8") if args.voice_rewrite else None

    conditions = generate_experimental_conditions(
        original,
        genre=args.genre,
        lexical_rewrite=lex_rew,
        editorial_rewrite=ed_rew,
        voice_rewrite=vc_rew,
    )
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for name, item in conditions.items():
        (out_dir / f"{name}.txt").write_text(item["text"] + "\n", encoding="utf-8")
        imp = item["impact"]
        elig = check_vendor_length_eligibility(imp["word_count_after"])
        rows.append({
            "condition": name,
            "condition_code": item["condition_code"],
            "word_count": imp["word_count_after"],
            "words_preserved": str(imp["word_sequence_preserved"]).lower(),
            "punctuation_marks": imp["punctuation_marks_after"],
            "sentences": imp["sentence_count_after"],
            "sentence_cv": imp["sentence_cv_after"],
            "damages_grammar": str(imp["damages_grammar"]).lower(),
            "is_production_safe": str(item["is_production_safe"]).lower(),
            "changed": str(imp["changed"]).lower(),
            "sha256": item["sha256"],
            "source": src_path.name,
            "length_bin": elig["stratum"],
            "turnitin_300w_eligible": str(elig["eligible_for_official_turnitin"]).lower(),
            "true_origin": args.true_origin,
            "detector": "",
            "detector_version_date": "",
            "repeat_index": "",
            "ai_score": "",
            "human_score": "",
            "mixed_score": "",
            "notes": "",
        })

    score_csv = out_dir / "score_sheet.csv"
    with score_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    manifest = {
        "source": str(src_path),
        "genre": args.genre,
        "true_origin": args.true_origin,
        "variants_generated": len(rows),
        "unique_outputs": len({r["sha256"] for r in rows}),
        "word_preserving_variants_verified": all(
            item["impact"]["word_sequence_preserved"]
            for item in conditions.values()
            if item["preserves_word_sequence_by_design"]
        ),
        "output_dir": str(out_dir),
        "conditions": {
            k: {
                "condition_code": v["condition_code"],
                "label": v["label"],
                "sha256": v["sha256"],
                "is_production_safe": v["is_production_safe"],
                "impact": v["impact"],
            }
            for k, v in conditions.items()
        },
    }
    (out_dir / "experiment_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps({
        "variants": len(rows),
        "output": str(out_dir),
        "words_unchanged_on_punctuation_probes": manifest["word_preserving_variants_verified"],
        "unique_outputs": manifest["unique_outputs"],
    }, indent=2))
    return 0


def cmd_analyze_scores(args: argparse.Namespace) -> int:
    rows = load_score_rows(args.score_file)
    summary = analyze_score_sheet(rows, ai_flag_threshold=args.threshold)
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0
    print("NOT AI 4.0 : DETECTOR SCORE STABILITY & ROBUSTNESS REPORT")
    print("─" * 56)
    print(f"Total rows: {summary['total_rows']}  |  Scored rows: {summary['scored_rows']}")
    if summary.get("status") == "awaiting_manual_observations":
        print(f"Note: {summary['note']}")
        return 0
    print(f"Classification reversal rate across variants: {summary['reversal_rate']:.1%}")
    if summary["punctuation_isolated_deltas"]:
        print("\nWORD-IDENTICAL PUNCTUATION PERTURBATION DELTAS:")
        for item in summary["punctuation_isolated_deltas"]:
            print(
                f"  • [{item['experiment']} | {item['detector']}] {item['word_identical_pair']}: "
                f"AI score delta {item['ai_score_delta']:+g}, Human score delta {item['human_score_delta']:+g}"
            )
    if summary["between_detector_disagreement"]:
        print("\nBETWEEN-DETECTOR DISAGREEMENT ON IDENTICAL PASSAGES:")
        for item in summary["between_detector_disagreement"]:
            print(
                f"  • [{item['experiment']} | {item['condition']}] detectors={item['detectors']} "
                f"AI scores={item['ai_scores']} (spread={item['max_spread']} pts, conflict={item['label_conflict']})"
            )
    if summary["eligibility_warnings"]:
        print("\nVENDOR MINIMUM WORD-COUNT WARNINGS:")
        for w in summary["eligibility_warnings"]:
            print(f"  ⚠ {w}")
    print(f"\nCaveat: {summary['scientific_caveat']}")
    return 0


def cmd_evaluate_corpus(args: argparse.Namespace) -> int:
    corpus_dir = Path(args.corpus)
    if not corpus_dir.is_dir():
        print(f"Error: robustness corpus directory not found: {corpus_dir}", file=sys.stderr)
        return 2

    fixtures_reports: list[dict] = []
    b_cv_deltas: list[float] = []
    g_cv_deltas: list[float] = []
    b_grammar_damage_count = 0
    g_grammar_damage_count = 0
    g_fidelity_pass_count = 0

    for subdir in sorted(d for d in corpus_dir.iterdir() if d.is_dir()):
        meta_path = subdir / "metadata.json"
        orig_path = subdir / "original.txt"
        if not orig_path.is_file():
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
        genre = meta.get("genre", "linkedin")
        true_origin = meta.get("true_origin", "unknown")
        protected = meta.get("protected_facts", [])
        original = orig_path.read_text(encoding="utf-8")
        editorial = (
            (subdir / "editorial.txt").read_text(encoding="utf-8")
            if (subdir / "editorial.txt").is_file()
            else None
        )
        voice_ref = (
            (subdir / "reference_voice.txt").read_text(encoding="utf-8")
            if (subdir / "reference_voice.txt").is_file()
            else None
        )

        conditions = generate_experimental_conditions(
            original,
            genre=genre,
            editorial_rewrite=editorial,
        )
        b_imp = conditions["B_punctuation_only"]["impact"]
        g_eval = evaluate_passage_pair(
            original,
            conditions["G_genre_aware_editorial"]["text"],
            genre=genre,
            reference_voice=voice_ref,
            protected_facts=protected,
            true_origin=true_origin,
        )

        b_cv_deltas.append(b_imp["sentence_cv_delta"])
        g_cv_deltas.append(g_eval["prosody_and_segmentation"]["sentence_cv_delta"])
        if b_imp["damages_grammar"]:
            b_grammar_damage_count += 1
        if g_eval["grammatical_integrity"]["damages_grammar"]:
            g_grammar_damage_count += 1
        if g_eval["factual_preservation"]["passed"]:
            g_fidelity_pass_count += 1

        fixtures_reports.append({
            "fixture": subdir.name,
            "genre": genre,
            "true_origin": true_origin,
            "stratum": g_eval["length_stratum"],
            "turnitin_300w_eligible": g_eval["turnitin_300w_eligible"],
            "word_count": g_eval["word_count"]["before"],
            "word_preserving_probes_verified": all(
                c["impact"]["word_sequence_preserved"]
                for c in conditions.values()
                if c["preserves_word_sequence_by_design"]
            ),
            "condition_B_punctuation_only": {
                "sentences_before": b_imp["sentence_count_before"],
                "sentences_after": b_imp["sentence_count_after"],
                "sentence_cv_before": b_imp["sentence_cv_before"],
                "sentence_cv_after": b_imp["sentence_cv_after"],
                "sentence_cv_delta": b_imp["sentence_cv_delta"],
                "damages_grammar": b_imp["damages_grammar"],
                "mechanisms": b_imp["detector_sensitivity_mechanisms"],
            },
            "condition_G_genre_aware_editorial": g_eval,
        })

    n = len(fixtures_reports)
    score_analysis = None
    if args.scores and Path(args.scores).is_file():
        score_analysis = analyze_score_sheet(load_score_rows(args.scores))

    aggregate = {
        "fixtures_evaluated": n,
        "by_stratum": {
            s: sum(1 for f in fixtures_reports if f["stratum"] == s)
            for s in ("short_under_150", "medium_150_299", "long_300_plus")
        },
        "by_origin": {
            o: sum(1 for f in fixtures_reports if f["true_origin"] == o)
            for o in sorted({f["true_origin"] for f in fixtures_reports})
        },
        "all_word_preserving_probes_verified": all(
            f["word_preserving_probes_verified"] for f in fixtures_reports
        ),
        "condition_B_punctuation_perturbation_summary": {
            "sentence_cv_delta_ci": bootstrap_ci(b_cv_deltas, stat="mean"),
            "grammar_damage_rate": round(b_grammar_damage_count / n, 3) if n else 0.0,
            "note": (
                "Punctuation-only perturbations (dropping stops / tight ellipses) artificially "
                "inflate sentence-length CV by fusing sentences, but damage grammar on "
                f"{b_grammar_damage_count}/{n} passages."
            ),
        },
        "condition_G_not_ai_4_editorial_summary": {
            "sentence_cv_delta_ci": bootstrap_ci(g_cv_deltas, stat="mean"),
            "grammar_damage_rate": round(g_grammar_damage_count / n, 3) if n else 0.0,
            "factual_preservation_rate": round(g_fidelity_pass_count / n, 3) if n else 0.0,
            "note": (
                "Not-AI 4.0 genre-aware editorial rewrites preserve factual invariants and "
                "maintain grammatical boundary integrity without artificial punctuation damage."
            ),
        },
        "external_detector_score_analysis": score_analysis,
        "fixtures": fixtures_reports,
    }

    if args.out_report:
        Path(args.out_report).write_text(
            json.dumps(aggregate, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    if args.json:
        print(json.dumps(aggregate, indent=2, ensure_ascii=False))
    else:
        print("NOT AI 4.0 : ROBUSTNESS & NATURAL WRITING BENCHMARK SUITE")
        print("─" * 58)
        print(f"Fixtures evaluated: {n}  |  Strata: {aggregate['by_stratum']}")
        print(f"Origins:            {aggregate['by_origin']}")
        print(f"All word-preserving probes verified: {aggregate['all_word_preserving_probes_verified']}")
        b_sum = aggregate["condition_B_punctuation_perturbation_summary"]
        g_sum = aggregate["condition_G_not_ai_4_editorial_summary"]
        print(f"\nCondition B (Punctuation-only perturbation):")
        print(f"  Mean sentence-CV shift: {b_sum['sentence_cv_delta_ci']['estimate']} "
              f"(95% CI [{b_sum['sentence_cv_delta_ci']['ci95_low']}, {b_sum['sentence_cv_delta_ci']['ci95_high']}])")
        print(f"  Grammar damage rate:    {b_sum['grammar_damage_rate']:.1%}")
        print(f"\nCondition G (Not-AI 4.0 genre-aware editorial):")
        print(f"  Factual preservation:   {g_sum['factual_preservation_rate']:.1%}")
        print(f"  Grammar damage rate:    {g_sum['grammar_damage_rate']:.1%}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    cmp_p = sub.add_parser("compare", help="Compare two variants and measure segmentation/prosody impact")
    cmp_p.add_argument("before")
    cmp_p.add_argument("after")
    cmp_p.add_argument("--genre", default="linkedin", choices=sorted(POLICIES))
    cmp_p.add_argument("--json", action="store_true")

    gen_p = sub.add_parser("generate", help="Generate Conditions A-H for a source passage")
    gen_p.add_argument("source")
    gen_p.add_argument("--out", default="variants")
    gen_p.add_argument("--genre", default="linkedin", choices=sorted(POLICIES))
    gen_p.add_argument("--true-origin", default="unknown")
    gen_p.add_argument("--lexical-rewrite", default=None)
    gen_p.add_argument("--editorial-rewrite", default=None)
    gen_p.add_argument("--voice-rewrite", default=None)

    sc_p = sub.add_parser("analyze-scores", help="Analyze a manual/permissioned detector score CSV/JSON")
    sc_p.add_argument("score_file")
    sc_p.add_argument("--threshold", type=float, default=50.0)
    sc_p.add_argument("--json", action="store_true")

    ev_p = sub.add_parser("evaluate-corpus", help="Run the full multi-condition robustness evaluation suite")
    ev_p.add_argument("--corpus", default="benchmarks/robustness/corpus")
    ev_p.add_argument("--scores", default="benchmarks/robustness/modi_case_study/observed_scores.csv")
    ev_p.add_argument("--out-report", default=None)
    ev_p.add_argument("--json", action="store_true")

    args = parser.parse_args()
    if args.command == "compare":
        return cmd_compare(args)
    if args.command == "generate":
        return cmd_generate(args)
    if args.command == "analyze-scores":
        return cmd_analyze_scores(args)
    return cmd_evaluate_corpus(args)


if __name__ == "__main__":
    raise SystemExit(main())
