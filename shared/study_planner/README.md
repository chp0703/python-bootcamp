# Shared Study Planner

The shared Study Planner reads tasks from a CSV file, orders them by importance and deadline, allocates a study-hour budget, and prints a text plan. Run it from the repository root as a Python module.

## Requirements and setup

Use Python 3.10 or newer (the repository CI uses 3.12), Git, and pip. Clone the repository and install its test and lint dependencies:

```bash
git clone https://github.com/chp0703/python-bootcamp.git
cd python-bootcamp
python -m pip install -r requirements.txt
```

The planner itself uses the Python standard library. Run commands from `python-bootcamp/` so the `shared` package and relative CSV paths resolve.

## CSV input

The header must be exactly `title,importance,effort_h,deadline`, in that order. [The supplied sample](../../samples/tasks.csv) contains:

```csv
title,importance,effort_h,deadline
DS exam,5,6,2026-10-30
Assignment,4,1.5,2026-10-27
```

| Column | Meaning |
| --- | --- |
| `title` | Task name shown in the plan. |
| `importance` | Integer priority value; larger values increase priority. The shared task contract describes a 1–5 scale. |
| `effort_h` | Estimated hours, parsed as a decimal number. |
| `deadline` | Calendar date in `YYYY-MM-DD` format. |

The parser checks the exact header and converts row values. The CLI does not call the available `validate_inputs()` helper, so it does not enforce every task-value constraint described by that helper.

## CLI usage

```bash
python -m shared.study_planner samples/tasks.csv --hours 2 --today 2026-10-26
python -m shared.study_planner --help
```

The positional path names the CSV file. `--hours` is required and accepts a numeric study-hour budget. `--today` is optional; supply an ISO date (`YYYY-MM-DD`) for repeatable priority results. If omitted, the CLI uses the machine's current date at startup.

## Processing pipeline

`parse_csv -> prioritise -> allocate -> render`

1. `parse_csv` reads the CSV and creates `Task` objects.
2. `prioritise` sorts tasks in descending order of `importance / max(days_until_deadline, 1)`. An overdue or same-day task uses a divisor of 1.
3. `allocate` walks that order and assigns up to each task's estimated effort until the budget is exhausted. A task may receive a partial block; unused hours remain unused.
4. `render` prints numbered blocks and the allocated total to one decimal place.

`check_feasible()`, `validate_inputs()`, and `summarise_plan()` exist in the shared package but are not called by this CLI pipeline.

## Example output

With the sample above and a fixed date, a two-hour budget gives a partial allocation for the exam:

```bash
python -m shared.study_planner samples/tasks.csv --hours 2 --today 2026-10-26
```

```text
STUDY PLAN
1. Assignment - 1.5 h
2. DS exam - 0.5 h

Total: 2.0 h
```

An eight-hour budget covers both tasks' 7.5 hours of estimated effort:

```bash
python -m shared.study_planner samples/tasks.csv --hours 8 --today 2026-10-26
```

```text
STUDY PLAN
1. Assignment - 1.5 h
2. DS exam - 6.0 h

Total: 7.5 h
```

## Tests

From the repository root, after installing `requirements.txt`:

```bash
python -m pytest -q tests/test_tw3_cli.py
python -m pytest -q
python -m ruff check shared/study_planner tests/test_tw3_cli.py
```

See [the team demo](../../docs/tw3_demo.md) for the results observed on `main` at `3964a1e` and the pending end-to-end and error-test integrations.

## Known limitations and errors

- `argparse` reports missing arguments, nonnumeric `--hours`, and malformed `--today` values as usage errors (exit code 2).
- Negative budgets raise an uncaught `ValueError` traceback. `nan` and `inf` budgets are accepted by the CLI instead of being rejected.
- Missing files, directory paths, empty files, and malformed CSV rows can produce uncaught Python tracebacks. The parser identifies invalid headers and rows, but the CLI does not format those exceptions for users.
- The current CLI allocates partial plans; it does not invoke `check_feasible()` to reject a budget below total task effort.

The seven failing CLI cases are recorded in [the integration report](../../docs/tw3-cli-integration-dmh612.md) and tracked by the shared CLI and error-handling contributions ([PR #62](https://github.com/chp0703/python-bootcamp/pull/62) and [PR #60](https://github.com/chp0703/python-bootcamp/pull/60)).
