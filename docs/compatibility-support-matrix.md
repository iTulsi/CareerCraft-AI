# Compatibility Support Matrix

This document records the environments and file formats CareerCraft AI is expected to support.

## Runtime

The supported Python version should match the version declared by the repository and deployment platform. Contributors should run the project with that version before reporting compatibility problems.

## Input formats

| Input | Support level | Notes |
|---|---|---|
| Plain text resume | Supported | Must contain readable, non-empty text |
| PDF resume | Supported | Scanned-image-only and encrypted files may be rejected |
| DOCX resume | Supported | Corrupted or password-protected documents may be rejected |
| Job description text | Supported | Must pass request validation |
| Other document formats | Unsupported | Convert to a documented format before upload |

## Analysis modes

| Mode | Availability |
|---|---|
| Deterministic scoring | Core feature |
| Section detection | Core feature |
| Skill comparison | Core feature |
| Semantic similarity | Optional dependency |
| Interview-question generation | Core feature unless documented otherwise |

## Browser and client expectations

The frontend should work in current stable releases of major desktop browsers. API clients should rely on the generated OpenAPI schema rather than undocumented response fields.

## Updating this matrix

Update this document when runtime versions, parser support, public endpoints, or optional-feature requirements change.
