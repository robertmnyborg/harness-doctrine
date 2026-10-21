# 5. When a small specialist model wins

All four criteria, or the generalist wins:

1. **Volume above ~100 calls/day.** Below that the eval harness costs more than the savings.
2. **Enumerable input distribution.** You can write down what the inputs look like. If you can't, you can't know when you're off-distribution.
3. **Cheap ground truth.** Right/wrong is checkable automatically, with no human reading the output.
4. **Failure caught downstream** before it ships.

**Criterion 3 is the gate.** Without automatic ground truth you cannot detect drift, so you're running an unmonitored component that degrades in silence. That is worse than an expensive generalist you can sanity-check.

Plausible candidates are narrow and data-shaped: field extraction from documents, ranking comparables, inbound reply-sentiment triage, PII scrub before data leaves the machine, label normalization. All rung 3, all with a checkable answer. The coding loop is not one of them.

## Manufacturing criterion 3: the golden set

Criterion 3 is purchasable. A task with no free ground truth is one labeling pass away from cheap ground truth, and that pass is a fixed one-time cost against an unbounded stream of runs. This is the only move that converts Q3 "expensive" into "cheap", so it is the only move that unblocks an unattended loop.

Five requirements. Miss any one and the set measures the labeler instead of the component.

| Requirement | Why | Failure if skipped |
|---|---|---|
| **Representative cuts, named up front** | The set has to span the axes the component varies over (geo, source, size, quality tier, language) | A set that scores 99% and a production run that scores 70%, with no way to see which cut broke |
| **Objective labeling guideline** | Two labelers reading the same guideline must produce the same label | Labeler disagreement enters the set as noise and caps the measurable ceiling below the real one |
| **Enrich for hard cases, reweight to the true distribution** | A balanced set proves nothing when the real class balance is 99.9% easy | The enriched score picks the winner and the population score reverses it (address matching, lesson 2 below) |
| **Frozen** | The set is the constant the component is tuned against | Tuning the set alongside the component measures nothing |
| **Held-out refresh from production** | Real inputs drift away from the set that was built once | The set stays green while the component degrades in silence |

**The gate the set buys:** no new version of the component ships until it re-passes the frozen set on the guardrail metric. That gate is rung 1, so it holds regardless of what tier produced the change. Without the gate the set is documentation.

**When not to buy it.** Labeling cost scales with the number of cuts, so a set pays off when the component runs often enough to amortize it, roughly the same volume bar as criterion 1. For a judgment that runs a few times a month and gets read by a human every time, the human read is cheaper than the set.

**Look for free labels first.** The address-matching set below cost nothing to label: a table that an upstream entity-resolution process had already merged across several data sources put two source addresses on the same row, and each row was a verified positive pair.

## Measured: address matching failed the test

The first candidate put through this filter came out at **rung 1, not rung 3**. Method and code in [`examples/address-matching/`](../examples/address-matching/).

| Arm | Recall | Precision | Wall time |
|---|---|---|---|
| Normalizer, 3 iterations | **99.89%** | **99.92%** | ~2s for the full set |
| `qwen3:30b-a3b` local, projected to population | 94.95% | not measured | 2.6h |

The model recovered about half of the pairs the normalizer missed and lost roughly 100 times as many it already had. Net: **about 5% fewer matches**.

Three transferable lessons:

1. **Measure the headroom before measuring the model.** The first normalizer scored 96.19%, and the 3.81% residual *looked* like hard cases needing judgment. It was one missing rule (a directional present on one side only). Two more iterations took it to 99.89%. Every apparent hard case dissolved into deterministic code.
2. **A balanced eval set would have proved nothing.** Both arms score ~99% on a 50/50 sample, because the real class distribution is 99.9% easy. Enrich for hard cases to *find* the failure modes, then project back onto the true distribution to *decide*. The enriched set scored the model at 76.2% vs the normalizer's 72.2%, a win. The population weighting reversed it.
3. **Check what the model breaks, not just what it fixes.** The control bucket is where the decision was made. The model's failure mode was identical to the normalizer bug already fixed: calling `2210 Marrowbend Dr` and `2210 Marrowbend Drive NE` different properties.

## Delivery mode beats tier

Two levers sit orthogonal to model choice and are usually larger:

- **Batch APIs: typically 50% off any model, under 24h turnaround.** A batched frontier model can undercut the mid tier at list price. So for anything not interactive, **downgrading the model is the wrong move.** Downgrade the delivery mode and keep the intelligence.
- **Prompt caching: cache reads cost roughly a tenth of fresh input.** On a repeated large prefix this dominates tier choice outright.

Check both before considering a cheaper model. Prices move; re-check your provider's current list before quoting numbers.

## Local model sizing

On a 36GB unified-memory laptop, roughly 24GB is usable for weights before paging.

| Shape | Size at Q4 | Verdict |
|---|---|---|
| 7B-14B dense | 4-9GB | Fast, comfortable |
| 30B MoE (3B active) | ~18GB | The workhorse. Fits, and the small active-param count keeps it fast |
| 32B dense | ~20GB | Fits, noticeably slower, because every param activates |
| 70B dense | ~40GB | Does not fit |

Local quality on a specific task is unmeasured until that task has an eval. Until it does, the task stays hosted.
