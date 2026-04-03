from __future__ import annotations

import json
import random
import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ipdlab.strategies import COOPERATE, DEFECT, MaraStrategy, NadiaStrategy, PayoffMatrix, Strategy
from scripts.tournament_analysis import build_field


OUTPUT_DIR = ROOT / "outputs" / "analysis"


def play_match(player_a: Strategy, player_b: Strategy, rounds: int, seed: int, payoffs: PayoffMatrix) -> tuple[float, float]:
    rng = random.Random(seed)
    player_a.reset()
    player_b.reset()
    history_a: list[str] = []
    history_b: list[str] = []
    score_a = 0.0
    score_b = 0.0
    for _ in range(rounds):
        move_a = player_a.move(history_a, history_b, rng, payoffs, rounds)
        move_b = player_b.move(history_b, history_a, rng, payoffs, rounds)
        round_score_a, round_score_b = payoffs.score(move_a, move_b)
        history_a.append(move_a)
        history_b.append(move_b)
        score_a += round_score_a
        score_b += round_score_b
    return score_a / rounds, score_b / rounds


def evaluate_candidate(candidate: Strategy, rounds: int, repetitions: int, seed: int, include_existing: bool = True) -> dict:
    payoffs = PayoffMatrix()
    field = build_field()
    players = [candidate] + [player.clone() for player in field]
    unique_names: list[str] = []
    for player in players:
        if player.name() not in unique_names:
            unique_names.append(player.name())
    score_sum = {name: 0.0 for name in unique_names}
    match_count = {name: 0 for name in unique_names}
    head_rows: list[dict] = []
    seed_rng = random.Random(seed)

    for repetition in range(repetitions):
        for i, player_a in enumerate(players):
            for j in range(i, len(players)):
                player_b = players[j]
                match_seed = seed_rng.randint(0, 2**31 - 1)
                avg_a, avg_b = play_match(player_a.clone(), player_b.clone(), rounds, match_seed, payoffs)
                score_sum[player_a.name()] += avg_a
                match_count[player_a.name()] += 1
                if i != j:
                    score_sum[player_b.name()] += avg_b
                    match_count[player_b.name()] += 1
                if player_a.name() == candidate.name() and player_b.name() != candidate.name():
                    head_rows.append({"opponent": player_b.name(), "margin": avg_a - avg_b, "candidate_avg": avg_a, "opponent_avg": avg_b})
                elif player_b.name() == candidate.name() and player_a.name() != candidate.name():
                    head_rows.append({"opponent": player_a.name(), "margin": avg_b - avg_a, "candidate_avg": avg_b, "opponent_avg": avg_a})

    standings = sorted([(name, score_sum[name] / match_count[name]) for name in unique_names], key=lambda item: (-item[1], item[0]))
    candidate_avg = next(value for name, value in standings if name == candidate.name())
    candidate_rank = 1 + sum(1 for name, value in standings if value > candidate_avg)
    best_other_name, best_other_avg = next((name, value) for name, value in standings if name != candidate.name())
    head_df = pd.DataFrame(head_rows)
    head_summary = head_df.groupby("opponent")["margin"].mean().sort_values()
    return {
        "name": candidate.name(),
        "rank": candidate_rank,
        "average_score_per_turn": candidate_avg,
        "gap_to_best_other": candidate_avg - best_other_avg,
        "best_other": best_other_name,
        "head_mean_margin": float(head_df["margin"].mean()),
        "head_min_margin": float(head_summary.min()),
        "head_negative_count": int((head_summary < 0).sum()),
        "top_5": standings[:5],
        "head_summary": head_summary,
    }


@dataclass
class NadiaGenome:
    trust_gain_c: float
    trust_loss_d: float
    betrayal_pressure: float
    deadlock_pressure: float
    mutual_relief: float
    volatility_gain: float
    volatility_decay: float
    repair_gain: float
    repair_decay: float
    grace_gain: float
    grace_loss: float
    endgame_rounds: int
    coop_streak_gate: int
    pressure_gate: float
    trust_gate: float
    bias: float
    trust_weight: float
    pressure_weight: float
    volatility_weight: float
    repair_weight: float
    grace_weight: float
    recent_coop_weight: float
    recent_defect_weight: float
    betrayal_weight: float
    score_gap_weight: float
    threshold: float


