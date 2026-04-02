from __future__ import annotations

import math
import random
import json
import os
from dataclasses import dataclass
from typing import Callable, Dict, List, Sequence
from urllib import error, request


COOPERATE = "C"
DEFECT = "D"
ABSTAIN = "A"


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def opposite(move: str) -> str:
    return DEFECT if move == COOPERATE else COOPERATE


def chi_square_p_value_binary(cooperations: int, defections: int) -> float:
    total = cooperations + defections
    if total == 0:
        return 1.0
    expected = total / 2
    chi_square = ((cooperations - expected) ** 2) / expected + ((defections - expected) ** 2) / expected
    return math.erfc(math.sqrt(chi_square / 2))


def load_xai_api_key(secret_path: str = ".secret") -> str | None:
    env_key = os.getenv("XAI_API_KEY")
    if env_key:
        return env_key.strip()
    try:
        raw = open(secret_path, "r", encoding="utf-8").read().strip()
    except OSError:
        return None
    for line in raw.splitlines():
        if line.startswith("XAI_API_KEY="):
            return line.split("=", 1)[1].strip()
    return None


def clean_classic_label(label: str) -> str:
    return label.replace("First by ", "")


@dataclass(frozen=True)
class PayoffMatrix:
    temptation: float = 5.0
    reward: float = 3.0
    punishment: float = 1.0
    sucker: float = 0.0
    abstain_payoff: float = 0.0

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


class Strategy:
    strategy_name = "strategy"
    stochastic = False

    def reset(self) -> None:
        pass

    def move(
        self,
        my_history: Sequence[str],
        opponent_history: Sequence[str],
        rng: random.Random,
        payoffs: PayoffMatrix,
        match_length: int,
    ) -> str:
        raise NotImplementedError

    def clone(self) -> "Strategy":
        raise NotImplementedError

    def name(self) -> str:
        return self.strategy_name


class UnconditionalCooperator(Strategy):
    strategy_name = "Cu"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        return COOPERATE

    def clone(self) -> Strategy:
        return UnconditionalCooperator()


class UnconditionalDefector(Strategy):
    strategy_name = "Du"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        return DEFECT

    def clone(self) -> Strategy:
        return UnconditionalDefector()


class RandomStrategy(Strategy):
    stochastic = True

    def __init__(self, p: float = 0.5, label: str | None = None) -> None:
        self.p = clamp01(p)
        self.label = label

    def name(self) -> str:
        return self.label or f"Random: {self.p:g}"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        return COOPERATE if rng.random() < self.p else DEFECT

    def clone(self) -> Strategy:
        return RandomStrategy(self.p, self.label)


class ProbabilityCooperator(RandomStrategy):
    def name(self) -> str:
        return f"Cp({self.p:g})"

    def clone(self) -> Strategy:
        return ProbabilityCooperator(self.p)


class TitForTat(Strategy):
    strategy_name = "TFT"

    def name(self) -> str:
        return "Tit For Tat"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        return COOPERATE if not opponent_history else opponent_history[-1]

    def clone(self) -> Strategy:
        return TitForTat()


class SuspiciousTitForTat(Strategy):
    strategy_name = "STFT"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        return DEFECT if not opponent_history else opponent_history[-1]

    def clone(self) -> Strategy:
        return SuspiciousTitForTat()


class GenerousTitForTat(Strategy):
    strategy_name = "GTFT"
    stochastic = True

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
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

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
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


