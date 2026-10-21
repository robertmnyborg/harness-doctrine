# 4. Predicates route. Classifiers guess.

Routing by task classification moves the hard problem rather than solving it. A router that can reliably tell "this is a Type-7 task" has already done the expensive part. Router error compounds: a classifier wrong 10% of the time, dispatching to a specialist that fails off-distribution, loses to always calling the generalist.

A **predicate** is a deterministic test over observable facts: file path matches a regex, command starts with `git commit`, repo has a `.planning/` dir, prompt contains a URL.

| | Predicate | Classifier |
|---|---|---|
| Coverage | Partial, by design | Total, by assumption |
| No match | Abstains, falls through to the generalist | Guesses |
| Failure mode | Fail-safe | Fail-silent |
| Router error | Zero on what it covers | Unknown without an eval |

Reach for a classifier only when a predicate cannot express the distinction, and then treat it as a rung-3 component with an eval behind it ([small specialist](05-small-specialist.md)).

**In practice.** A skill description that says "use whenever you edit server code" fired zero times in 90 days of transcripts. A `PreToolUse` hook that regex-matches the edited file path and injects the same skill fires on every qualifying edit. Same content, different binding time, different mechanism.
