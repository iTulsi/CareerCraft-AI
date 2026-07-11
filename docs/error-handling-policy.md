# Error Handling Policy

CareerCraft AI should fail clearly, safely, and predictably.

## Client errors

Use structured validation responses for unsupported files, empty content, invalid fields, and requests that exceed documented limits. Messages should tell the client what can be corrected.

## Server errors

Unexpected failures should return a stable server-error response without exposing tracebacks, local paths, environment variables, or dependency internals.

## Parsing failures

Distinguish unsupported documents from corrupted, encrypted, or empty documents. Preserve enough internal context for maintainers to diagnose the failure without logging sensitive document text.

## Optional features

A missing model, unavailable embedding dependency, or external provider failure must not break deterministic analysis. Optional capability errors should be reported separately.

## Logging

Log request identifiers, error categories, and safe operational context. Avoid complete request bodies and generated outputs.

## Testing

Each corrected failure mode should receive a regression test that proves both the expected response and the absence of sensitive internal details.
