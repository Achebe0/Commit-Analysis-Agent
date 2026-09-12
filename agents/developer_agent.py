from pathlib import Path

import item

from agents.state import State



def build_default_fix_plan(issue_analysis: str, suspect_commits: list[str]) -> str:
    commit_text = ", ".join(suspect_commits) if suspect_commits else "latest deployment"

    return f"""## Incident summary

{issue_analysis}

## Likely affected commit(s)

- {commit_text}

## Recommended fix

1. Confirm the failing service and the deployment window.
2. Roll back to the last known good deploy if the issue matches the latest rollout.
3. Fix the broken config or code path that matches the error signature.
4. Re-run the smallest validation pass: unit tests and a smoke check.
5. Redeploy only after validation passes.

## Example patch idea

```python
# Example guard for a missing required config value
required = ["SERVICE_URL"]
for item in required:
    if not os.getenv(item):
        raise RuntimeError(f"Missing required env var: {item}")
```
"""


def generate_fix_plan(state: State, output_file: str | None = None) -> str:
    issue_analysis = state.get("issue_analysis") or "No issue analysis was found."
    suspect_commits = state.get("suspect_commits") or []

    plan = build_default_fix_plan(issue_analysis, suspect_commits)
    state["fix_plan"] = plan
    state["solution_markdown"] = plan

    if output_file:
        create_markdown_file(output_file, "Solution", plan)

    return plan




def create_markdown_file(file_path, title: str, body: str):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# {title}\n\n{body}", encoding="utf-8")
    return str(path)


def developer_agent(state: State, issue_analysis: str, output_file: str) -> str:
    state["issue_analysis"] = issue_analysis
    return generate_fix_plan(state, output_file)

