# Quickstart Validation: title-search

## Prerequisites

- Python virtual environment activated
- Run tests with: sh scripts/check.sh

## Scenarios

1) Search by partial title (case-insensitive)
- Create tasks: POST /tasks {"title":"Buy milk","tags":["shop"]}, POST /tasks {"title":"Read book","tags":["read"]}
- GET /tasks?q=milk → 200, ["Buy milk"]
- GET /tasks?q=MILK → 200, ["Buy milk"]

2) Reject empty q
- GET /tasks?q= → 400 with detail
- GET /tasks?q=%20%20 → 400 with detail

3) Combine q with tag
- Create: {"title":"Milk report","tags":["work"]}
- GET /tasks?q=milk&tag=work → 200, ["Milk report"]

Expected: Ordering matches creation order; no regressions when q omitted.
