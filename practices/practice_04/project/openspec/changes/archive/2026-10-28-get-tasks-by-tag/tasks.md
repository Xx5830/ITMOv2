# Tasks

## 1. Tests first

- [x] 1.1 Add `tests/test_filter_by_tag.py` covering: no tag returns all, matching tag, no match returns `[]`, case-sensitivity, whitespace trimming, empty tag → 400, whitespace-only tag → 400, order preserved. Verify: new tests fail before the implementation (`sh scripts/check.sh`).

## 2. Implementation

- [x] 2.1 Add the optional `tag` query parameter and filtering logic to `GET /tasks` in `app/main.py`. Verify: `sh scripts/check.sh` is fully green, including existing tests.

## 3. Verification

- [x] 3.1 Run `openspec validate get-tasks-by-tag --type change --strict --no-interactive`. Verify: exit code 0.
