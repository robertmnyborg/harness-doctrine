# 2. The ladder: what level

Descend until quality breaks, then step back one rung. The default entry point is rung 1, not rung 5.

| Rung | What it is | Buys | Costs | Tell you're too high |
|---|---|---|---|---|
| 0 | Constant / config | Zero variance, zero latency | No adaptivity | Asking a model something with one right answer |
| 1 | Deterministic code (hook, script, regex, hash) | A guarantee | Brittle to shape changes | Asking a model to check something checkable |
| 2 | Retrieval, no generation | Grounding | Stale index | The model recites a fact already on disk |
| 3 | Small model, fixed schema out | Speed, cheap volume | Fails off-distribution | Output is a label, score, rank, or a few fields |
| 4 | Frontier, one shot, no tools | Judgment | Latency, variance | It answers right on the first try every time |
| 5 | Frontier + tools + agency | Open-ended, multi-step | Scope creep, cost | It explores a space you could have enumerated |
| 6 | Frontier + fan-out | Coverage | Large cost | You needed one answer, not many |

Rungs 0-2 contain no intelligence. Most durable harness components live there.

**Two overrides beat any cost reasoning:**

- Needs a **guarantee** → rung 1. No exceptions. Gates, checks, invariants, anything another component trusts.
- **Irreversible or outward-facing** → top rung regardless of apparent simplicity. Deploys, sends, deletes, publishes. Cheap-looking tasks with expensive failure modes are where downshifting kills you.
