# 1. The constraint is dose, not cost

Budget framing (tokens, latency, dollars) suggests the fix is to spend less. Cost is the weaker constraint. Excess intelligence degrades output on its own:

- **Extra context adds distractors.** A dead skill in the listing dilutes retrieval, so the right one competes with wrong ones for the match.
- **A higher tier on a deterministic task buys variance where you wanted a guarantee.** A SHA-256 of test output beats any model judging "did the tests pass," at every tier, forever.
- **More agency on a bounded task invents requirements.** A rule like "if you wrote 200 lines and it could be 50, rewrite it" is a dose limit written as a code rule.

**The asymmetry that makes harnesses accrete.** Underdosing fails loudly, so you fix it. Overdosing fails quietly: fluent, wrong output with no signal that the harness caused it. The feedback loop pushes one direction. Assume drift toward overdose and audit on a schedule ([audit recipe](08-audit.md)).
