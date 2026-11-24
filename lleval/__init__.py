"""A tiny harness for scoring text outputs against expectations."""
from .scorers import SCORERS, score_case
from .runner import run_cases, summarize

__all__ = ["SCORERS", "score_case", "run_cases", "summarize"]
