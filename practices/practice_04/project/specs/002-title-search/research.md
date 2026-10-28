# Research: title-search

Decision: Case-insensitive substring filtering on title via optional q; empty/whitespace-only q rejected with 400; q combines with tag using logical AND.

Rationale: Aligns with user expectation for simple search; preserves existing tag filter semantics; prevents ambiguous empty searches.

Alternatives considered:
- Prefix/word-boundary search: rejected as unnecessarily complex for scope.
- Returning all tasks on empty q: rejected to avoid silent ambiguity; explicit 400 improves client correctness.
- Regex/wildcard search: rejected to keep contract simple and predictable; special characters treated literally.

Clarifications resolved: None outstanding; behavior defined in spec and constitution.
