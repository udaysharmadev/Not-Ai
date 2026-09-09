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


POLICIES = {
    "linkedin": GenrePolicy("linkedin", True, True, True, True),
    "personal": GenrePolicy("personal", True, True, True, True),
    "email": GenrePolicy("email", True, True, False, True),
    "social": GenrePolicy("social", True, False, True, True),
    "fiction": GenrePolicy("fiction", True, False, True, True),
    "readme": GenrePolicy("readme", False, False, False, True),
    "technical": GenrePolicy("technical", False, False, False, False),
    "student": GenrePolicy("student", False, False, False, True),
    "academic": GenrePolicy("academic", False, False, False, False),
}


def get_policy(genre: str) -> GenrePolicy:
    """Return a validated profile; callers must not silently guess a genre."""
    try:
        return POLICIES[genre.lower()]
    except KeyError as error:
        options = ", ".join(sorted(POLICIES))
        raise ValueError(f"Unknown genre '{genre}'. Choose one of: {options}") from error
