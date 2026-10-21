# harness-doctrine

Where does a model belong in an agent harness? Usually lower than you put it.

The first time I tested that claim on a real step, a 70-line deterministic normalizer matched street addresses at **99.89% recall and 99.92% precision in about 2 seconds**. A local 30B model on the same job reached **94.95% recall in 2.6 hours** and lost about **5% of the matches** the normalizer found. The step looked like it needed judgment. It needed three more rules.

This repo is the decision procedure that came out of that, plus the code and method for the address test. It covers Claude Code harnesses (rules, skills, hooks, subagents, MCP servers, crons), and the reasoning applies to any agent stack.

## Four questions, before any approach

Answer them **per step**, not per task. One job often splits: the dedupe is a guarantee, the send is irreversible, the scoring is a judgment. Domain ("frontend", "data", "strategy") is not one of the questions, because it predicts nothing about where the model goes.

| # | Question | If the answer is... | ...then |
|---|---|---|---|
| 1 | **Guarantee or estimate?** Does something downstream trust this output? | Guarantee | Deterministic code. No model at any tier. "Check", "verify", "make sure" in the ask are the tell. |
| 2 | **Reversible?** Undoable in a minute, alone, before anyone sees it? | No | Top model plus an explicit human confirm, whatever the cost. Sends, deploys, merges, publishes. Mechanical-looking is not the same as reversible. |
| 3 | **Ground truth cheap?** Can a script tell right from wrong with no human reading? | Yes | Automation, specialist models, and unattended loops become safe, because drift announces itself. If no: a generalist, a human read, no loop. |
| 4 | **Interactive?** Is anyone waiting on it? | No | Batch it or cron it and keep the model tier. Delivery mode beats tier. |

The questions are facts about the outcome, checkable before you start, so they cannot misroute. A task classifier can.

## The ladder

Start at rung 1 and climb only when quality breaks.

| Rung | What | Buys |
|---|---|---|
| 0 | Constant, config | Zero variance |
| 1 | Deterministic code: hook, script, regex, hash | A guarantee |
| 2 | Retrieval, no generation | Grounding |
| 3 | Small model, fixed output schema | Cheap volume |
| 4 | Frontier, one shot | Judgment |
| 5 | Frontier + tools + agency | Open-ended work |
| 6 | Fan-out | Coverage |

Rungs 0 to 2 contain no intelligence, and most durable harness components live there. Two overrides beat any cost argument: a guarantee goes to rung 1, and an irreversible outward-facing step goes to the top rung.

## Why harnesses drift upward

Excess intelligence degrades output on its own, separate from what it costs. Extra context is a distractor. A frontier model on a checkable question buys variance where you wanted a guarantee. More agency on a bounded task invents requirements.

Underdosing fails loudly, so you fix it. Overdosing fails quietly: fluent, wrong output with no signal that the harness caused it. The feedback runs one way, so every harness accretes. The fix is a schedule: audit invocation counts from transcripts, and delete anything nobody called. On this harness the first audit found 25 custom subagent definitions with zero launches in 90 days.

## Predicates route, classifiers guess

A router that can reliably say "this is a Type-7 task" has already done the hard part. A predicate (file path matches a regex, command starts with `git commit`, prompt contains a URL) covers less, abstains when it doesn't match, and has zero router error on what it covers. A skill description that said "use whenever you edit server code" fired zero times in 90 days; a hook keyed on the edited file path fires every time. Same content, later binding, real mechanism.

## When a small model does win

All four, or the generalist wins: volume above ~100 calls/day, an input distribution you can write down, ground truth a script can check, and failures caught downstream. The third is the gate. Without automatic ground truth you cannot see drift, so the specialist degrades in silence.

Ground truth is purchasable. A frozen, labeled golden set turns "expensive" into "cheap" for one fixed cost. Look for free labels first: the address test needed none, because an upstream entity-resolution table already put several data sources' addresses for the same property on one row.

## The address test, in three lessons

1. **Measure the headroom before the model.** The first normalizer scored 96.19%, and the residual looked like hard cases. It was one missing rule: a directional (`NE`) present on one side only. Two iterations later every apparent hard case was deterministic.
2. **A balanced eval set proves nothing** when the real distribution is 99.9% easy. On the enriched hard-case set the model won, 76.2% to 72.2%. Reweighted to the real distribution, it lost about 5% of all matches.
3. **Check what the model breaks, not only what it fixes.** It recovered about half of the normalizer's few misses and broke roughly 100 times as many easy pairs, with the exact bug the normalizer had already fixed.

Code, method, and a synthetic fixture: [`examples/address-matching/`](examples/address-matching/).

## The longer doctrine

| Doc | Covers |
|---|---|
| [01 Dose, not cost](docs/01-dose.md) | Why more intelligence makes output worse |
| [02 The ladder](docs/02-ladder.md) | Seven rungs, the tell you're too high, two overrides |
| [03 Four questions, four dials](docs/03-four-questions-and-dials.md) | Worked tuples; then level, place, time, amount |
| [04 Predicates over classifiers](docs/04-predicates-over-classifiers.md) | Why deterministic routing fails safe |
| [05 Small specialists](docs/05-small-specialist.md) | Four criteria, building a golden set, delivery mode, local model sizing |
| [06 Checklist](docs/06-checklist.md) | Eight questions before adding any component |
| [07 Anti-patterns](docs/07-anti-patterns.md) | Eleven patterns and how to spot each |
| [08 Audit recipe](docs/08-audit.md) | Re-runnable shell one-liners over Claude Code transcripts |
| [09 Routing table](docs/09-routing-table.md) | The four questions compressed into an always-on table |

## Use it

Nothing to install for the essay. Two ways to put it to work in Claude Code:

1. Copy the four-question table into your `~/.claude/CLAUDE.md` so it loads every session (about 330 tokens).
2. Save `docs/` as `~/.claude/harness-doctrine.md` (concatenated) and point to it from `CLAUDE.md` with "load before adding, cutting, or debugging a rule, skill, hook, subagent, MCP server, or cron."

The example needs Python 3.9+ and `rapidfuzz`:

```bash
cd examples/address-matching
pip install rapidfuzz
python -m unittest -v test_matcher
```

## The one-line version

Four questions about the outcome set the requirement; predicates route, the ladder assigns the level, binding is late by default, and the amount is whatever survives deletion.

MIT License.
