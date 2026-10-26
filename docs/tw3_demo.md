# T-W3 Study Planner demo

## Purpose and setup

This demo runs the shared CLI with a fixed date so teammates and reviewers can reproduce the same task order and output. Use Python 3.10 or newer from the repository root:

```bash
git clone https://github.com/chp0703/python-bootcamp.git
cd python-bootcamp
python -m pip install -r requirements.txt
```

The input is [`samples/tasks.csv`](../samples/tasks.csv):

```csv
title,importance,effort_h,deadline
DS exam,5,6,2026-10-30
Assignment,4,1.5,2026-10-27
```

## Run the demo

### Partial allocation: two hours

```bash
python -m shared.study_planner samples/tasks.csv --hours 2 --today 2026-10-26
```

Observed output (exit code 0):

```text
STUDY PLAN
1. Assignment - 1.5 h
2. DS exam - 0.5 h

Total: 2.0 h
```

### All task effort: eight hours available

```bash
python -m shared.study_planner samples/tasks.csv --hours 8 --today 2026-10-26
```

Observed output (exit code 0):

```text
STUDY PLAN
1. Assignment - 1.5 h
2. DS exam - 6.0 h

Total: 7.5 h
```

On 2026-10-26, Assignment is due in one day, so its score is `4 / 1 = 4`; DS exam is due in four days, so its score is `5 / 4 = 1.25`. The planner schedules Assignment first, then uses the remaining budget for DS exam. The eight-hour run leaves 0.5 h unused because the two tasks require 7.5 h in total. The CLI follows `parse_csv -> prioritise -> allocate -> render` and permits a partial final block.

## Verification on `main` at `304b443`

The following commands were run from the repository root with Python 3.12.8 and the repository's `.venv` (which has pytest and Ruff installed). A fresh clone can use `python` after installing `requirements.txt`.

| Command | Exit | Observed result |
| --- | ---: | --- |
| `python -m shared.study_planner samples/tasks.csv --hours 2 --today 2026-10-26` | 0 | Exact 2.0 h output above. |
| `python -m shared.study_planner samples/tasks.csv --hours 8 --today 2026-10-26` | 0 | Exact 7.5 h output above. |
| `python -m shared.study_planner --help` | 0 | Shows positional `csv_path`, required `--hours`, optional `--today`. |
| `.venv/bin/python -m pytest -q tests/test_tw3_cli.py` | 1 | 15 passed, 7 failed. |
| `.venv/bin/python -m pytest -q tests/test_tw3_e2e.py` | 0 | 3 passed. |
| `.venv/bin/python -m pytest -q` | 1 | 113 passed, 7 failed, 11 skipped. |
| `.venv/bin/python -m ruff check shared/study_planner tests/test_tw3_cli.py` | 1 | Two `TRY004` findings in `shared/study_planner/validate.py`. |

`tests/test_tw3_e2e.py` is now on `main` through [PR #71](https://github.com/chp0703/python-bootcamp/pull/71). `tests/test_tw3_errors.py` was merged into the feature branch of [PR #60](https://github.com/chp0703/python-bootcamp/pull/60) by [PR #54](https://github.com/chp0703/python-bootcamp/pull/54), but is not present on this `main` revision, so that focused test file was not run here.

The seven CLI failures cover negative or non-finite hour budgets, missing files, directory input, and empty files. Negative budgets and file errors currently show tracebacks; `nan` and `inf` can produce successful plans. The CLI does not call the shared validation or feasibility helpers. See the [usage guide](../shared/study_planner/README.md) and [CLI integration report](tw3-cli-integration-dmh612.md) for details. The current CI workflow runs its broad Ruff and pytest checks with `|| true`, so a green job alone does not establish a passing suite.
