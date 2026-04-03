# New Strategy Experiments

This note summarizes the two new strategy tracks added in this round:

- `Mara`: a pure Grok-driven player
- `Nadia`: a fully local custom controller designed from scratch for this repo and tuned by search

## 1. Mara

`Mara` is the pure LLM-based player.

Design:

- uses Grok directly
- does not select from a fixed menu of named classic strategies
- asks Grok to invent a fresh numeric control law for the current match from raw match features
- can replan mid-match if the current line is underperforming

Current implementation:

- class: `MaraStrategy`
- name: `mara`
- file: [`ipdlab/strategies.py`](../ipdlab/strategies.py)

Observed result:

- best prompt/model variant tested was `Mara:grok-4.20-beta-latest-non-reasoning:balanced`
- in the current field it is competitive, but not dominant
- in the validation run it landed around rank 9-10 depending on seed

Saved outputs:

- [`outputs/analysis/mara_benchmark.csv`](../outputs/analysis/mara_benchmark.csv)
- [`outputs/analysis/mara_seed_validation.csv`](../outputs/analysis/mara_seed_validation.csv)
- [`outputs/analysis/mara_head_to_head.csv`](../outputs/analysis/mara_head_to_head.csv)
- [`outputs/analysis/mara_seed_consistency.png`](../outputs/analysis/mara_seed_consistency.png)
- [`outputs/analysis/mara_head_to_head.png`](../outputs/analysis/mara_head_to_head.png)
- [`outputs/analysis/mara_match_distribution.png`](../outputs/analysis/mara_match_distribution.png)

## 2. Nadia

`Nadia` is the custom non-LLM strategy from this round.

Design:

- not built by selecting or stitching together named stock strategies at runtime
- uses its own internal state variables:
  trust, pressure, volatility, repair, grace
- updates those variables from match events
- acts using a tuned nonlinear control rule and a few hard gates

How it was tuned:

- local search over a parameterized family
- refinement against the real tournament objective
- objective balanced tournament score with some pressure toward stronger head-to-head margins

Current implementation:

- class: `NadiaStrategy`
- name: `nadia`
- file: [`ipdlab/strategies.py`](../ipdlab/strategies.py)

Observed result:

- `Nadia` is clearly stronger than a large part of the field
- but in the full validation run it did **not** dethrone the current best tournament winner
- it settled around rank 3 in repeated validation

Saved outputs:

- [`outputs/analysis/nadia_search.csv`](../outputs/analysis/nadia_search.csv)
- [`outputs/analysis/nadia_refine.csv`](../outputs/analysis/nadia_refine.csv)
- [`outputs/analysis/nadia_heavy_refine.csv`](../outputs/analysis/nadia_heavy_refine.csv)
- [`outputs/analysis/nadia_seed_validation.csv`](../outputs/analysis/nadia_seed_validation.csv)
- [`outputs/analysis/nadia_head_to_head.csv`](../outputs/analysis/nadia_head_to_head.csv)
- [`outputs/analysis/nadia_seed_consistency.png`](../outputs/analysis/nadia_seed_consistency.png)
- [`outputs/analysis/nadia_head_to_head.png`](../outputs/analysis/nadia_head_to_head.png)
- [`outputs/analysis/nadia_match_distribution.png`](../outputs/analysis/nadia_match_distribution.png)

## Bottom Line

Best current tournament winner in this repo:

- `Eleanor`

Best pure LLM player from this round:

- `Mara`

Best fully local custom-from-scratch player from this round:

- `Nadia`

Important honesty clause:

- `Mara` is the purest LLM experiment, but it is not the strongest overall strategy in the repo
- `Nadia` is the strongest custom-from-scratch controller from this round, but it still trails `Eleanor`
- `Eleanor` remains the strongest validated tournament winner in the current field