class OrbitGuard(Strategy):
    strategy_name = "orbit_guard"

    def __init__(self, margin: int = 1, final_defect_rounds: int = 1, trigger_round: int = 8) -> None:
        self.margin = margin
        self.final_defect_rounds = final_defect_rounds
        self.trigger_round = trigger_round
        self.inner = GradualTitForTat()
        self.reset()

    def reset(self) -> None:
        self.inner.reset()
        self.lock_defect = False

    def name(self) -> str:
        return "OrbitGuard"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if match_length - len(my_history) <= self.final_defect_rounds:
            return DEFECT
        if len(opponent_history) >= self.trigger_round:
            if opponent_history.count(DEFECT) > opponent_history.count(COOPERATE) + self.margin:
                self.lock_defect = True
        if self.lock_defect:
            return DEFECT
        return self.inner.move(my_history, opponent_history, rng, payoffs, match_length)

    def clone(self) -> Strategy:
        return OrbitGuard(self.margin, self.final_defect_rounds, self.trigger_round)


class ImperfectTitForTat(Strategy):
    strategy_name = "ImpTFT"
    stochastic = True

    def __init__(self, accuracy: float = 0.9) -> None:
        self.accuracy = clamp01(accuracy)

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if not opponent_history:
            return COOPERATE
        return opponent_history[-1] if rng.random() < self.accuracy else opposite(opponent_history[-1])

    def clone(self) -> Strategy:
        return ImperfectTitForTat(self.accuracy)


class TitForTwoTats(Strategy):
    strategy_name = "TFTT"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        return DEFECT if len(opponent_history) >= 2 and list(opponent_history[-2:]) == [DEFECT, DEFECT] else COOPERATE

    def clone(self) -> Strategy:
        return TitForTwoTats()


class TwoTitsForTat(Strategy):
    strategy_name = "TTFT"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
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

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if not opponent_history:
            return COOPERATE
        if len(my_history) == 1:
            return opponent_history[-1]
        if self.deadlock_counter >= self.deadlock_threshold:
            if self.deadlock_counter == self.deadlock_threshold:
                self.deadlock_counter += 1
            else:
                self.deadlock_counter = 0
            return COOPERATE
        if opponent_history[-2:] == [COOPERATE, COOPERATE]:
            self.randomness_counter -= 1
        if opponent_history[-2] != opponent_history[-1]:
            self.randomness_counter += 1
        if my_history[-1] != opponent_history[-1]:
            self.randomness_counter += 1
        if self.randomness_counter >= self.randomness_threshold:
            return DEFECT
        if opponent_history[-2] != opponent_history[-1]:
            self.deadlock_counter += 1
        else:
            self.deadlock_counter = 0
        return opponent_history[-1]

    def clone(self) -> Strategy:
        return OmegaTitForTat(self.deadlock_threshold, self.randomness_threshold)


class GrimTrigger(Strategy):
    strategy_name = "GRIM"

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.grim = False

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if DEFECT in opponent_history:
            self.grim = True
        return DEFECT if self.grim else COOPERATE

    def clone(self) -> Strategy:
        return GrimTrigger()


class DiscriminatingAltruist(Strategy):
    strategy_name = "DA"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        return ABSTAIN if DEFECT in opponent_history else COOPERATE

    def clone(self) -> Strategy:
        return DiscriminatingAltruist()


class Pavlov(Strategy):
    strategy_name = "WSLS"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if not my_history:
            return COOPERATE
        return COOPERATE if my_history[-1] == opponent_history[-1] else DEFECT

    def clone(self) -> Strategy:
        return Pavlov()


class ReactiveStrategy(Strategy):
    stochastic = True

    def __init__(self, y: float, p: float, q: float) -> None:
        self.y = clamp01(y)
        self.p = clamp01(p)
        self.q = clamp01(q)

    def name(self) -> str:
        return f"R({self.y:g},{self.p:g},{self.q:g})"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        probability = self.y if not opponent_history else self.p if opponent_history[-1] == COOPERATE else self.q
        return COOPERATE if rng.random() < probability else DEFECT

    def clone(self) -> Strategy:
        return ReactiveStrategy(self.y, self.p, self.q)


