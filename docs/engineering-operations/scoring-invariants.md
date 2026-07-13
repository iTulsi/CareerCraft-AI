# Scoring Invariants

CareerCraft's deterministic assessment is intentionally explainable.

```text
overall score = 75% job-skill coverage + 25% resume-section coverage
```

```text
job-skill coverage = matched requested skills / detected requested skills
```

```text
resume-section coverage = detected core sections / 4
```

The core sections are Skills, Experience, Projects, and Education.

## Required properties

1. Scores remain within the documented range.
2. The same normalized inputs produce the same deterministic result.
3. Matched and missing skills are derived from the same requested-skill set.
4. A missing skill is never also reported as matched.
5. Recommendations correspond to observable gaps in the analysis.
6. Semantic similarity remains a separate signal and is not silently blended
   into the deterministic score.
7. A result is described as an assessment, not as an official employer ATS
   score or hiring probability.
8. Empty or insufficient inputs are rejected instead of receiving a misleading
   score.
9. Rounding is applied only for presentation; internal calculations should
   retain enough precision for consistent tests.

## Change review

A scoring change requires:

- a written reason for changing the formula or vocabulary,
- updated unit tests for boundaries and representative examples,
- benchmark comparison against the current baseline,
- documentation of any score shifts users may notice,
- confirmation that the UI explanation still matches the implementation.
