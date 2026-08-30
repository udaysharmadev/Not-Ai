#!/usr/bin/env python3
"""
not-ai: verify_checks.py
Negative controls for the three checks that no file in this repository exercises.

Why this file exists. The convention here is that no checker is trusted until it
has been deliberately broken and caught the break. For most measures the repo's
own text supplies the control: `examples/already-natural/input.md` is
human-written and every detector stays quiet on it. Three checks have no such
control available, so the specimens have to be written by hand:

  1. `stance_balance` in `_shared.py`. Not one file in this repository earns a
     real balance verdict. Twelve carry no hedge or booster at all and five carry
     one or two, so "over-hedged", "over-assertive" and "calibrated" are
     unreachable from repo text. Without synthetic input those three branches
     would never run.
  2. `repeated_syntactic_frames` in `repetition.py`. Its warning needs the same
     frame in two adjacent sentences.
  3. `coordinated_series` in `repetition.py`. Its warning needs three items that
     all open with the same word.

Each control below is one of three kinds, and the kind is part of the point:

  MUST FIRE      the check is supposed to catch this
  MUST STAY QUIET  the check is supposed to let this through
  KNOWN LIMIT    the check gets this wrong, on the record, deliberately

The KNOWN LIMIT cases are pinned here so a future edit cannot quietly change the
documented behaviour without a test turning red. A checker with no recorded
limits is a checker nobody has probed.

Usage:
    python3 scripts/verify_checks.py
    python3 scripts/verify_checks.py --verbose
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import measure  # noqa: E402
import repetition  # noqa: E402
from _shared import get_sentences, stance_balance, tokenize_words  # noqa: E402

results = []


def check(kind: str, name: str, passed: bool, detail: str = "") -> None:
    results.append((kind, name, passed, detail))


# ─── 1. Stance balance ───────────────────────────────────────────────────────
#
# Hedge and booster patterns are fixed lists in metrics.py and measure.py, so
# each specimen names its markers in a comment. Counts were taken from a run,
# not from reading the regexes.

STANCE_CASES = [
    (
        "MUST FIRE",
        "absent: no hedge, no booster",
        # The regression that prompted the fix. The old logic compared counts
        # directly, 0 > 0 was false in both branches, and this fell through to
        # "calibrated": a clean bill of health on a text with no stance at all.
        "The cache stores a copy of the response. The copy goes stale when the "
        "underlying record changes. Nothing in the protocol says when that is.",
        "absent",
    ),
    (
        "MUST FIRE",
        "too sparse: under the 3-marker floor",
        # 2 hedges: "might", "seems". Ratio would read over-hedged; 2 is too
        # little to read a ratio from.
        "The build might fail on the older runner. It seems related to the "
        "cache key, though nobody has confirmed that yet, so the fix is on hold.",
        "too sparse to judge",
    ),
    (
        "MUST FIRE",
        "too sparse: over the marker floor, under the rate floor",
        # 3 hedges in roughly 1,800 words: passes the count floor, fails the
        # 2.0 per 1,000 floor at 1.7. This is the branch that catches a long
        # document with a few stray hedges in it, which is what README.md
        # (5 hedges in 6,185 words) and methodology.md actually are.
        ("The record is written once and read many times. " * 200)
        + "It might be stale. It could be current. It may not matter.",
        "too sparse to judge",
    ),
    (
        "MUST FIRE",
        "over-hedged: hedges past 3x boosters",
        # 5 hedges: might, could, perhaps, seems, suggests. 0 boosters.
        "The result might hold. It could be an artifact of the sample. Perhaps "
        "the effect is real, though the confidence interval seems wide, and the "
        "residual plot suggests the model is missing a term.",
        "over-hedged",
    ),
    (
        "MUST FIRE",
        "over-assertive: boosters past 2x hedges",
        # 4 boosters: clearly, obviously, certainly, of course. 0 hedges.
        "The result clearly holds. The mechanism is obviously the cache. That is "
        "certainly the cause, and of course the fix follows from it directly.",
        "over-assertive",
    ),
    (
        "MUST STAY QUIET",
        "calibrated: neither ratio triggered",
        # 3 hedges (might, seems, suggests) and 2 boosters (clearly, certainly).
        # 3 > 6 is false, 2 > 6 is false.
        "The effect clearly shows in the first cohort. It might not survive the "
        "second, which seems underpowered. The pooled estimate suggests a real "
        "difference, and the direction is certainly consistent across sites.",
        "calibrated",
    ),
]


def check_stance(verbose: bool) -> None:
    for kind, name, text, expected in STANCE_CASES:
        markers = measure.tone_markers(text)
        got = markers["stance_balance"]
        words = len(text.split())
        detail = (f"{markers['hedge_count']}h {markers['booster_count']}b in "
                  f"{words}w -> {got!r}, expected {expected!r}")
        check(kind, f"stance, {name}", got == expected, detail)

        # The two implementations must agree, since measure.py is embedded
        # verbatim in dist/SKILL.md and cannot import _shared.py.
        canonical = stance_balance(markers["hedge_count"], markers["booster_count"], words)
        check("MUST FIRE", f"stance parity, {name}", canonical == got,
              f"_shared={canonical!r} measure={got!r}")

        if verbose:
            print(f"    {detail}")

    # The specific regression, asserted as itself rather than only as a verdict.
    zero = measure.tone_markers(STANCE_CASES[0][2])
    check("MUST FIRE", "stance, zero markers never reads calibrated",
          zero["stance_balance"] != "calibrated",
          f"got {zero['stance_balance']!r}")


# ─── 2. Repeated syntactic frames ────────────────────────────────────────────

FRAME_CASES = [
    (
        "MUST FIRE",
        "range sweep in two consecutive sentences",
        # Reduced from the paragraph that started this: two sentences, no shared
        # 3-gram, no shared opening, same move twice.
        "Its history stretches from the Indus Valley cities through Mughal "
        "architecture to independence. Geography here swings from Himalayan "
        "peaks to tropical coastlines.",
        {"consecutive": ["range sweep"]},
    ),
    (
        "MUST STAY QUIET",
        "same frame two sentences apart",
        # Proves the window really is adjacency. Sentences 1 and 3 sweep; the
        # count is 2 and the warning list is empty.
        "The archive runs from 1890 to 1954. Nobody has catalogued it. The "
        "gaps run from the war years through the early fifties.",
        {"consecutive": [], "counts": {"range sweep": 2}},
    ),
    (
        "MUST STAY QUIET",
        "two different frames back to back",
        # Adjacent sentences, one frame each, no overlap.
        "The archive runs from 1890 to 1954. It holds more letters than the "
        "county records office.",
        {"consecutive": []},
    ),
    (
        "MUST STAY QUIET",
        "plain prose, no named frame",
        "The clerk locked the door at six. Rain had started. He walked home.",
        {"consecutive": [], "counts": {}},
    ),
    (
        "KNOWN LIMIT",
        "gerund subject counts as 'comma plus -ing word'",
        # "In conclusion, caching remains" appends nothing to anything. The
        # frame is named after the string it matches for exactly this reason;
        # calling it "participial tail" would have been a claim the regex
        # cannot support. Both sentences here are gerund subjects, so the
        # warning fires on a repeat that is not a participial repeat.
        "In conclusion, caching remains an indispensable tool. In practice, "
        "batching reduces the round trips.",
        {"consecutive": ["comma plus -ing word"]},
    ),
    (
        "KNOWN LIMIT",
        "adjacency measured across a markdown heading",
        # Reduced from references/wikipedia-signs.md, which reports this warning
        # today. A heading carries no terminal punctuation, so the splitter runs
        # the end of one section, the heading, and the body of the next into a
        # single sentence. The two matches here sit in different sections with a
        # level-3 heading between them, and the first is the preposition
        # "including" rather than a participle, so both halves of the warning
        # are wrong: the frame and the adjacency.
        "A model asked for a structured piece fills every slot in the "
        "structure, including slots the material does not support.\n\n"
        "In non-fiction a `Future Outlook` heading is a strong signal on its "
        "own.\n\n### Awards and legacy sections\n\nSections with these "
        "headings that contain no specific award or citation, existing because "
        "the shape of the article seemed to call for one.",
        {"consecutive": ["comma plus -ing word"]},
    ),
]


def check_frames(verbose: bool) -> None:
    for kind, name, text, expect in FRAME_CASES:
        sentences = get_sentences(text)
        for label, fn in (("repetition.py", repetition.repeated_syntactic_frames),
                          ("measure.py", measure.syntactic_frames)):
            got = fn(sentences)
            frames = sorted(r["frame"] for r in got["consecutive_repeats"])
            ok = frames == sorted(expect["consecutive"])
            if "counts" in expect:
                ok = ok and got["frame_counts"] == expect["counts"]
            detail = (f"consecutive={frames}, counts={got['frame_counts']}, "
                      f"expected consecutive={sorted(expect['consecutive'])}")
            check(kind, f"frames [{label}], {name}", ok, detail)
            if verbose:
                print(f"    {label}: {detail}")


# ─── 3. Coordinated series ───────────────────────────────────────────────────

SERIES_CASES = [
    (
        "MUST FIRE",
        "Oxford series of three, not parallel",
        # The closing sentence of the paragraph that started this. Three items,
        # lead words "powered", "a", "and cities", so no anaphora and no
        # warning: it is reported for a reading, which is all a regex can ask.
        "India has become one of the fastest-growing major economies, powered "
        "by a young workforce, a booming tech sector, and cities like Bengaluru.",
        {"series": 1, "parallel": 0},
    ),
    (
        "MUST FIRE",
        "parallel triple, all three items open with 'a'",
        "The plan needed a bigger room, a longer window, and a second reviewer.",
        {"series": 1, "parallel": 1, "lead": "a"},
    ),
    (
        "MUST FIRE",
        "parallel triple on a repeated subordinator",
        "We asked whether the voice survived, whether the rules were right, and "
        "whether the change was worth making.",
        {"series": 1, "parallel": 1, "lead": "whether"},
    ),
    (
        "MUST STAY QUIET",
        "two coordinated items, not three",
        "The plan needed a bigger room and a second reviewer.",
        {"series": 0, "parallel": 0},
    ),
    (
        "MUST STAY QUIET",
        "no coordinator at the end",
        "The room, which had no window, was the only one free that afternoon.",
        {"series": 0, "parallel": 0},
    ),
    (
        "KNOWN LIMIT",
        "series without the Oxford comma is missed entirely",
        # Detection is comma-delimited, so the final item has to be its own
        # segment. This is the largest documented gap in the check.
        "The plan needed a bigger room, a longer window and a second reviewer.",
        {"series": 0, "parallel": 0},
    ),
    (
        "KNOWN LIMIT",
        "adverbial plus two clauses reads as a series",
        # Not a list at all: an opening adverbial and a compound sentence. It
        # produces three comma segments ending in "and", so it is reported.
        # It carries no warning, and the printed span makes the error visible,
        # which is the most the design can offer.
        "Economically, India grew, and Bollywood thrived.",
        {"series": 1, "parallel": 0},
    ),
    (
        "KNOWN LIMIT",
        "series spanning a table cell and the paragraph after it",
        # Reduced from examples/linkedin-post/README.md, which reports this
        # warning today. A pipe is not a sentence terminator, so a table cell
        # ending in a comma series is joined to the next paragraph and the
        # third item is picked up from prose that has nothing to do with the
        # list. The second item printed in the report still carries the pipe,
        # which is the tell that a reader needs to dismiss it.
        "| [rationale.md](rationale.md) | Per-sentence accounting, what the "
        "platform gets to keep, and the burstiness finding |\n\n**What this "
        "example is for.** It is the counterpart to the human paragraph, and "
        "the pair is the most useful thing here.",
        {"series": 1, "parallel": 1, "lead": "the"},
    ),
]


def check_series(verbose: bool) -> None:
    for kind, name, text, expect in SERIES_CASES:
        sentences = get_sentences(text)
        word_count = len(tokenize_words(text))
        for label, fn in (("repetition.py", repetition.coordinated_series),
                          ("measure.py", measure.coordinated_series)):
            got = fn(sentences, word_count)
            ok = (got["series_count"] == expect["series"]
                  and len(got["parallel_triples"]) == expect["parallel"])
            if "lead" in expect and got["parallel_triples"]:
                ok = ok and got["parallel_triples"][0]["lead_word"] == expect["lead"]
            detail = (f"series={got['series_count']} "
                      f"parallel={len(got['parallel_triples'])}, expected "
                      f"series={expect['series']} parallel={expect['parallel']}")
            check(kind, f"series [{label}], {name}", ok, detail)
            if verbose:
                print(f"    {label}: {detail}")


# ─── 4. The human-written control stays clean ────────────────────────────────


def check_human_control() -> None:
    """
    The one control that is not synthetic. `examples/already-natural/input.md` is
    human-written, and both new detectors should be silent on it. A detector that
    fires on this file is measuring something other than what it claims.
    """
    path = Path(__file__).resolve().parent.parent / "examples/already-natural/input.md"
    if not path.is_file():
        check("MUST STAY QUIET", "human control file present", False, f"missing: {path}")
        return
    text = path.read_text(encoding="utf-8")
    sentences = get_sentences(text)
    frames = repetition.repeated_syntactic_frames(sentences)
    series = repetition.coordinated_series(sentences, len(tokenize_words(text)))
    check("MUST STAY QUIET", "human control, no frame warning",
          not frames["consecutive_repeats"], str(frames["frame_counts"]))
    check("MUST STAY QUIET", "human control, no series warning",
          not series["parallel_triples"], f"series={series['series_count']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Not Ai: negative controls")
    parser.add_argument("--verbose", action="store_true",
                        help="print the measured figures for each control")
    args = parser.parse_args()

    print("Negative controls for stance balance, sentence frames and coordinated series\n")
    check_stance(args.verbose)
    check_frames(args.verbose)
    check_series(args.verbose)
    check_human_control()

    failed = [r for r in results if not r[2]]
    for kind, name, passed, detail in results:
        if not passed:
            print(f"  FAIL  [{kind}] {name}")
            print(f"        {detail}")

    by_kind = {}
    for kind, _, passed, _ in results:
        hit = by_kind.setdefault(kind, [0, 0])
        hit[1] += 1
        if passed:
            hit[0] += 1
    for kind in ("MUST FIRE", "MUST STAY QUIET", "KNOWN LIMIT"):
        if kind in by_kind:
            good, total = by_kind[kind]
            print(f"  {kind:<16} {good} of {total}")

    print(f"\n{len(results) - len(failed)} of {len(results)} controls passed")
    print("CONTROLS OK" if not failed else "CONTROLS FAILED")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
