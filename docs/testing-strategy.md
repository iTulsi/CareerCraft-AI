# Testing Strategy

CareerCraft AI uses automated tests to protect observable product behavior rather
than implementation details.

## Main test areas

- health and frontend routes
- PDF, DOCX, and TXT parsing
- unsupported, malformed, and oversized uploads
- request-model validation
- deterministic skill matching
- resume-section detection
- optional semantic-model behavior
- interview-question generation
- report validation and download behavior
- benchmark input and output handling

## Local commands

Run the complete test suite:

```bash
make test
```

Run the broader verification workflow:

```bash
make verify
```

The verification target runs the tests, compiles the backend package, and runs
the deterministic benchmark. New behavior should include both a meaningful
success case and the most important failure case.
