# 9. A routing table in practice

The four questions and the ladder compress into a short table that loads with every session. Each row keys on an **observable requirement**, not a task category, because an observable requirement is a predicate and a category is a classifier.

| Requirement (observable) | Approach |
|---|---|
| One or two files, reversible, you can watch it work | Direct execution |
| Several files, one session, you review each step | Plan mode → execute → verify |
| Work outlives this context window (multi-session, multi-phase) | A phased plan on disk with a validation contract per phase |
| Someone else executes from the artifact (hand-off, multi-reader, future re-entry) | A written spec: requirements, design, tasks |
| Reading costs more than the conclusion is worth | Explore subagents. Demand the conclusion, never the dump |
| The same yes/no, pick-one, or rubric judgment over 50+ items, with code consuming the answer | A rung-3 structured-output model. Draft the schema, run 20 already-labeled rows, report agreement, batch only on a pass. The frontier model keeps extraction, reasoning, and prose |
| No cheap ground truth; the answer is a judgment about what to build | Frontier judgment plus a product-thinking skill. No loop |
| Claims drawn from qualitative customer data | A skill that forces quote-level evidence, because themes are cheap to fabricate |
| A metric moved (drop, spike, divergence) | A diagnosis skill that sizes the drop before naming a cause |
| Changing structure without changing behavior | A refactor skill with a behavior-preservation check |
| Deciding whether a harness component earns its context | A/B it with and without, before cutting |
| Irreversible and outward-facing (prod) | A deploy runbook; explicit confirm before the irreversible step |
| Runs again without you (recurring, CI/CD, batch, monitoring) | Scaffold the agent **and** register it with a closing signal, a guardrail error, and a golden-set decision before it ships |

**A row naming a skill is an instruction to invoke it, not a label.** Write it as `Skill(name)` in your own table, so the model reads a call to make rather than a category to recognize. A table whose rows name skills as labels is the "rule with no mechanism" anti-pattern.

Where a row has a deterministic trigger (a file path, a filename like `PRD.md`, a command prefix), move it out of the table and into a hook. The table is rung 2: read on demand, applied by judgment. A hook is rung 1.
