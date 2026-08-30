Caching keeps a copy of data somewhere faster to reach than the original. That is the whole idea. Everything else is detail about where the copy lives and when you throw it away.

The payoff is real but bounded. A read that hits the cache skips the database entirely, so it returns faster and the database does less work. Both effects compound under load, which is when you need them.

The hard part is deciding when a cached copy has gone stale. Time-based expiry is simple: hold the copy for a fixed window, then fetch again. Event-driven invalidation is more precise and more work, because something has to notice the underlying data changed and say so. Which one fits depends on how bad it is to serve a stale value, and that varies enormously between systems. A stale follower count is a cosmetic problem. A stale account balance is not.

So the real decision is not about caching. It is about how much staleness the thing you are building can absorb.
