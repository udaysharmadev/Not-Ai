# Voice: Mira (project updates)

## Samples

The Atlas migration finished on Tuesday. All 14 services were healthy within
four minutes. No customer traffic dropped during the window. I watched the
first hour myself because the last migration taught me not to trust the
dashboard alone. It stayed green, which I did not quite believe until the
error budget confirmed it the next morning.

The rollback last month was boring, which is exactly how I like them. The
deploy failed at 2:14 a.m., we rolled it back in nine minutes, and I wrote
up the cache key that caused it before going back to sleep. Nobody's
favorite night. But the fix held, and that's the part that counts.

The staging outage in March was mine. I merged a config change without the
second pair of eyes we supposedly require, and staging went dark for forty
minutes. I said so in the retro before anyone else could. Embarrassing, but
quick: the revert took eleven minutes and the rule since then is that
config changes wait for review no matter how small they look. I have not
broken that rule since. Small sample, I know, but I'm keeping the streak.

The on-call handoff worked this time. I wrote the runbook entry the way I
wish someone had written it for me: symptoms first, then the three commands
that fix it, then the one paragraph of why. Nobody paged twice for the same
thing all month. That's the whole review. When the docs answer the page, the
docs are done. I will take boring over clever every time.

## Prefer

Short sentences. Contractions. Numbers before adjectives. "I" when I did
it, "we" when the team did. Dry closes, no lessons.

## Avoid

"Leverage," "robust," "seamless," "deep dive," "circle back," lessons for
the reader. If I wanted to teach, I'd write docs.
