"""Intervention planner (Not-AI 3.0).

Determines editorial workload from actual need, never rewards changing text.
Levels: NONE / LIGHT / MODERATE / HEAVY / RESTRUCTURE / BLOCKED_BY_MISSING_INFORMATION.
Regression fixtures with expected NONE must return the source unchanged.
"""

from __future__ import annotations


LEVELS = ("NONE", "LIGHT", "MODERATE", "HEAVY", "RESTRUCTURE", "BLOCKED_BY_MISSING_INFORMATION")


def plan(*, errors: int = 0, reviews: int = 0, missing_info_blocked: bool = False,
         global_restructure: bool = False) -> dict:
    if missing_info_blocked or errors:
        level = "BLOCKED_BY_MISSING_INFORMATION" if missing_info_blocked else "HEAVY"
        if errors and not missing_info_blocked:
            # Objective errors must be fixed first, but that is not automatically
            # a restructure; keep HEAVY unless global signals say otherwise.
            level = "HEAVY" if not global_restructure else "RESTRUCTURE"
        return {"level": level, "reason": "objective errors or missing information block normal editing"}
    if global_restructure:
        return {"level": "RESTRUCTURE", "reason": "global map shows duplicated/contradicted sections or lost definitions"}
    if reviews == 0:
        return {"level": "NONE", "reason": "no findings; already-good writing stays unchanged"}
    if reviews <= 2:
        return {"level": "LIGHT", "reason": "one or two targeted prompts"}
    if reviews <= 6:
        return {"level": "MODERATE", "reason": "a few targeted edits"}
    return {"level": "HEAVY", "reason": "several passages deserve re-reading"}


def diagnose_to_reviews(diagnose_entry: dict) -> int:
    return sum(1 for item in diagnose_entry.get("revise", [])
               if item.get("severity") != "error")
