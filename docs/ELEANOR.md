# Eleanor

`Eleanor` is a tournament-focused hybrid strategy for the iterated prisoner's dilemma.

It was designed inside this repo by starting from `Gradual Tit For Tat` and then adding two extra control rules:

- a majority-based lock into defection against opponents that trend clearly defection-heavy
- a one-round endgame defection

## Short Description

Eleanor is:

- cooperative by default
- retaliatory when exploited
- willing to escalate permanently against opponents that defect too often
- slightly endgame-aware

In the current field used in this repo, Eleanor consistently wins the tournament aggregate, but it is not pairwise unbeatable against every single opponent.

## Exact Behavior

The implementation is in [`ipdlab/strategies.py`](../ipdlab/strategies.py).

At a high level:

1. Start from `Gradual Tit For Tat`.
2. If the match is in the final round, defect.
3. Once at least `8` opponent moves have been observed:
   if opponent defections > opponent cooperations + `1`, lock into always defect.
4. Otherwise, keep following `Gradual Tit For Tat`.

## What That Means In Practice

`Gradual Tit For Tat` already does two useful things:

- it cooperates with cooperative opponents
- it punishes defections with increasing retaliation, then tries to return to cooperation

Eleanor keeps that core behavior, but adds a second layer:

- if the opponent is not just noisy, but genuinely trending defection-heavy, Eleanor stops trying to reconcile and defects permanently

That makes it stronger than plain `Gradual Tit For Tat` in a mixed field with unconditional defectors, probing strategies, periodic defect-heavy strategies, and some opportunistic entrants.

The final-round defection is a small endgame optimization. In a finite known-length match, the last move cannot be punished in the future, so keeping unconditional cooperation there is often leaving points on the table.

## Why It Performs Well Here

In this repo's current tournament field, the strongest strategies are mostly:

- cooperative enough to collect high mutual-payoff runs
- retaliatory enough to avoid being farmed by defect-heavy opponents

Eleanor fits that environment well because it:

- still earns near-maximum scores against nice reciprocators
- punishes exploiters harder than softer reciprocal strategies
- avoids getting dragged into too many long recovery attempts once an opponent is clearly bad-faith

## Is It Novel?

Honest answer: partially.

It is new in the narrow sense that:

- I created this exact combination here, in this repo
- I did not copy an existing published strategy named `Eleanor`
- I did not lift this implementation from a paper, library, or website

It is not novel in the strong research sense.

It is clearly based on known ideas from the iterated prisoner's dilemma literature:

- `Gradual Tit For Tat`
- majority-style counting of opponent cooperation vs defection
- finite-horizon endgame defection logic

So the right description is:

- **new hybrid for this project**
- **not a claim of academic novelty**

## Did I Use External Resources?

For `Eleanor` itself:

- no external strategy was copied directly
- no paper or codebase was used as the exact template

The inspiration came from strategies that were already present in this repo and from standard IPD ideas already discussed in the project:

- `Gradual Tit For Tat`
- majority-style strategies such as `soft_majo` / `hard_majo`
- finite-match endgame reasoning

Earlier in the project, I did use official/documented sources for other parts of the repo, especially when checking Axelrod-tournament reconstructions and xAI model names. But `Eleanor` specifically was produced by local hybridization and empirical tournament search in this codebase, not by copying a named external strategy.

## Validation Claim

The strongest validated claim I can make is:

- Eleanor ranked `#1` in the current tournament field across the tested repeated runs used in this repo

I cannot honestly claim:

- that it is universally best for all IPD settings
- that it is pairwise unbeatable against every opponent
- that it is an established literature strategy

## One-Line Summary

Eleanor is a `Gradual Tit For Tat`-based hybrid that cooperates first, escalates against defections, permanently hardens against clearly defect-heavy opponents, and defects in the final round.
