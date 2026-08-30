## Output: Technical Passage (After Not Ai)

---

Caching is how you avoid doing the same work twice. When a user requests data, the system checks the cache first. If the data is there, it skips the database entirely. If not, it fetches, stores it in the cache, and serves it.

The benefits are straightforward: lower latency, fewer database hits, and better scaling when traffic spikes. These aren't independent wins — they compound. A well-designed cache reduces load on the database, which lets the database handle harder queries better, which makes the whole system more responsive under load.

The tricky part is keeping cached data fresh. Two common approaches: time-based expiration (data expires after N seconds, regardless of whether it changed) and event-driven invalidation (the cache entry is cleared when the underlying data changes). Time-based is simpler but wastes cache space on stale data. Event-driven is more precise but requires your application to know when to invalidate.

Which strategy fits depends on how often your data changes and how much staleness you can tolerate. A product catalog that updates once a day and a user session that updates on every request need different caching approaches.
