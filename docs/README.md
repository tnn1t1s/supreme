# docs/

Decision corpus storage. One subdirectory per case.

## Structure

```
docs/decision/{date}_{case-name}_{docket}/
  source/       slip opinion PDF (gitignored)
  extracted/    full text per opinion (markdown)
  blocks/       segmented blocks with YAML frontmatter
  manifest.json complete metadata index
```

## Current Cases

| Case | Docket | Decided | Blocks | Opinions |
|------|--------|---------|--------|----------|
| Learning Resources, Inc. v. Trump | 24-1287 | 2026-02-20 | 53 | 8 |
