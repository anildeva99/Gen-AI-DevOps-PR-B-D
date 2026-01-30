# Day50/pr_agent/utils/github_client.py

import os
from github import Github
from github.Auth import Token


def _get_github_token() -> str:
    """
    Prefer PR_AGENT_GITHUB_TOKEN (our secret),
    fallback to GITHUB_TOKEN for GitHub Actions compatibility.
    """
    token = os.getenv("PR_AGENT_GITHUB_TOKEN") or os.getenv("GITHUB_TOKEN") or ""
    return token.strip()  # IMPORTANT: removes hidden newline/space


def get_pr_files_and_diff(repo_name: str, pr_number: int):
    token = _get_github_token()
    if not token:
        raise ValueError("Missing GitHub token. Set PR_AGENT_GITHUB_TOKEN (recommended) or GITHUB_TOKEN.")

    # New PyGithub recommended way (also removes deprecation warning)
    gh = Github(auth=Token(token))

    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    # Collect files
    files = [f.filename for f in pr.get_files()]

    # Collect diff (patches may be None for binary/large files)
    diffs = []
    for f in pr.get_files():
        if f.patch:
            diffs.append(f"--- {f.filename}\n{f.patch}")
        else:
            diffs.append(f"--- {f.filename}\n(no patch available)")

    full_diff = "\n\n".join(diffs)
    return files, full_diff
