# DAP Plan Demo — Three Scenarios

## Scenario A: Precedent + Marks

**Query:** "What is the narrowest controlling principle under Marks in Learning Resources v. Trump?"

**Features:**
```json
{
  "intents": {
    "precedent": true,
    "marks": true,
    "compliance": false,
    "commentary_assessment": false,
    "factual_summary": false
  },
  "keywords": ["controlling", "marks", "narrowest ground"],
  "triggered_rules": [
    {"intent": "precedent", "type": "keyword", "match": "controlling"},
    {"intent": "marks", "type": "keyword", "match": "marks"},
    {"intent": "marks", "type": "keyword", "match": "narrowest ground"}
  ]
}
```

**DAG:**
```
retrieval → vote_structure → holdings → fractures → marks → synthesis
```

**Execution trace:**
- All 6 agents run
- Synthesis includes Sections 1-9 (all sections)
- Corpus scope: SCOTUS opinions + Section 122 (no NR)

---

## Scenario B: Compliance

**Query:** "Does the Section 122 proclamation satisfy the statute's balance-of-payments predicate?"

**Features:**
```json
{
  "intents": {
    "precedent": false,
    "marks": false,
    "compliance": true,
    "commentary_assessment": false,
    "factual_summary": false
  },
  "keywords": ["satisfy", "predicate", "section 122"],
  "triggered_rules": [
    {"intent": "compliance", "type": "keyword", "match": "satisfy"},
    {"intent": "compliance", "type": "keyword", "match": "predicate"},
    {"intent": "compliance", "type": "keyword", "match": "section 122"},
    {"intent": "compliance", "type": "pattern", "match": "does the section 122 proclamation satisfy"}
  ]
}
```

**DAG:**
```
retrieval → synthesis
```

**Execution trace:**
- 2 agents run (retrieval + synthesis)
- Synthesis omits Sections 2-6 (Vote, Holdings, Fractures, Marks, Doctrinal)
- Report contains: Query & Scope, Open Questions, Citation Index
- Corpus scope: SCOTUS opinions + Section 122 (no NR)

---

## Scenario C: Commentary Assessment

**Query:** "Assess McCarthy's National Review claims about Section 122 against the statutory text"

**Features:**
```json
{
  "intents": {
    "precedent": false,
    "marks": false,
    "compliance": false,
    "commentary_assessment": true,
    "factual_summary": false
  },
  "keywords": ["national review", "mccarthy", "assess claims"],
  "triggered_rules": [
    {"intent": "commentary_assessment", "type": "keyword", "match": "national review"},
    {"intent": "commentary_assessment", "type": "keyword", "match": "mccarthy"},
    {"intent": "commentary_assessment", "type": "keyword", "match": "assess claims"},
    {"intent": "commentary_assessment", "type": "pattern", "match": "assess mccarthy's national review claims"}
  ]
}
```

**DAG:**
```
retrieval → synthesis
```

**Execution trace:**
- 2 agents run (retrieval + synthesis)
- Retriever includes NR corpus in scope
- Synthesis includes Section 7 (External Commentary Assessment)
- Corpus scope: ALL corpora (SCOTUS + Section 122 + National Review)
