The correct output for this input is the input, unchanged. Reproduced here so that the before and after measurements in `rationale.md` can be run against two real files.

```
I spent three days last month hunting a bug that only showed up under load. The issue was in how we handled connection timeouts — specifically, a race condition between the health check and the reconnection logic. I found it by adding more aggressive logging and watching the logs during a controlled load test. Not fun, but at least I know what to look for next time.
```

The fenced block above is byte-identical to `input.md`. Intervention rate 0%.