class MemoryOneStrategy(Strategy):
    stochastic = True

    def __init__(self, p: float, q: float, r: float, s: float, label: str | None = None, initial: float = 1.0) -> None:
        self.p = clamp01(p)
        self.q = clamp01(q)
        self.r = clamp01(r)
        self.s = clamp01(s)
        self.label = label
        self.initial = clamp01(initial)

    def name(self) -> str:
        return self.label or f"S({self.p:g},{self.q:g},{self.r:g},{self.s:g})"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if not my_history:
            probability = self.initial
        else:
            probability = {
                "CC": self.p,
                "CD": self.q,
                "DC": self.r,
                "DD": self.s,
            }.get(my_history[-1] + opponent_history[-1], self.s)
        return COOPERATE if rng.random() < probability else DEFECT

    def clone(self) -> Strategy:
        return MemoryOneStrategy(self.p, self.q, self.r, self.s, self.label, self.initial)


class GoodStrategy(MemoryOneStrategy):
    def __init__(self) -> None:
        super().__init__(1.0, 0.0, 1.0, 0.0, label="GOOD", initial=1.0)


class Spiteful(GrimTrigger):
    strategy_name = "spiteful"

    def clone(self) -> Strategy:
        return Spiteful()


class SoftMajority(Strategy):
    strategy_name = "soft_majo"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        return COOPERATE if opponent_history.count(COOPERATE) >= opponent_history.count(DEFECT) else DEFECT

    def clone(self) -> Strategy:
        return SoftMajority()


class HardMajority(Strategy):
    strategy_name = "hard_majo"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if not opponent_history:
            return DEFECT
        return DEFECT if opponent_history.count(DEFECT) >= opponent_history.count(COOPERATE) else COOPERATE

    def clone(self) -> Strategy:
        return HardMajority()


class PeriodicStrategy(Strategy):
    def __init__(self, pattern: str, label: str) -> None:
        self.pattern = pattern
        self.label = label

    def name(self) -> str:
        return self.label

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        return self.pattern[len(my_history) % len(self.pattern)]

    def clone(self) -> Strategy:
        return PeriodicStrategy(self.pattern, self.label)


class Mistrust(SuspiciousTitForTat):
    strategy_name = "mistrust"

    def clone(self) -> Strategy:
        return Mistrust()


class HardTitForTat(Strategy):
    strategy_name = "hard_tft"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if len(opponent_history) < 2:
            return COOPERATE
        return DEFECT if DEFECT in opponent_history[-2:] else COOPERATE

    def clone(self) -> Strategy:
        return HardTitForTat()


class SlowTitForTat(Strategy):
    strategy_name = "slow_tft"

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.retaliating = False

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if len(opponent_history) < 2:
            return COOPERATE
        if self.retaliating:
            if list(opponent_history[-2:]) == [COOPERATE, COOPERATE]:
                self.retaliating = False
                return COOPERATE
            return DEFECT
        if list(opponent_history[-2:]) == [DEFECT, DEFECT]:
            self.retaliating = True
            return DEFECT
        return COOPERATE

    def clone(self) -> Strategy:
        return SlowTitForTat()


class Prober(Strategy):
    strategy_name = "prober"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        opening = [DEFECT, COOPERATE, COOPERATE]
        if len(my_history) < len(opening):
            return opening[len(my_history)]
        if list(opponent_history[1:3]) == [COOPERATE, COOPERATE]:
            return DEFECT
        return COOPERATE if opponent_history[-1] == COOPERATE else DEFECT

    def clone(self) -> Strategy:
        return Prober()


class MEM2(Strategy):
    strategy_name = "mem2"

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.play_as = "TFT"
        self.shift_counter = 3
        self.alld_counter = 0

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        self.shift_counter -= 1
        if self.shift_counter == 0 and self.alld_counter < 2:
            self.shift_counter = 2
            last_two = list(zip(my_history[-2:], opponent_history[-2:]))
            if last_two and set(last_two) == {(COOPERATE, COOPERATE)}:
                self.play_as = "TFT"
            elif set(last_two) == {(COOPERATE, DEFECT), (DEFECT, COOPERATE)}:
                self.play_as = "TFTT"
            else:
                self.play_as = "ALLD"
                self.alld_counter += 1
        if self.play_as == "ALLD":
            return DEFECT
        if self.play_as == "TFTT":
            return DEFECT if len(opponent_history) >= 2 and list(opponent_history[-2:]) == [DEFECT, DEFECT] else COOPERATE
        return COOPERATE if not opponent_history else opponent_history[-1]

    def clone(self) -> Strategy:
        return MEM2()


