# 7. Anti-patterns and their tells

| Anti-pattern | Tell |
|---|---|
| False always-on | A skill saying "use whenever you X" with zero invocations in 90 days |
| Model doing a checkable job | A prompt asking whether something passed, exists, or matches |
| Always-on prose for a rare domain | A `CLAUDE.md` section relevant in under half of sessions |
| Duplicate capability loaded twice | Two MCP servers reaching the same account or workspace |
| Dead weight in the listing | Any skill or plugin with zero invocations over a full audit window |
| Subagent used for speed | Fan-out returning dumps instead of conclusions |
| Silent truncation | A component capping coverage (top-N, sampling) without logging what it dropped |
| Rule with no mechanism | `CLAUDE.md` naming a skill as a label rather than an invocation |
| Nugatory change | A large diff that changes no decision. The agent-work form of reward hacking: rewriting to something generic and safe scores well on "did it change" and zero on "is it better" |
| Gate with one direction priced | A pass/fail check whose docs never say which error it refuses to make |
| Redundant gate that reports nothing upstream | A final check catching what an earlier stage should have caught, logging only pass/fail. What leaks to the last gate is the leading drift signal on the first one |
