"""Genre policy for deterministic checks.

The gate deliberately has a small hard-fail surface. Style varies by genre;
the rest of its findings are review prompts, not instructions to distort prose.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class GenrePolicy:
    name: str
    conversational: bool
    require_contractions: bool
    allow_fragments: bool
    check_nominalizations: bool
    # Minimum tokens before the missing-contraction prompt can fire.
    # Short conversational posts rarely have room for one naturally.
    contraction_floor: int = 80
    # Expected Flesch-Kincaid band for the genre, used only as a review
    # prompt by tooling that computes readability. Academic and technical
    # writing are legitimately dense; LinkedIn and social are not.
    grade_low: float = 0.0
    grade_high: float = 99.0


POLICIES = {
    "linkedin": GenrePolicy("linkedin", True, True, True, True,
                            contraction_floor=30, grade_low=5.0, grade_high=12.0),
    "personal": GenrePolicy("personal", True, True, True, True,
                            contraction_floor=40, grade_low=5.0, grade_high=12.0),
    "email": GenrePolicy("email", True, True, False, True,
                         contraction_floor=40, grade_low=5.0, grade_high=12.0),
    "social": GenrePolicy("social", True, False, True, True,
                          contraction_floor=30, grade_low=3.0, grade_high=10.0),
    "fiction": GenrePolicy("fiction", True, False, True, True,
                           contraction_floor=60, grade_low=3.0, grade_high=10.0),
    "readme": GenrePolicy("readme", False, False, False, True,
                          grade_low=6.0, grade_high=14.0),
    "technical": GenrePolicy("technical", False, False, False, False,
                             grade_low=8.0, grade_high=16.0),
    "student": GenrePolicy("student", False, False, False, True,
                           grade_low=8.0, grade_high=16.0),
    "academic": GenrePolicy("academic", False, False, False, False,
                            grade_low=12.0, grade_high=22.0),
}


def get_policy(genre: str) -> GenrePolicy:
    """Return a validated profile; callers must not silently guess a genre."""
    try:
        return POLICIES[genre.lower()]
    except KeyError as error:
        options = ", ".join(sorted(POLICIES))
        raise ValueError(f"Unknown genre '{genre}'. Choose one of: {options}") from error
