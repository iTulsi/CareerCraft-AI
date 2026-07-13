# Release Checklist

## Scope

- [ ] The change solves a stated problem.
- [ ] Existing project code was reused before adding new logic.
- [ ] No unnecessary dependency or abstraction was introduced.
- [ ] The branch contains one understandable release scope.

## Correctness

- [ ] Success paths are tested.
- [ ] Validation and failure paths are tested.
- [ ] Parser changes include a minimal regression fixture.
- [ ] Scoring changes preserve documented invariants or update the methodology.
- [ ] Semantic matching still degrades safely when unavailable.

## Privacy and security

- [ ] No resume or job-description content is logged.
- [ ] Upload size and file-type validation remain enforced.
- [ ] Error responses do not reveal tracebacks or local paths.
- [ ] Report responses remain non-cacheable.
- [ ] No secret, local environment file, or personal fixture is committed.

## Verification

- [ ] Automated tests pass.
- [ ] Python compilation passes.
- [ ] The deterministic benchmark completes.
- [ ] `git diff --check` passes.
- [ ] The final diff contains only intended files.
- [ ] Documentation matches the actual behavior.

## Delivery

- [ ] Commit messages explain the change.
- [ ] The branch is pushed without bypassing protected `main`.
- [ ] The pull request explains scope, validation, risk, and rollback.
- [ ] Deployment smoke tests pass after merge.
