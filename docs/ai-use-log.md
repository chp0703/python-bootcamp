# AI use log

## 2026-10-26 - Member 2, Python bootcamp W3

- Author: Huỳnh Nguyễn Thế Hiển (`@AIVIETNAM-AIO-TheHien`).
- Tool: OpenAI Codex.
- Scope: W3-1 to W3-4, personal regression tests, focused CI checks, and documentation.
- Issue: [#68](https://github.com/chp0703/python-bootcamp/issues/68).
- Pull request: [#69](https://github.com/chp0703/python-bootcamp/pull/69).

### Assistance retained

Codex generated the due-date parser, route-latency analysis, CLI adapter from the personal W2 model to the shared Task contract, focused edge-case tests, and strict personal CI steps. Codex also added type hints/docstrings and formatted this member's existing W1-W2 code, and drafted the progress and PR text.

### Design and verification

- Named weekdays mean the strictly next occurrence, including seven days later for the current weekday.
- p95 uses the nearest-rank convention; an empty log has no slowest route, and ties preserve first-seen route order.
- The CLI reuses the personal W2 CSV loader and reports its line-number errors. It allocates a partial plan rather than requiring all task effort to fit in the available hours.
- Official W1-W3 tests, personal W3 edge tests, and W2 cross-tests: **51 passed**.
- Repository regression after syncing `main`: **110 passed, 7 failed, 11 skipped**. The failures are existing shared CLI error scenarios (invalid numeric hours, missing paths, directory input, and empty files) in `tests/test_tw3_cli.py`. The skipped instructor cases require `--member` and are exercised in the dedicated personal run.
- Personal edge tests use a unique filename and a namespace package to avoid pytest module collisions across member folders.
- Ruff lint and formatting checks passed. All personal functions have annotations and docstrings.

The author still needs to review the retained code and be able to explain each line during the individual defense. Peer review and merging are recorded separately on the pull request.
