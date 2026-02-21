# prompts/

System prompt modules injected into each agent.

## Structure

Every agent receives the **invariants preamble** (`invariants.py`) prepended to its agent-specific instruction.

| File | Contents |
|------|----------|
| `invariants.py` | 7 global invariants enforced across all agents |
| `retriever.py` | Retrieval strategy and JSON output schema |
| `join_analysis.py` | Join mapping rules and JSON output schema |
| `holding.py` | Holding classification with width enforcement |
| `fracture.py` | Fracture typing with cold measurable fields |
| `marks.py` | Marks v. United States analysis with skepticism constraints |
| `synthesis.py` | 8-section report format with clerical voice rules |

## Invariants

1. Grounding (cite block_id + pages)
2. Holding discipline (holding / reasoning / dicta)
3. No narrative collapse (individual attribution)
4. Minimality bias (narrowest reading)
5. Doctrine precision (exact labels)
6. No motive inference (text only)
7. Marks skepticism (flag uncertainty)

## Tuning

Edit any prompt file. Changes take effect on the next query without restarting `adk web`.
