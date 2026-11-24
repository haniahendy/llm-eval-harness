"""Deterministic scorers. Each returns 1.0 (pass) or 0.0 (fail).

A case is a dict with an "output" string and a "scorer" name plus the
fields that scorer needs, e.g. {"scorer": "regex", "pattern": "\\d+"}.
"""
from __future__ import annotations

import re


def exact_match(case: dict) -> float:
    return float(case["output"].strip() == case["expected"].strip())


def exact_match_ci(case: dict) -> float:
    return float(case["output"].strip().lower() == case["expected"].strip().lower())


def contains(case: dict) -> float:
    return float(case["substring"].lower() in case["output"].lower())


def regex(case: dict) -> float:
    return float(re.search(case["pattern"], case["output"]) is not None)


def numeric_tolerance(case: dict) -> float:
    """Pass when a number in the output is within tolerance of the target."""
    numbers = re.findall(r"-?\d+(?:\.\d+)?", case["output"])
    target = float(case["target"])
    tol = float(case.get("tolerance", 0.0))
    return float(any(abs(float(n) - target) <= tol for n in numbers))


def json_keys(case: dict) -> float:
    """Pass when the output parses as JSON containing every required key."""
    import json

    try:
        parsed = json.loads(case["output"])
    except (ValueError, TypeError):
        return 0.0
    if not isinstance(parsed, dict):
        return 0.0
    return float(all(k in parsed for k in case["keys"]))


SCORERS = {
    "exact_match": exact_match,
    "exact_match_ci": exact_match_ci,
    "contains": contains,
    "regex": regex,
    "numeric_tolerance": numeric_tolerance,
    "json_keys": json_keys,
}


def score_case(case: dict) -> float:
    name = case["scorer"]
    if name not in SCORERS:
        raise KeyError(f"unknown scorer: {name}")
    return SCORERS[name](case)
