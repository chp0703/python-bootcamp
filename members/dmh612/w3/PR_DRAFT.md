# py-w3: dmh612

## What

Implement W3-1 through W3-4 for dmh612: deadline parsing, per-route request
counts and nearest-rank p95, and a study-planner CLI reusing the W02 loader
and model. Complete personal W01/W02 function annotations and docstrings.

## How tested

- `python -m ruff check members/dmh612`: passed.
- `python -m pytest -q tests/test_w3.py tests/test_w2.py members/dmh612/w3/test_w3_edges.py members/dmh612/w2/tests_for_chp0703.py --member dmh612`: 41 passed locally.
- Covers leap days, weekday rollover, empty logs, percentile boundaries,
  priority changes with `--today`, partial allocation, CSV errors, and CLI exits.

## Python versus C++ — proposed lines for the student to review

1. Python type hints document intended types; unlike C++ declarations, they do not enforce those types at runtime.
2. `Counter` and `defaultdict(list)` replace manual map initialisation for request counts and grouped latencies.
3. `python -m` executes a module in its package, so relative imports can reuse W02 code without editing the module search path.

## AI use

Codex generated the W03 implementation, tests, documentation, and W01/W02
type/docstring changes. Codex ran the checks above. Student review and any
student edits are pending; see `docs/ai-use-log.md`.

## Submission status

Prepared locally on `py/w3-dmh612`. No issue/PR link or peer approval is
claimed. Git push failed because the local credential manager could not
authenticate. Link the real issue and request the assigned reviewer when
opening the PR. Do not merge before review.
