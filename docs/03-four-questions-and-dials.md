# 3. The four questions, then the four dials

## The four questions about the outcome

Answer these before touching a dial. They are facts about the task, checkable up front, so they carry no router error ([predicates over classifiers](04-predicates-over-classifiers.md)). Domain ("frontend", "strategy", "data") tells you nothing and is not one of them.

Answer them **per step, not per task**. A single job often splits: the dedupe is a guarantee, the send is irreversible, the fit-scoring is a judgment.

| # | Question | Answer | What it sets |
|---|---|---|---|
| 1 | **Guarantee or estimate?** Does something downstream *trust* this, or does a human read it and decide? | Guarantee | Rung 1. No model at any tier. Stop. |
| 2 | **Reversible?** Undoable in a minute, alone, with nobody having seen it? | No | Top rung + explicit confirm, ignore cost. |
| 3 | **Ground truth cheap?** Can a script tell right from wrong with no human reading output? | Yes | Licenses automation, specialization, unattended loops. |
| 4 | **Interactive?** Are you waiting on it? | No | Batch or cron it. Keep the tier. |

Tells and traps:

- **Q1** fires on "check that", "verify", "make sure", "confirm" in the ask. Those name a checkable fact, and a model's fluency on a checkable fact is a liability: confident-right and confident-wrong arrive identical.
- **Q2** catches tasks that look mechanical and aren't. "Push these 250 leads into the outreach tool" reads as data plumbing and is 250 unsendable messages under your name.
- **Q3 gates autonomy, not model choice.** Cheap ground truth means drift announces itself, so a cron or a loop is safe. Expensive ground truth means every run needs a human read, so a loop multiplies review work instead of removing it.
- **Q4** is worth more than a tier downgrade. Batch APIs typically take 50% off any model, so a batched frontier call can undercut the mid tier at list price ([delivery mode](05-small-specialist.md#delivery-mode-beats-tier)).

Worked tuples:

| Task | Q1 | Q2 | Q3 | Q4 | Falls out as |
|---|---|---|---|---|---|
| Add a column to an internal dashboard | estimate | reversible | cheap (it renders) | interactive | Main loop, no ceremony |
| Push the week's leads into an outreach tool | dedupe is a **guarantee** | send is **irreversible** | fit-scoring expensive | non-interactive | Rung-1 ledger dedupe + human approve gate + batch |
| Is this spec ready for the reviewer? | estimate | reversible | **expensive** | interactive | Frontier judgment. No eval, no specialist, no loop. |

## The four dials

Set in this order. Each constrains the next.

**1. Level.** Pick the rung ([ladder](02-ladder.md)), honoring both overrides.

**2. Place.** Follows from level.

| Level | Place |
|---|---|
| 0-1 | Hook, scheduled job, or a script on `$PATH` |
| 2 | Retrieval tool, or a file the agent reads on demand |
| 3 | A tool call with a fixed output schema |
| 4-5 | Main loop, or a subagent |
| 6 | Fan-out (workflow, parallel agents) |

Choose a subagent when the work requires reading more than the conclusion is worth. The payoff is the context firewall, not the speed. Demand the conclusion back, never the dump.

**3. Time.** When it arrives. Ranked best to worst:

1. Fired by a predicate at the moment of the decision (hook)
2. Loaded by explicit invocation (skill, slash command)
3. Always-on prose (`CLAUDE.md`, memory files)

Later binding wins. Content attached to a decision gets acted on. The same content arriving 200 turns early gets ignored. Reserve always-on for what changes behavior in **most** sessions; everything else is late-bound.

**4. Amount.** Context and agency: the minimum that clears the bar. Test by deletion: remove a piece and see if the task still passes. Anything removable without failure was never load-bearing. It was competing for attention with what was.
