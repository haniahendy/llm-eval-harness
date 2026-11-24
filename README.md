# llm-eval-harness

A small deterministic harness for scoring text outputs (for example from an
LLM) against expectations, with pass rates per scorer.

## What it does

- Cases live in JSONL: one JSON object per line with an `output` string, a
  `scorer` name, and the fields that scorer needs.
- Built-in scorers: `exact_match`, `exact_match_ci`, `contains`, `regex`,
  `numeric_tolerance`, `json_keys`.
- `run.py` prints total/passed/pass-rate plus per-scorer averages and can
  list failing cases. One malformed case fails that case only, not the run.
- No network calls: scoring is fully deterministic and offline. You bring
  the outputs; the harness judges them.

## Usage

```bash
pip install -r requirements.txt
python run.py examples/cases.jsonl --show-failures
```

## Tests

```bash
pytest -q
```

## Honest limits

- Scorers are literal/deterministic. There is no semantic or model-graded
  judging (no LLM-as-judge), so paraphrases of a correct answer fail
  `exact_match`.
- The harness runs and scores saved outputs; it does not call any model
  provider itself.