class NadiaGenomeStrategy(Strategy):
    strategy_name = "nadia_genome"

    def __init__(self, genome: NadiaGenome) -> None:
        self.genome = genome
        self.reset()

    def reset(self) -> None:
        self.trust = 0.4
        self.pressure = 0.0
        self.volatility = 0.0
        self.repair = 0.0
        self.grace = 0.8
        self.recorded_rounds = 0
        self.my_total = 0.0
        self.opp_total = 0.0

    def name(self) -> str:
        return "NadiaSearch"

    def _update(self, my_history, opponent_history, payoffs):
        while self.recorded_rounds < len(my_history):
            my_move = my_history[self.recorded_rounds]
            opp_move = opponent_history[self.recorded_rounds]
            my_score, opp_score = payoffs.score(my_move, opp_move)
            self.my_total += my_score
            self.opp_total += opp_score
            betrayal = my_move == COOPERATE and opp_move == DEFECT
            deadlock = my_move == DEFECT and opp_move == DEFECT
            mutual_coop = my_move == COOPERATE and opp_move == COOPERATE
            rescue = my_move == DEFECT and opp_move == COOPERATE
            if opp_move == COOPERATE:
                self.trust += self.genome.trust_gain_c
                self.grace += self.genome.grace_gain
            else:
                self.trust -= self.genome.trust_loss_d if betrayal else self.genome.trust_loss_d * 0.72
                self.grace -= self.genome.grace_loss
            if mutual_coop:
                self.trust += self.genome.mutual_relief * 0.65
                self.pressure -= self.genome.mutual_relief
            if betrayal:
                self.pressure += self.genome.betrayal_pressure
            elif deadlock:
                self.pressure += self.genome.deadlock_pressure
            else:
                self.pressure -= 0.18
            if self.recorded_rounds >= 1 and opponent_history[self.recorded_rounds] != opponent_history[self.recorded_rounds - 1]:
                self.volatility = self.volatility * self.genome.volatility_decay + self.genome.volatility_gain
            else:
                self.volatility *= self.genome.volatility_decay
            if rescue:
                self.repair = self.repair * self.genome.repair_decay + self.genome.repair_gain
            else:
                self.repair *= self.genome.repair_decay
            self.recorded_rounds += 1

    def move(self, my_history, opponent_history, rng, payoffs, match_length):
        self._update(my_history, opponent_history, payoffs)
        rounds_played = len(my_history)
        rounds_left = match_length - rounds_played
        if rounds_played == 0:
            return COOPERATE
        if rounds_left <= self.genome.endgame_rounds:
            return DEFECT
        mutual_streak = 0
        for my_move, opp_move in zip(reversed(my_history), reversed(opponent_history)):
            if my_move == COOPERATE and opp_move == COOPERATE:
                mutual_streak += 1
            else:
                break
        recent_opp = opponent_history[-8:] if len(opponent_history) >= 8 else opponent_history
        recent_opp_coop_rate = recent_opp.count(COOPERATE) / max(1, len(recent_opp))
        recent_opp_defect_rate = recent_opp.count(DEFECT) / max(1, len(recent_opp))
        betrayal_rate = sum(1 for my_move, opp_move in zip(my_history, opponent_history) if my_move == COOPERATE and opp_move == DEFECT) / max(1, rounds_played)
        score_gap = (self.my_total - self.opp_total) / max(1, rounds_played)

        if mutual_streak >= self.genome.coop_streak_gate and self.pressure < self.genome.pressure_gate * 0.6 and self.volatility < 1.0:
            return COOPERATE
        if self.pressure > self.genome.pressure_gate and self.trust < self.genome.trust_gate:
            return DEFECT

        cooperation_signal = (
            self.genome.bias
            + self.genome.trust_weight * self.trust
            - self.genome.pressure_weight * self.pressure
            - self.genome.volatility_weight * self.volatility
            + self.genome.repair_weight * self.repair
            + self.genome.grace_weight * self.grace
            + self.genome.recent_coop_weight * recent_opp_coop_rate
            - self.genome.recent_defect_weight * recent_opp_defect_rate
            - self.genome.betrayal_weight * betrayal_rate
            + self.genome.score_gap_weight * score_gap
        )
        return COOPERATE if cooperation_signal >= self.genome.threshold else DEFECT

    def clone(self):
        return NadiaGenomeStrategy(self.genome)


