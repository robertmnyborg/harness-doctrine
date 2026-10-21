# 6. Checklist for any new harness component

Run all eight before adding a rule, skill, hook, subagent, MCP server, or cron.

1. **Rung?** Name it. If above 1, say what breaks at rung 1.
2. **Guarantee or estimate?** Guarantee → rung 1, stop here.
3. **Reversible?** No → top rung, ignore cost.
4. **Trigger?** Name the predicate. "The model will notice" is not a trigger.
5. **Binding time?** Always-on requires justifying that it changes behavior in most sessions.
6. **Deletion test.** What fails if this is absent? No answer → don't add it.
7. **Kill condition.** What observation would tell you to remove this later? Write it down now.
8. **Guardrail error.** If it gates or routes: which of the two errors do you refuse to make, and what does each cost? Answer "n/a" only for a component that decides nothing.

For rung-3 components, add: **is it interactive?** If not, batch it before considering a cheaper model.

**Item 4 is the one most often skipped.** A `SKILL.md` `description` is a retrieval hint, not a trigger. Anything with a deterministic predicate belongs in a hook, not in prose that says "use whenever."

**Item 7 exists because components have no natural death.** Without a written kill condition, everything accumulates.

**Item 8 sets the threshold.** A gate tuned without it drifts toward whichever error is quieter, and the quieter error is almost always the one that ships. A commit gate that blocks a good commit costs thirty seconds; one that passes a broken test costs a bad `main`. So it refuses false passes and tolerates false blocks. Say which way yours leans, in the component, next to the threshold.
