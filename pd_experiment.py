from __future__ import annotations

import argparse
import csv
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


COOPERATE = "C"
DEFECT = "D"
ABSTAIN = "A"
VALID_MOVES = {COOPERATE, DEFECT, ABSTAIN}


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def parse_float_list(text: str) -> List[float]:
    return [float(part.strip()) for part in text.split(",") if part.strip()]


def parse_strategy_list(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    if ";" in text:
        return [part.strip() for part in text.split(";") if part.strip()]
    return [part.strip() for part in text.split("|") if part.strip()]


def move_to_feature(move: str) -> tuple[float, float]:
    if move == COOPERATE:
        return 1.0, 0.0
    if move == DEFECT:
        return 0.0, 1.0
    return 0.0, 0.0


@dataclass(frozen=True)
class StrategyCatalogEntry:
    name: str
    abbreviation: str
    description: str
    implementation: str


CATALOG: List[StrategyCatalogEntry] = [
    StrategyCatalogEntry("Unconditional Cooperator", "Cu", "Cooperates unconditionally.", "exact"),
    StrategyCatalogEntry("Unconditional Defector", "Du", "Defects unconditionally.", "exact"),
    StrategyCatalogEntry("Random", "Random", "Cooperates with probability one-half.", "exact"),
    StrategyCatalogEntry("Probability p Cooperator", "Cp", "Cooperates with fixed probability p.", "exact"),
    StrategyCatalogEntry("Tit for Tat", "TFT", "Cooperates first, then copies opponent's previous move.", "exact"),
    StrategyCatalogEntry("Suspicious Tit for Tat", "STFT", "Defects first, then copies opponent's previous move.", "exact"),
    StrategyCatalogEntry("Generous Tit for Tat", "GTFT", "TFT with probabilistic forgiveness after defections.", "exact"),
    StrategyCatalogEntry("Gradual Tit for Tat", "GrdTFT", "Punishes defections with growing retaliation and two-round calming.", "source-backed"),
    StrategyCatalogEntry("Imperfect TFT", "ImpTFT", "Copies opponent with high but imperfect accuracy.", "exact"),
    StrategyCatalogEntry("Tit for Two Tats", "TFTT", "Defects only after two consecutive defections.", "exact"),
    StrategyCatalogEntry("Two Tits for Tat", "TTFT", "Defects twice after a single defection.", "exact"),
    StrategyCatalogEntry("Omega Tit for Tat", "OmegaTFT", "Noise-tolerant TFT with deadlock and randomness checks.", "source-backed"),
    StrategyCatalogEntry("GRIM", "GRIM", "Cooperates until a single opponent defection, then defects forever.", "exact"),
    StrategyCatalogEntry("Discriminating Altruist", "DA", "Optional-IPD strategy that abstains after an opponent defected.", "exact"),
    StrategyCatalogEntry("Pavlov", "WSLS", "Win-stay lose-shift.", "exact"),
    StrategyCatalogEntry("n-Pavlov", "Pn", "Adjusts cooperation probability based on prior payoff by 1/n or 2/n.", "exact"),
    StrategyCatalogEntry("Adaptive Pavlov", "APavlov", "Category-based strategy following Li's tournament description.", "source-backed"),
    StrategyCatalogEntry("Reactive", "R(y,p,q)", "First-round probability y, then p after C and q after D.", "exact"),
    StrategyCatalogEntry("Memory-one", "S(p,q,r,s)", "Probabilities after CC, CD, DC, DD.", "exact"),
    StrategyCatalogEntry("Zero Determinant", "ZD", "Generic memory-one four-vector or linear-relation form.", "research-friendly"),
    StrategyCatalogEntry("Equalizer", "SET-n", "Equalizer family with explicit long-run target and optional phi.", "research-friendly"),
    StrategyCatalogEntry("Extortionary", "Extort-n", "Extortion family with explicit factor and optional phi.", "research-friendly"),
    StrategyCatalogEntry("Generous", "Gen-n", "Generous family with explicit factor and optional phi.", "research-friendly"),
    StrategyCatalogEntry("Good", "GOOD", "Akin-style good strategy represented as a memory-one vector.", "research-friendly"),
    StrategyCatalogEntry("Lookup tables", "LookerUp", "General lookup-table strategy with opening and history depths.", "source-backed"),
    StrategyCatalogEntry("Neural Net", "ANN", "Single-hidden-layer network using the Axelrod ANN feature set.", "source-backed"),
    StrategyCatalogEntry("Finite State Machine", "FSM", "Deterministic state machine parameterized by states and transitions.", "research-friendly"),
]


@dataclass(frozen=True)
class PayoffMatrix:
    temptation: float = 5.0
    reward: float = 3.0
    punishment: float = 1.0
    sucker: float = 0.0
    abstain_payoff: float = 0.0

    def __post_init__(self) -> None:
        if not (self.temptation > self.reward > self.punishment > self.sucker):
            raise ValueError("Payoffs must satisfy T > R > P > S.")
        if not (2 * self.reward > self.temptation + self.sucker):
            raise ValueError("Payoffs must satisfy 2R > T + S.")

    def score(self, move_a: str, move_b: str) -> tuple[float, float]:
        if move_a == ABSTAIN or move_b == ABSTAIN:
            return self.abstain_payoff, self.abstain_payoff
        if move_a == COOPERATE and move_b == COOPERATE:
            return self.reward, self.reward
        if move_a == COOPERATE and move_b == DEFECT:
            return self.sucker, self.temptation
        if move_a == DEFECT and move_b == COOPERATE:
            return self.temptation, self.sucker
        return self.punishment, self.punishment


@dataclass
class MatchResult:
    player_a: str
    player_b: str
    rounds: int
    score_a: float
    score_b: float
    history_a: List[str]
    history_b: List[str]

    @property
    def cooperation_rate_a(self) -> float:
        return self.history_a.count(COOPERATE) / self.rounds if self.rounds else 0.0

    @property
    def cooperation_rate_b(self) -> float:
        return self.history_b.count(COOPERATE) / self.rounds if self.rounds else 0.0


class Strategy:
    strategy_name = "strategy"

    def reset(self) -> None:
        pass

    def move(
        self,
        my_history: Sequence[str],
        opponent_history: Sequence[str],
        rng: random.Random,
        payoffs: PayoffMatrix,
    ) -> str:
        raise NotImplementedError

    def clone(self) -> "Strategy":
        raise NotImplementedError

    def name(self) -> str:
        return self.strategy_name


class UnconditionalCooperator(Strategy):
    strategy_name = "Cu"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        return COOPERATE

    def clone(self) -> Strategy:
        return UnconditionalCooperator()


class UnconditionalDefector(Strategy):
    strategy_name = "Du"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        return DEFECT

    def clone(self) -> Strategy:
        return UnconditionalDefector()


class ProbabilityCooperator(Strategy):
    def __init__(self, p: float) -> None:
        self.p = clamp01(p)

    def name(self) -> str:
        return f"Cp({self.p:g})"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        return COOPERATE if rng.random() < self.p else DEFECT

    def clone(self) -> Strategy:
        return ProbabilityCooperator(self.p)


class TitForTat(Strategy):
    strategy_name = "TFT"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        return COOPERATE if not opponent_history else opponent_history[-1]

    def clone(self) -> Strategy:
        return TitForTat()


class SuspiciousTitForTat(Strategy):
    strategy_name = "STFT"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        return DEFECT if not opponent_history else opponent_history[-1]

    def clone(self) -> Strategy:
        return SuspiciousTitForTat()


class GenerousTitForTat(Strategy):
    strategy_name = "GTFT"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        if not opponent_history or opponent_history[-1] == COOPERATE:
            return COOPERATE
        g = min(
            1 - (payoffs.temptation - payoffs.reward) / (payoffs.reward - payoffs.sucker),
            (payoffs.reward - payoffs.punishment) / (payoffs.temptation - payoffs.punishment),
        )
        return COOPERATE if rng.random() < clamp01(g) else DEFECT

    def clone(self) -> Strategy:
        return GenerousTitForTat()


class GradualTitForTat(Strategy):
    strategy_name = "GrdTFT"

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.punishing = False
        self.calming = False
        self.punishment_limit = 0
        self.punishment_remaining = 0
        self.calming_remaining = 0

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        if self.punishing:
            self.punishment_remaining -= 1
            if self.punishment_remaining <= 0:
                self.punishing = False
                self.calming = True
                self.calming_remaining = 2
            return DEFECT
        if self.calming:
            self.calming_remaining -= 1
            if self.calming_remaining <= 0:
                self.calming = False
            return COOPERATE
        if opponent_history and opponent_history[-1] == DEFECT:
            self.punishment_limit += 1
            self.punishing = True
            self.punishment_remaining = self.punishment_limit - 1
            if self.punishment_remaining <= 0:
                self.punishing = False
                self.calming = True
                self.calming_remaining = 2
            return DEFECT
        return COOPERATE

    def clone(self) -> Strategy:
        return GradualTitForTat()


class ImperfectTitForTat(Strategy):
    strategy_name = "ImpTFT"

    def __init__(self, accuracy: float = 0.9) -> None:
        self.accuracy = clamp01(accuracy)

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        if not opponent_history:
            return COOPERATE
        imitate = rng.random() < self.accuracy
        if imitate:
            return opponent_history[-1]
        return DEFECT if opponent_history[-1] == COOPERATE else COOPERATE

    def clone(self) -> Strategy:
        return ImperfectTitForTat(self.accuracy)


class TitForTwoTats(Strategy):
    strategy_name = "TFTT"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        return DEFECT if len(opponent_history) >= 2 and opponent_history[-2:] == [DEFECT, DEFECT] else COOPERATE

    def clone(self) -> Strategy:
        return TitForTwoTats()


class TwoTitsForTat(Strategy):
    strategy_name = "TTFT"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        return DEFECT if DEFECT in opponent_history[-2:] else COOPERATE

    def clone(self) -> Strategy:
        return TwoTitsForTat()


class OmegaTitForTat(Strategy):
    strategy_name = "OmegaTFT"

    def __init__(self, deadlock_threshold: int = 3, randomness_threshold: int = 8) -> None:
        self.deadlock_threshold = deadlock_threshold
        self.randomness_threshold = randomness_threshold
        self.reset()

    def reset(self) -> None:
        self.deadlock_counter = 0
        self.randomness_counter = 0

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        if not opponent_history:
            return COOPERATE
        if len(my_history) >= 2 and len(opponent_history) >= 2:
            if my_history[-1] != opponent_history[-1] and my_history[-2] != opponent_history[-2]:
                self.deadlock_counter += 1
            else:
                self.deadlock_counter = 0
        if self.deadlock_counter >= self.deadlock_threshold:
            self.deadlock_counter = 0
            return COOPERATE
        if len(opponent_history) >= 8:
            recent = opponent_history[-8:]
            flips = sum(1 for i in range(1, len(recent)) if recent[i] != recent[i - 1])
            coop = recent.count(COOPERATE)
            if flips >= 6 and 2 <= coop <= 6:
                self.randomness_counter += 1
            else:
                self.randomness_counter = max(0, self.randomness_counter - 1)
        if self.randomness_counter >= self.randomness_threshold:
            return DEFECT
        return opponent_history[-1]

    def clone(self) -> Strategy:
        return OmegaTitForTat(self.deadlock_threshold, self.randomness_threshold)


class GrimTrigger(Strategy):
    strategy_name = "GRIM"

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.grim = False

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        if DEFECT in opponent_history:
            self.grim = True
        return DEFECT if self.grim else COOPERATE

    def clone(self) -> Strategy:
        return GrimTrigger()


class DiscriminatingAltruist(Strategy):
    strategy_name = "DA"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        return ABSTAIN if DEFECT in opponent_history else COOPERATE

    def clone(self) -> Strategy:
        return DiscriminatingAltruist()


class Pavlov(Strategy):
    strategy_name = "WSLS"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        if not my_history:
            return COOPERATE
        return COOPERATE if my_history[-1] == opponent_history[-1] else DEFECT

    def clone(self) -> Strategy:
        return Pavlov()


class NPavlov(Strategy):
    def __init__(self, n: int) -> None:
        self.n = max(1, n)
        self.reset()

    def reset(self) -> None:
        self.p = 1.0

    def name(self) -> str:
        return f"P{self.n}"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        if not my_history:
            self.p = 1.0
            return COOPERATE
        my_score, _ = payoffs.score(my_history[-1], opponent_history[-1])
        if math.isclose(my_score, payoffs.reward):
            self.p = min(1.0, self.p + 1 / self.n)
        elif math.isclose(my_score, payoffs.punishment):
            self.p = max(0.0, self.p - 1 / self.n)
        elif math.isclose(my_score, payoffs.temptation):
            self.p = min(1.0, self.p + 2 / self.n)
        else:
            self.p = max(0.0, self.p - 2 / self.n)
        return COOPERATE if rng.random() < self.p else DEFECT

    def clone(self) -> Strategy:
        return NPavlov(self.n)


class AdaptivePavlov(Strategy):
    strategy_name = "APavlov"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        if len(my_history) < 6:
            return COOPERATE if not opponent_history else opponent_history[-1]
        opponent_actions = [m for m in opponent_history if m in {COOPERATE, DEFECT}]
        if not opponent_actions:
            return COOPERATE
        cooperation_rate = opponent_actions.count(COOPERATE) / len(opponent_actions)
        alternations = sum(1 for i in range(1, len(opponent_actions)) if opponent_actions[i] != opponent_actions[i - 1])
        if cooperation_rate == 1.0:
            return DEFECT
        if cooperation_rate == 0.0:
            return DEFECT
        if alternations <= 2:
            return COOPERATE if my_history[-1] == opponent_history[-1] else DEFECT
        if 0.35 < cooperation_rate < 0.65:
            return DEFECT
        return COOPERATE if my_history[-1] == opponent_history[-1] else (COOPERATE if rng.random() < 0.25 else DEFECT)

    def clone(self) -> Strategy:
        return AdaptivePavlov()


class ReactiveStrategy(Strategy):
    def __init__(self, y: float, p: float, q: float) -> None:
        self.y = clamp01(y)
        self.p = clamp01(p)
        self.q = clamp01(q)

    def name(self) -> str:
        return f"R({self.y:g},{self.p:g},{self.q:g})"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        probability = self.y if not opponent_history else self.p if opponent_history[-1] == COOPERATE else self.q
        return COOPERATE if rng.random() < probability else DEFECT

    def clone(self) -> Strategy:
        return ReactiveStrategy(self.y, self.p, self.q)


class MemoryOneStrategy(Strategy):
    def __init__(self, p: float, q: float, r: float, s: float, label: str | None = None, initial: float = 1.0) -> None:
        self.p = clamp01(p)
        self.q = clamp01(q)
        self.r = clamp01(r)
        self.s = clamp01(s)
        self.label = label
        self.initial = clamp01(initial)

    def name(self) -> str:
        return self.label or f"S({self.p:g},{self.q:g},{self.r:g},{self.s:g})"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix) -> str:
        if not my_history:
            probability = self.initial
        else:
            key = my_history[-1] + opponent_history[-1]
            probability = {"CC": self.p, "CD": self.q, "DC": self.r, "DD": self.s}.get(key, self.s)
        return COOPERATE if rng.random() < probability else DEFECT

    def clone(self) -> Strategy:
        return MemoryOneStrategy(self.p, self.q, self.r, self.s, self.label, self.initial)


class LinearRelationZD(MemoryOneStrategy):
    def __init__(self, phi: float, s: float, l: float, payoffs: PayoffMatrix, label: str) -> None:
        r = payoffs.reward
        p = payoffs.punishment
        t = payoffs.temptation
        u = payoffs.sucker
        p1 = 1 - phi * (1 - s) * (r - l)
        p2 = 1 - phi * (s * (l - u) + (t - l))
        p3 = phi * ((l - u) + s * (t - l))
        p4 = phi * (1 - s) * (l - p)
        super().__init__(p1, p2, p3, p4, label=label, initial=1.0)


class GoodStrategy(MemoryOneStrategy):
    def __init__(self, p: float = 1.0, q: float = 0.0, r: float = 1.0, s: float = 0.0) -> None:
        super().__init__(p, q, r, s, label="GOOD", initial=1.0)
