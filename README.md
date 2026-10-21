# Python Bootcamp — Group 03

This repository contains the individual assignments and collaborative programming projects of **Group 03** for the Python Bootcamp.

---

## Team Members

| No. | Member | GitHub Username | Student ID |
|:---:|---|---|:---:|
| 1 | Member 1 | [@chp0703](https://github.com/chp0703) | 25127224 |
| 2 | Member 2 | [@AIVIETNAM-AIO-TheHien](https://github.com/AIVIETNAM-AIO-TheHien) | 25127327 |
| 3 | Member 3 | [@phkhoiit-1508](https://github.com/phkhoiit-1508) | 25127390 |
| 4 | Member 4 | [@kentlatoi](https://github.com/kentlatoi) | 25127369 |
| 5 | Member 5 | [@thanhhuong107](https://github.com/thanhhuong107) | 25127197 |
| 6 | Member 6 | [@dmh612](https://github.com/dmh612) | 25127340 |

---

## Repository Structure

```text
python-bootcamp/
├── .github/
│   ├── ISSUE_TEMPLATE/       # Reusable issue templates
│   └── workflows/            # GitHub Actions workflows
│
├── members/                  # Individual assignments
│   └── <username>/
│       └── w<week>/          # Exercises organized by week
│
├── samples/                  # Sample files and input data
│
├── shared/                   # Shared code and project modules
│
├── tests/                    # Automated tests
│
├── requirements.txt          # Python dependencies
├── PROGRESS.md               # Weekly tasks and progress tracking
└── README.md                 # Repository documentation
```

---

## Getting Started

### Requirements

- Python 3
- Git
- pip

### Installation

Clone the repository:

```bash
git clone https://github.com/chp0703/python-bootcamp.git
cd python-bootcamp
```

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

### Running Tests

Run the automated test suite from the repository root:

```bash
python -m pytest -v
```

To run a specific test file:

```bash
python -m pytest tests/<test_file>.py -v
```

---

## Development Workflow

The team uses Git and GitHub to manage changes and collaborate.

1. Review or create an Issue describing the task.
2. Create a dedicated branch for the task.
3. Implement the required changes and add relevant tests.
4. Commit and push the changes to GitHub.
5. Open a Pull Request for code review.
6. Address review feedback and merge the approved changes.

Each contribution should follow the repository's conventions and include appropriate tests where applicable.

---

## Reviewer Rotation

Reviewers rotate among team members according to the following cycle:

1. Member 1 reviews Member 2.
2. Member 2 reviews Member 3.
3. Member 3 reviews Member 4.
4. Member 4 reviews Member 5.
5. Member 5 reviews Member 6.
6. Member 6 reviews Member 1.

**Rotation:** Member 1 → Member 2 → Member 3 → Member 4 → Member 5 → Member 6 → Member 1

---

## Progress Tracking

`PROGRESS.md` contains the detailed weekly assignments, task ownership, completion status, testing results, and relevant pull requests.

Please refer to that file for the current development status and weekly requirements.

---

## Collaboration Guidelines

- Keep individual assignments organized by member and week.
- Place shared code in the appropriate shared directories.
- Write tests for implemented functionality.
- Use descriptive commit messages and pull request descriptions.
- Keep changes focused and request review before merging.
- Update progress records as work is completed.

