# Dependency Update Policy

Dependency changes should be deliberate, reviewable, and limited to verified project needs.

## Before adding a dependency

Confirm that:

1. the standard library or existing framework cannot solve the requirement clearly;
2. an existing project dependency does not already provide the capability;
3. the package is actively maintained;
4. its license is compatible with the project;
5. its security and transitive dependency impact is acceptable; and
6. the added complexity is justified.

## Updating dependencies

Use focused updates rather than changing unrelated packages together. Review release notes for breaking changes, security fixes, runtime support, and removed behavior.

## Verification

After an update:

- install from a clean environment;
- run the full test suite;
- run the benchmark when analysis behavior could change;
- test supported PDF and DOCX parsing;
- confirm optional semantic analysis still degrades safely; and
- review the lockfile or requirements diff.

## Removing dependencies

Remove packages that are unused, duplicated, abandoned, or replaceable by simpler native functionality. Delete related configuration and tests only after confirming nothing still imports the package.

## Emergency security updates

Apply the smallest safe upgrade, document the affected component, run verification, deploy promptly, and record the fixed commit.
