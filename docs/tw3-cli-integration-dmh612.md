# T-W3 CLI integration report - dmh612

Checked on 2026-10-26, Windows, Python 3.12.14.

## Scope

Member 6: CLI arguments, invalid CLI input, and operation from a fresh clone.
Deliverable: tests/test_tw3_cli.py. The suite launches the actual public command
in subprocesses; it does not mock argparse or call another member's personal CLI.

## Revisions and results

| Target | Revision | Result |
| --- | --- | --- |
| main | b87f7eb5032370fdfa65ce8dae89ce9f032aa51a | Cannot run the shared CLI: shared.study_planner.__main__ is absent. |
| PR #62, py/tw3-chp0703 | 242d7afee485a96d4b973e8f62b3e64ddf272309 | 15 passed, 7 failed across 22 test cases. |

PR #62: https://github.com/chp0703/python-bootcamp/pull/62
PR #60 (separate domain-error work): https://github.com/chp0703/python-bootcamp/pull/60

These results apply to PR #62 alone. They are not a claim that PR #60 has been
merged or that the combined implementation has passed integration checks.

## Fresh-clone check

1. Cloned the public repository with --branch py/tw3-chp0703 --single-branch
   into a new directory.
2. Copied only tests/test_tw3_cli.py into that clone.
3. Verified that tracked project files had no changes.
4. Ran the suite with Python 3.12.14 and pytest 9.1.1.
5. Each CLI subprocess removes inherited PYTHONPATH, runs from the clone root,
   and has a 15-second timeout. The project was not installed as an editable
   package. Runtime code uses only the standard library.

The root-relative sample command works on this clone:

```powershell
python -m shared.study_planner samples/tasks.csv --hours 8 --today 2026-10-26
```

The test uses eight hours so the 7.5-hour sample is feasible under either
partial-allocation or strict feasibility policies.

## Passing cases (15)

- Help without mandatory planning arguments: 1.
- Missing required arguments: 3.
- Non-numeric hours: 3.
- Invalid calendar dates or unsupported date text: 3.
- Unknown option: 1.
- Fractional hours with spaces in the input path: 1.
- Default --today: 1.
- Repository sample with a fixed --today and expected ordering: 1.
- Changing --today actually changes task priority: 1.

## Failed cases (7)

| Input | Observed | Expected |
| --- | --- | --- |
| --hours=-1 | ValueError traceback | Nonzero exit with a readable error on stderr, no plan/traceback |
| --hours=nan | Exit 0; renders a plan | Reject a non-finite budget |
| --hours=inf | Exit 0; renders a plan | Reject a non-finite budget |
| --hours=-inf | ValueError traceback | Reject a non-finite budget without a traceback |
| Missing CSV | FileNotFoundError traceback | Nonzero exit with the missing path and a readable error |
| Directory used as CSV | OS exception traceback | Nonzero exit with a readable error |
| Empty CSV | ValueError traceback | Nonzero exit with a readable header/empty-file error |

The suite intentionally retains failing assertions. No skips or xfails hide
these integration defects. Zero-hour and infeasible-plan policies are left
for the team to agree; this suite does not impose a new contract for them.

## Integration follow-up

- Integrate the CLI entry point and the team's domain-error work.
- Validate finite, non-negative hours. The existing validate_inputs helper
  already provides this validation but PR #62 does not call it.
- Handle expected file/validation/domain exceptions at the CLI boundary,
  write a clear message to stderr, and return a nonzero exit code.
- Rerun this suite after integration and update this report with the new SHA
  and actual result. No changes to shared runtime code are included here.

## Reproduce

From the repository root after integrating the CLI:

```powershell
python -m pip install -r requirements.txt
python -m ruff check tests/test_tw3_cli.py
python -m pytest -q tests/test_tw3_cli.py
```

Ruff check on the delivered test file passed. On main without the CLI entry
point, test failures are expected; this is a dependency, not a passing run.
The existing CI uses `pytest -q || true`, so a green job alone does not prove
that all tests passed. Inspect the pytest summary.

## AI use

OpenAI Codex generated this suite and report and executed the checks above.
Student review is pending. Add this T-W3 entry to the existing
`docs/ai-use-log.md` and disclose it in the PR when submitting.
No peer review, approval, merge, or GitHub CI success is claimed.
