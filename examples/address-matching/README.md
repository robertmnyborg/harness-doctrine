# Worked example: a normalizer beat a local model at address matching

Question: does a local model earn a place in an address-matching step, or is the step rung 1?

Answer: rung 1. A deterministic normalizer reached **99.89% recall / 99.92% precision in ~2 seconds** over the full set of known-same pairs. A local `qwen3:30b-a3b` (Q4, via Ollama) projected to **94.95% recall in 2.6 hours**, a net loss of about 5% of matches.

The eval ran on proprietary data, so this folder ships the method, the matcher, and the aggregate numbers. No data.

## Method

1. **Free ground truth.** An upstream entity-resolution process had already merged properties from several data sources into one row per property. Two source addresses on the same row form a verified positive pair, with no labeling. Rows where the two sources' coordinates disagreed by more than 200m were dropped as likely entity-resolution errors.
2. **Hard negatives.** Distinct properties 150-600m apart: close enough to share a street and a number range, far enough to be different buildings. A lat/lng grid (`eval.py`) builds them in linear time; the equivalent spatial self-join in SQL timed out.
3. **Iterate the normalizer before touching a model.** Each iteration reads the residual misses and asks whether one rule explains them.
4. **Enrich, then reweight.** The model arm ran on a small set: every normalizer miss, a sample of normalizer false positives, plus 100 easy positives and 100 easy negatives as controls. Results were then projected back onto the real class distribution.

## Results

| Arm | Recall | Precision | Wall time |
|---|---|---|---|
| v1: suffix expansion + fuzzy core | 96.19% | not measured | ~2s |
| v2: + directional on one side only is OK | 99.47% | 99.90% | ~2s |
| **v3: + ordinals, numeric-token guard** | **99.89%** | **99.92%** | **~2s** |
| `qwen3:30b-a3b` Q4 local, projected | 94.95% | not measured | 2.6h |

On the enriched set the model looked better (76.2% vs 72.2%), because the set was built from the normalizer's failures. On the controls it lost: it recovered about half of the pairs v3 misses and broke roughly 100 times as many that v3 gets right. Its failure mode was the v1 bug: it called `2210 Marrowbend Dr` and `2210 Marrowbend Drive NE` different.

## What the residual looked like

- **The misses** were all the same shape: one source carries the wrong quadrant (`77 Fennick St NW` vs `77 Fennick Street NE`), with the two coordinates 9-116m apart. A rule "coordinates within 150m ⇒ match" catches all of them, still at rung 1. Not applied in the numbers above.
- **Most of the false positives** were one property split across two rows with different geocodes (`Ct` vs `Court`, ~200m apart). The matcher was right and the reference data was wrong, so true precision sits above 99.92%.

Both residuals are data-quality findings, not judgment calls. Neither needed a model.

## Files

| File | What it does |
|---|---|
| `matcher.py` | `match(a1, a2) -> (bool, reason)`, the v3 normalizer |
| `eval.py` | Recall, precision, and the grid-based hard-negative builder, for your own data |
| `local_model.py` | The model arm: SAME/DIFFERENT per pair via a local Ollama endpoint |
| `fixtures/pairs.json` | 12 synthetic pairs (invented street names), one per rule and failure mode |
| `test_matcher.py` | Tests against the fixture and the hard-negative distance band |

## Run

```bash
pip install rapidfuzz
python -m unittest -v test_matcher          # 4 tests, no network
python eval.py positives.json records.json  # your data
python local_model.py fixtures/pairs.json   # needs Ollama running
```
