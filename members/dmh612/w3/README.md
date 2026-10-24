# W03 individual — dmh612

## Run from the repository root

```powershell
python -m pip install -r requirements.txt
python -m members.dmh612.w3.cli samples/tasks.csv --hours 2 --today 2026-10-26
```

Expected output:

```text
Tonight (2.0 h):
1. Assignment ...... 1.5 h
2. DS exam ...... 0.5 h
```

## Exercise decisions

- W3-1: ISO `YYYY-MM-DD`, `tomorrow`, `in N days`, abbreviated/full English
  weekday names. Weekdays always mean a strictly later occurrence; invalid
  expressions raise `ValueError`. Relative expressions ignore case/outer spaces.
- W3-2: `Counter` request counts, nearest-rank p95 (index `ceil(0.95*n)-1`).
  Empty logs return `slowest=None`; tied routes resolve alphabetically.
  Negative, NaN, and infinite latency values raise `ValueError`.
- W3-3: reuse W02 `load_tasks`, `Task`, and `days_left`. Sort by descending
  `importance / max(days_left, 1)`; ties keep CSV order. Allocate partial tasks
  up to the budget. `--today` controls priority reproducibly.
  Missing/invalid CSV returns 1; invalid command arguments return 2.
  Hours must be finite and positive. A header-only CSV prints no tasks.
- W3-4: type annotations and docstrings cover all personal bootcamp functions,
  including W01/W02. No shared planner modules are changed.

## Verify

```powershell
python -m ruff check members/dmh612
python -m pytest -q tests/test_w3.py tests/test_w2.py members/dmh612/w3/test_w3_edges.py members/dmh612/w2/tests_for_chp0703.py --member dmh612
```

Local result: Ruff passed; 41 tests passed. These checks do not establish
that a GitHub CI run or peer review has occurred.

## Explain the code before submitting

Be ready to explain modulo-seven weekday arithmetic, the p95 index,
`defaultdict`/`Counter`, stable sorting, argparse exit codes, and why a
partial evening plan does not call W02 `check_feasible` on all tasks.

The PR draft contains three proposed comparison lines. Review them and
replace them with your own observations before submitting.
