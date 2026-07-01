# Changelog

Notable project changes are recorded in this file.

## Unreleased

### Repository quality

- Added automated verification through GitHub Actions.
- Added root-level pytest configuration.
- Added contributor and security documentation.
- Documented the application architecture and API usage.

## 0.3.0

### Added

- Resume parsing for PDF, DOCX, and TXT files.
- Explainable deterministic skill matching.
- Resume-section assessment.
- Optional semantic similarity comparison.
- Tailored interview-practice questions.
- Downloadable analysis reports.
- Labelled benchmark evaluation.
- Browser frontend served by FastAPI.

### Safety and limitations

- Upload validation and a 5 MB document limit.
- Explicit separation between heuristic and semantic scores.
- Clear warnings that results are not employer ATS scores or hiring
  probabilities.
