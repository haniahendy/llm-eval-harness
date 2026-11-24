import json

import pytest

from lleval import run_cases, score_case, summarize


def test_exact_match_strips_whitespace():
    assert score_case({"scorer": "exact_match", "expected": "yes", "output": " yes \n"}) == 1.0
    assert score_case({"scorer": "exact_match", "expected": "yes", "output": "Yes"}) == 0.0


def test_exact_match_case_insensitive_variant():
    assert score_case({"scorer": "exact_match_ci", "expected": "Yes", "output": "yes"}) == 1.0


def test_contains_is_case_insensitive():
    assert score_case({"scorer": "contains", "substring": "Paris", "output": "paris is nice"}) == 1.0
    assert score_case({"scorer": "contains", "substring": "london", "output": "paris is nice"}) == 0.0


def test_numeric_tolerance_finds_number_in_text():
    assert score_case({"scorer": "numeric_tolerance", "target": 42, "tolerance": 0.5,
                       "output": "about 41.8, roughly"}) == 1.0
    assert score_case({"scorer": "numeric_tolerance", "target": 42, "tolerance": 0.5,
                       "output": "about 10"}) == 0.0


def test_json_keys_requires_all_keys_and_valid_json():
    assert score_case({"scorer": "json_keys", "keys": ["a"], "output": '{"a": 1, "b": 2}'}) == 1.0
    assert score_case({"scorer": "json_keys", "keys": ["a", "c"], "output": '{"a": 1}'}) == 0.0
    assert score_case({"scorer": "json_keys", "keys": ["a"], "output": "not json"}) == 0.0


def test_unknown_scorer_raises():
    with pytest.raises(KeyError):
        score_case({"scorer": "nope", "output": "x"})


def test_run_cases_and_summarize(tmp_path):
    cases = [
        {"name": "ok", "scorer": "contains", "substring": "hi", "output": "hi there"},
        {"name": "bad", "scorer": "contains", "substring": "hi", "output": "bye"},
        {"name": "err", "scorer": "unknown", "output": "x"},
    ]
    path = tmp_path / "cases.jsonl"
    path.write_text("\n".join(json.dumps(c) for c in cases))
    results = run_cases(path)
    summary = summarize(results)
    assert summary["total"] == 3
    assert summary["passed"] == 1
    assert summary["errored"] == 1
    assert summary["pass_rate"] == pytest.approx(1 / 3, abs=1e-4)
