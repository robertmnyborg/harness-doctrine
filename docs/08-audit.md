# 8. Audit recipe

Run it quarterly, after every model release, or when sessions feel slow. Claude Code transcripts live in `~/.claude/projects/**/*.jsonl`.

```bash
# skill invocations, 90 days
find ~/.claude/projects -name '*.jsonl' -mtime -90 -print0 \
  | xargs -0 grep -hoE '"skill":"[a-z0-9:_-]+"' | sed 's/"skill":"//;s/"//' \
  | sort | uniq -c | sort -rn

# MCP calls by server, 90 days
find ~/.claude/projects -name '*.jsonl' -mtime -90 -print0 \
  | xargs -0 grep -hoE '"name":"mcp__[a-zA-Z0-9_-]+__' \
  | sed 's/"name":"mcp__//;s/__$//' | sort | uniq -c | sort -rn

# subagent launches by type, 90 days
find ~/.claude/projects -name '*.jsonl' -mtime -90 -print0 \
  | xargs -0 grep -hoE '"subagent_type":"[a-zA-Z0-9:_-]+"' \
  | sed 's/"subagent_type":"//;s/"//' | sort | uniq -c | sort -rn

# always-on cost of a file, in tokens (~4 chars/token)
wc -c ~/CLAUDE.md | awk '{print $1/4" tok"}'
```

Zero calls means the component pays listing cost for nothing. The first subagent audit on this harness put all 25 custom agent definitions at zero invocations over 90 days, while the two built-in agent types took all 35 launches. The custom listing was pure overhead.

Before cutting something with plausible value, A/B it: run the same task scenarios with and without the component in context and compare pass rates. Guessing is how harnesses accrete in the first place.

**Whole-harness ablation.** After a model release or a large `CLAUDE.md` edit, re-run a set of incident-derived cases three ways: full harness, harness with scaffolding stripped, and bare. A rule that no longer changes the outcome on the current model is a deletion candidate.