def random_genome(rng: random.Random) -> NadiaGenome:
    return NadiaGenome(
        trust_gain_c=rng.uniform(0.35, 0.90),
        trust_loss_d=rng.uniform(0.80, 1.80),
        betrayal_pressure=rng.uniform(0.90, 1.90),
        deadlock_pressure=rng.uniform(0.15, 0.70),
        mutual_relief=rng.uniform(0.20, 0.80),
        volatility_gain=rng.uniform(0.40, 1.10),
        volatility_decay=rng.uniform(0.45, 0.85),
        repair_gain=rng.uniform(0.40, 1.20),
        repair_decay=rng.uniform(0.35, 0.85),
        grace_gain=rng.uniform(0.05, 0.35),
        grace_loss=rng.uniform(0.20, 0.75),
        endgame_rounds=rng.randint(0, 2),
        coop_streak_gate=rng.randint(4, 9),
        pressure_gate=rng.uniform(1.7, 3.2),
        trust_gate=rng.uniform(-0.2, 0.8),
        bias=rng.uniform(-0.3, 0.9),
        trust_weight=rng.uniform(0.15, 0.55),
        pressure_weight=rng.uniform(0.45, 1.10),
        volatility_weight=rng.uniform(0.10, 0.50),
        repair_weight=rng.uniform(0.15, 0.70),
        grace_weight=rng.uniform(0.05, 0.40),
        recent_coop_weight=rng.uniform(0.10, 0.70),
        recent_defect_weight=rng.uniform(0.20, 0.95),
        betrayal_weight=rng.uniform(0.20, 0.95),
        score_gap_weight=rng.uniform(0.05, 0.35),
        threshold=rng.uniform(-0.10, 0.55),
    )


def search_nadia(iterations: int = 80, rounds: int = 200, repetitions: int = 5, seed: int = 19) -> pd.DataFrame:
    rng = random.Random(seed)
    rows = []
    for iteration in range(iterations):
        genome = random_genome(rng)
        candidate = NadiaGenomeStrategy(genome)
        result = evaluate_candidate(candidate, rounds=rounds, repetitions=repetitions, seed=seed + iteration)
        objective = result["average_score_per_turn"] + 0.12 * result["head_mean_margin"] + 0.08 * result["head_min_margin"]
        rows.append(
            {
                "iteration": iteration,
                "objective": objective,
                **{field: getattr(genome, field) for field in genome.__dataclass_fields__},
                "rank": result["rank"],
                "average_score_per_turn": result["average_score_per_turn"],
                "gap_to_best_other": result["gap_to_best_other"],
                "head_mean_margin": result["head_mean_margin"],
                "head_min_margin": result["head_min_margin"],
                "head_negative_count": result["head_negative_count"],
            }
        )
    return pd.DataFrame(rows).sort_values(["objective", "average_score_per_turn"], ascending=[False, False]).reset_index(drop=True)


def benchmark_mara(rounds: int = 200, repetitions: int = 5) -> pd.DataFrame:
    candidates = [
        MaraStrategy(model="grok-4.20-beta-latest-non-reasoning", style="balanced"),
        MaraStrategy(model="grok-4.20-beta-latest-non-reasoning", style="opportunistic"),
        MaraStrategy(model="grok-4.20-beta-latest-non-reasoning", style="fortress"),
    ]
    rows = []
    for index, candidate in enumerate(candidates):
        result = evaluate_candidate(candidate, rounds=rounds, repetitions=repetitions, seed=70 + index)
        rows.append({k: v for k, v in result.items() if k not in {"top_5", "head_summary"}})
    return pd.DataFrame(rows).sort_values(["rank", "average_score_per_turn"], ascending=[True, False]).reset_index(drop=True)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    nadia_search = search_nadia()
    nadia_search.to_csv(OUTPUT_DIR / "nadia_search.csv", index=False)
    mara_benchmark = benchmark_mara()
    mara_benchmark.to_csv(OUTPUT_DIR / "mara_benchmark.csv", index=False)
    payload = {
        "nadia_best": nadia_search.head(5).to_dict(orient="records"),
        "mara": mara_benchmark.to_dict(orient="records"),
    }
    (OUTPUT_DIR / "innovation_lab_summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("NADIA SEARCH")
    print(nadia_search.head(10).to_string(index=False))
    print("\nMARA BENCHMARK")
    print(mara_benchmark.to_string(index=False))


if __name__ == "__main__":
    main()