class GrokStrategy(Strategy):
    strategy_name = "grok"
    _policy_cache: Dict[tuple[str, str], str] = {}

    def __init__(self, model: str = "grok-3-mini", secret_path: str = ".secret", timeout_seconds: float = 20.0, replan_interval: int = 0) -> None:
        self.model = model
        self.secret_path = secret_path
        self.timeout_seconds = timeout_seconds
        self.replan_interval = replan_interval
        self.api_key = load_xai_api_key(secret_path)
        self.reset()

    def name(self) -> str:
        return f"grok:{self.model}"

    def reset(self) -> None:
        self.selected_policy = "tft"

    def _fallback_move(self, opponent_history: Sequence[str]) -> str:
        return COOPERATE if not opponent_history else opponent_history[-1]

    def _prompt(self, my_history: Sequence[str], opponent_history: Sequence[str], rounds_remaining: int, payoffs: PayoffMatrix) -> str:
        return (
            "You are selecting a strategy for an iterated prisoner's dilemma. "
            "Choose exactly one policy name from this set: TFT, GRIM, WSLS, TF2T, HARD_TFT, SOFT_MAJO, ALL_C, ALL_D.\n"
            f"Payoffs: T={payoffs.temptation}, R={payoffs.reward}, P={payoffs.punishment}, S={payoffs.sucker}.\n"
            f"My history: {''.join(my_history) or '-'}\n"
            f"Opponent history: {''.join(opponent_history) or '-'}\n"
            f"Rounds remaining after this move: {rounds_remaining}\n"
            "Goal: maximize long-run score in this match. Output only the policy name."
        )

    def _query_grok(self, prompt: str) -> str | None:
        if not self.api_key:
            return None
        cache_key = (self.model, prompt)
        if cache_key in self._policy_cache:
            return self._policy_cache[cache_key]
        payload = json.dumps(
            {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "Respond with exactly one policy name from the provided list."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0,
                "max_tokens": 8,
            }
        ).encode("utf-8")
        req = request.Request(
            "https://api.x.ai/v1/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
        except (error.URLError, TimeoutError, json.JSONDecodeError, OSError):
            return None
        try:
            content = body["choices"][0]["message"]["content"].strip().upper()
        except (KeyError, IndexError, AttributeError, TypeError):
            return None
        for policy in ["TFT", "GRIM", "WSLS", "TF2T", "HARD_TFT", "SOFT_MAJO", "ALL_C", "ALL_D"]:
            if policy in content:
                chosen = policy.lower()
                self._policy_cache[cache_key] = chosen
                return chosen
        return None

    def _policy_move(self, policy: str, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if policy == "all_c":
            return COOPERATE
        if policy == "all_d":
            return DEFECT
        if policy == "grim":
            return DEFECT if DEFECT in opponent_history else COOPERATE
        if policy == "wsls":
            return COOPERATE if not my_history or my_history[-1] == opponent_history[-1] else DEFECT
        if policy == "tf2t":
            return DEFECT if len(opponent_history) >= 2 and list(opponent_history[-2:]) == [DEFECT, DEFECT] else COOPERATE
        if policy == "hard_tft":
            return DEFECT if len(opponent_history) >= 2 and DEFECT in opponent_history[-2:] else COOPERATE
        if policy == "soft_majo":
            return COOPERATE if opponent_history.count(COOPERATE) >= opponent_history.count(DEFECT) else DEFECT
        return COOPERATE if not opponent_history else opponent_history[-1]

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        should_replan = not my_history or (self.replan_interval > 0 and len(my_history) % self.replan_interval == 0)
        if should_replan:
            prompt = self._prompt(my_history, opponent_history, match_length - len(my_history) - 1, payoffs)
            self.selected_policy = self._query_grok(prompt) or "tft"
        return self._policy_move(self.selected_policy, my_history, opponent_history, rng, payoffs, match_length)

    def clone(self) -> Strategy:
        return GrokStrategy(self.model, self.secret_path, self.timeout_seconds, self.replan_interval)


class FirstByDavis(Strategy):
    strategy_name = "Davis"

    def __init__(self, rounds_to_cooperate: int = 10) -> None:
        self.rounds_to_cooperate = rounds_to_cooperate

    def name(self) -> str:
        return f"Davis: {self.rounds_to_cooperate}"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if len(my_history) < self.rounds_to_cooperate:
            return COOPERATE
        return DEFECT if DEFECT in opponent_history else COOPERATE

    def clone(self) -> Strategy:
        return FirstByDavis(self.rounds_to_cooperate)


class FirstByDowning(Strategy):
    strategy_name = "Downing"

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.responses_to_c = 0
        self.responses_to_d = 0

    def name(self) -> str:
        return "Downing"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        round_number = len(my_history) + 1
        if round_number == 1:
            return DEFECT
        if round_number == 2:
            if opponent_history[-1] == COOPERATE:
                self.responses_to_c += 1
            return DEFECT
        if my_history[-2] == COOPERATE and opponent_history[-1] == COOPERATE:
            self.responses_to_c += 1
        if my_history[-2] == DEFECT and opponent_history[-1] == COOPERATE:
            self.responses_to_d += 1
        alpha = self.responses_to_c / (my_history.count(COOPERATE) + 1)
        beta = self.responses_to_d / max(my_history.count(DEFECT), 2)
        expected_c = alpha * payoffs.reward + (1 - alpha) * payoffs.sucker
        expected_d = beta * payoffs.temptation + (1 - beta) * payoffs.punishment
        if expected_c > expected_d:
            return COOPERATE
        if expected_c < expected_d:
            return DEFECT
        return opposite(my_history[-1])

    def clone(self) -> Strategy:
        return FirstByDowning()


class FirstByFeld(Strategy):
    strategy_name = "Feld"
    stochastic = True

    def __init__(self, start_coop_prob: float = 1.0, end_coop_prob: float = 0.5, rounds_of_decay: int = 200) -> None:
        self.start_coop_prob = start_coop_prob
        self.end_coop_prob = end_coop_prob
        self.rounds_of_decay = rounds_of_decay

    def name(self) -> str:
        return f"Feld: {self.start_coop_prob:.1f}, {self.end_coop_prob:.1f}, {self.rounds_of_decay}"

    def _cooperation_probability(self, rounds_played: int) -> float:
        diff = self.end_coop_prob - self.start_coop_prob
        slope = diff / self.rounds_of_decay
        return max(self.start_coop_prob + slope * rounds_played, self.end_coop_prob)

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if not opponent_history:
            return COOPERATE
        if opponent_history[-1] == DEFECT:
            return DEFECT
        p = self._cooperation_probability(len(my_history))
        return COOPERATE if rng.random() < p else DEFECT

    def clone(self) -> Strategy:
        return FirstByFeld(self.start_coop_prob, self.end_coop_prob, self.rounds_of_decay)


class FirstByGraaskamp(Strategy):
    strategy_name = "Graaskamp"
    stochastic = True

    def __init__(self, alpha: float = 0.05) -> None:
        self.alpha = alpha
        self.reset()

    def reset(self) -> None:
        self.opponent_is_random = False
        self.next_random_defection_turn: int | None = None

    def name(self) -> str:
        return f"Graaskamp: {self.alpha:.2f}"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if not my_history:
            return COOPERATE
        if len(my_history) < 56:
            if opponent_history[-1] == DEFECT or len(my_history) == 50:
                return DEFECT
            return COOPERATE
        p_value = chi_square_p_value_binary(opponent_history.count(COOPERATE), opponent_history.count(DEFECT))
        self.opponent_is_random = self.opponent_is_random or p_value >= self.alpha
        if self.opponent_is_random:
            return DEFECT
        behaves_like_tft = all(opponent_history[i] == my_history[i - 1] for i in range(1, len(my_history)))
        behaves_like_clone = list(opponent_history) == list(my_history)
        if behaves_like_tft or behaves_like_clone:
            return DEFECT if opponent_history[-1] == DEFECT else COOPERATE
        if self.next_random_defection_turn is None:
            self.next_random_defection_turn = rng.randint(5, 15) + len(my_history)
        if len(my_history) == self.next_random_defection_turn:
            self.next_random_defection_turn = rng.randint(5, 15) + len(my_history)
            return DEFECT
        return COOPERATE

    def clone(self) -> Strategy:
        return FirstByGraaskamp(self.alpha)


class FirstByGrofman(Strategy):
    strategy_name = "Grofman"
    stochastic = True

    def name(self) -> str:
        return "Grofman"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if not my_history or my_history[-1] == opponent_history[-1]:
            return COOPERATE
        return COOPERATE if rng.random() < (2 / 7) else DEFECT

    def clone(self) -> Strategy:
        return FirstByGrofman()


class FirstByJoss(MemoryOneStrategy):
    def __init__(self, p: float = 0.9) -> None:
        super().__init__(p, 0.0, p, 0.0)
        self.joss_p = p

    def name(self) -> str:
        return f"Joss: {self.joss_p:.1f}"

    def clone(self) -> Strategy:
        return FirstByJoss(self.joss_p)


class FirstByNydegger(Strategy):
    strategy_name = "Nydegger"

    def __init__(self) -> None:
        self.As = {1, 6, 7, 17, 22, 23, 26, 29, 30, 31, 33, 38, 39, 45, 49, 54, 55, 58, 61}
        self.score_map = {
            (COOPERATE, COOPERATE): 0,
            (COOPERATE, DEFECT): 2,
            (DEFECT, COOPERATE): 1,
            (DEFECT, DEFECT): 3,
        }

    def name(self) -> str:
        return "Nydegger"

    def score_history(self, my_history: Sequence[str], opponent_history: Sequence[str]) -> int:
        score = 0
        for index, weight in [(-1, 16), (-2, 4), (-3, 1)]:
            score += weight * self.score_map[(my_history[index], opponent_history[index])]
        return score

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if len(my_history) == 0:
            return COOPERATE
        if len(my_history) == 1:
            return DEFECT if opponent_history[-1] == DEFECT else COOPERATE
        if len(my_history) == 2:
            if list(opponent_history[0:2]) == [DEFECT, COOPERATE]:
                return DEFECT
            return DEFECT if opponent_history[-1] == DEFECT else COOPERATE
        return DEFECT if self.score_history(my_history[-3:], opponent_history[-3:]) in self.As else COOPERATE

    def clone(self) -> Strategy:
        return FirstByNydegger()


class FirstByShubik(Strategy):
    strategy_name = "Shubik"

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.is_retaliating = False
        self.retaliation_length = 0
        self.retaliation_remaining = 0

    def name(self) -> str:
        return "Shubik"

    def _decrease_retaliation_counter(self) -> None:
        if self.is_retaliating:
            self.retaliation_remaining -= 1
            if self.retaliation_remaining == 0:
                self.is_retaliating = False

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if not opponent_history:
            return COOPERATE
        if self.is_retaliating:
            self._decrease_retaliation_counter()
            return DEFECT
        if opponent_history[-1] == DEFECT and my_history[-1] == COOPERATE:
            self.is_retaliating = True
            self.retaliation_length += 1
            self.retaliation_remaining = self.retaliation_length
            self._decrease_retaliation_counter()
            return DEFECT
        return COOPERATE

    def clone(self) -> Strategy:
        return FirstByShubik()


class FirstByTullock(Strategy):
    strategy_name = "Tullock"
    stochastic = True

    def __init__(self) -> None:
        self.rounds_to_cooperate = 11

    def name(self) -> str:
        return "Tullock"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if len(my_history) < self.rounds_to_cooperate:
            return COOPERATE
        window = self.rounds_to_cooperate - 1
        prop_cooperate = opponent_history[-window:].count(COOPERATE) / window
        return COOPERATE if rng.random() < max(0.0, prop_cooperate - 0.10) else DEFECT

    def clone(self) -> Strategy:
        return FirstByTullock()


class FirstByAnonymous(Strategy):
    strategy_name = "Anonymous"
    stochastic = True

    def name(self) -> str:
        return "Anonymous"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        return COOPERATE if rng.random() < (rng.uniform(3, 7) / 10) else DEFECT

    def clone(self) -> Strategy:
        return FirstByAnonymous()


class FirstBySteinAndRapoport(Strategy):
    strategy_name = "Stein & Rapoport"

    def __init__(self, alpha: float = 0.05) -> None:
        self.alpha = alpha
        self.reset()

    def reset(self) -> None:
        self.opponent_is_random = False

    def name(self) -> str:
        return f"Stein & Rapoport: {self.alpha:.2f}"

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if match_length - len(my_history) <= 2:
            return DEFECT
        round_number = len(my_history) + 1
        if round_number < 5:
            return COOPERATE
        if round_number < 15:
            return opponent_history[-1]
        if round_number % 15 == 0:
            p_value = chi_square_p_value_binary(opponent_history.count(COOPERATE), opponent_history.count(DEFECT))
            self.opponent_is_random = p_value >= self.alpha
        return DEFECT if self.opponent_is_random else opponent_history[-1]

    def clone(self) -> Strategy:
        return FirstBySteinAndRapoport(self.alpha)


class FirstByTidemanAndChieruzzi(Strategy):
    strategy_name = "Tideman & Chieruzzi"

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.is_retaliating = False
        self.retaliation_length = 0
        self.retaliation_remaining = 0
        self.current_score = 0.0
        self.opponent_score = 0.0
        self.last_fresh_start = 0
        self.fresh_start = False
        self.remembered_number_of_opponent_defections = 0

    def name(self) -> str:
        return "Tideman & Chieruzzi"

    def _decrease_retaliation_counter(self) -> None:
        if self.is_retaliating:
            self.retaliation_remaining -= 1
            if self.retaliation_remaining == 0:
                self.is_retaliating = False

    def _fresh_start(self) -> None:
        self.is_retaliating = False
        self.retaliation_length = 0
        self.retaliation_remaining = 0
        self.remembered_number_of_opponent_defections = 0

    def _score_last_round(self, my_history: Sequence[str], opponent_history: Sequence[str], payoffs: PayoffMatrix) -> None:
        my_score, opponent_score = payoffs.score(my_history[-1], opponent_history[-1])
        self.current_score += my_score
        self.opponent_score += opponent_score

    def move(self, my_history: Sequence[str], opponent_history: Sequence[str], rng: random.Random, payoffs: PayoffMatrix, match_length: int) -> str:
        if match_length - len(my_history) <= 2:
            return DEFECT
        if not opponent_history:
            return COOPERATE
        if opponent_history[-1] == DEFECT:
            self.remembered_number_of_opponent_defections += 1
        self._score_last_round(my_history, opponent_history, payoffs)
        if self.fresh_start:
            self.fresh_start = False
            return COOPERATE
        current_round = len(my_history) + 1
        valid_fresh_start = self.last_fresh_start == 0 or current_round - self.last_fresh_start >= 20
        if valid_fresh_start:
            valid_points = self.current_score - self.opponent_score >= 10
            valid_rounds = match_length - current_round >= 10
            opponent_is_cooperating = opponent_history[-1] == COOPERATE
            if valid_points and valid_rounds and opponent_is_cooperating:
                total = opponent_history.count(COOPERATE) + opponent_history.count(DEFECT)
                std_deviation = math.sqrt(total) / 2 if total else 0.0
                lower = total / 2 - 3 * std_deviation
                upper = total / 2 + 3 * std_deviation
                if self.remembered_number_of_opponent_defections <= lower or self.remembered_number_of_opponent_defections >= upper:
                    self.last_fresh_start = current_round
                    self._fresh_start()
                    self.fresh_start = True
                    return COOPERATE
        if self.is_retaliating:
            self._decrease_retaliation_counter()
            return DEFECT
        if opponent_history[-1] == DEFECT:
            self.is_retaliating = True
            self.retaliation_length += 1
            self.retaliation_remaining = self.retaliation_length
            self._decrease_retaliation_counter()
            return DEFECT
        return COOPERATE

    def clone(self) -> Strategy:
        return FirstByTidemanAndChieruzzi()


NamedFactory = Callable[[], Strategy]


NAMED_STRATEGIES: Dict[str, NamedFactory] = {
    "all_c": UnconditionalCooperator,
    "cu": UnconditionalCooperator,
    "all_d": UnconditionalDefector,
    "du": UnconditionalDefector,
    "random": RandomStrategy,
    "tit_for_tat": TitForTat,
    "tft": TitForTat,
    "mistrust": Mistrust,
    "suspicious_tft": SuspiciousTitForTat,
    "spiteful": Spiteful,
    "grim": GrimTrigger,
    "soft_majo": SoftMajority,
    "hard_majo": HardMajority,
    "per_cd": lambda: PeriodicStrategy("CD", "per_cd"),
    "per_ccd": lambda: PeriodicStrategy("CCD", "per_ccd"),
    "per_ddc": lambda: PeriodicStrategy("DDC", "per_ddc"),
    "pavlov": Pavlov,
    "wsls": Pavlov,
    "tf2t": TitForTwoTats,
    "tftt": TitForTwoTats,
    "hard_tft": HardTitForTat,
    "slow_tft": SlowTitForTat,
    "gradual": GradualTitForTat,
    "grdtft": GradualTitForTat,
    "orbit_guard": OrbitGuard,
    "orbitguard": OrbitGuard,
    "prober": Prober,
    "mem2": MEM2,
    "grok": GrokStrategy,
}


AXELROD_FIRST_TOURNAMENT: List[NamedFactory] = [
    TitForTat,
    FirstByTidemanAndChieruzzi,
    FirstByNydegger,
    FirstByGrofman,
    FirstByShubik,
    FirstBySteinAndRapoport,
    GrimTrigger,
    FirstByDavis,
    FirstByGraaskamp,
    FirstByDowning,
    FirstByFeld,
    FirstByJoss,
    FirstByTullock,
    FirstByAnonymous,
    RandomStrategy,
]


AXELROD_FIRST_REPORTED_RANKS = [
    "Tit For Tat",
    "Tideman & Chieruzzi",
    "Nydegger",
    "Grofman",
    "Shubik",
    "Stein & Rapoport",
    "GRIM",
    "Davis",
    "Graaskamp",
    "Downing",
    "Feld",
    "Joss",
    "Tullock",
    "Anonymous",
    "Random",
]


def create_named_strategy(name: str) -> Strategy:
    key = name.strip().lower()
    try:
        return NAMED_STRATEGIES[key]()
    except KeyError as exc:
        raise ValueError(f"Unknown named strategy: {name}") from exc


def create_axelrod_first_players() -> List[Strategy]:
    return [factory() for factory in AXELROD_FIRST_TOURNAMENT]
