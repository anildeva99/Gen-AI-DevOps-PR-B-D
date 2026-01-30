import os
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def load_constraints(paths):
    constraints = {}

    for p in paths:
        abs_path = os.path.join(BASE_DIR, p)

        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Constraint file not found: {abs_path}")

        with open(abs_path, "r") as f:
            data = yaml.safe_load(f) or {}
            constraints.update(data)

    return constraints


def evaluate(constraints, pr_title: str, files: list):
    """
    Simple constraint evaluation:
    - PR title must contain at least one required keyword
    - Block if forbidden files are modified
    """

    # Title rules
    required = constraints.get("required_keywords", [])
    if required:
        if not any(k.lower() in pr_title.lower() for k in required):
            return False, f"PR title must contain one of: {required}"

    # Forbidden files
    forbidden = constraints.get("forbidden_files", [])
    for f in files:
        for blocked in forbidden:
            if blocked in f:
                return False, f"Forbidden file modified: {f}"

    return True, "All constraints satisfied"

