from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Sequence

from .strategies import (
    AXELROD_FIRST_REPORTED_RANKS,
    PayoffMatrix,
    Strategy,
    create_axelrod_first_players,
    create_named_strategy,
)


@dataclass
class MatchResult:
    player_a: str
    player_b: str
    rounds: int
    score_a: float
    score_b: float
    history_a: List[str]
    history_b: List[str]


@dataclass
class TournamentStanding:
    rank: int
    name: str
    total_score: float
    average_score_per_turn: float
    matches_played: int
    cooperation_rate: float
    reported_rank: int | None = None


def play_match(player_a: Strategy, player_b: Strategy, rounds: int, seed: int, payoffs: PayoffMatrix) -> MatchResult:
    rng = random.Random(seed)
    player_a.reset()
    player_b.reset()
    history_a: List[str] = []
    history_b: List[str] = []
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
    return MatchResult(player_a.name(), player_b.name(), rounds, score_a, score_b, history_a, history_b)


def run_round_robin(players: Sequence[Strategy], rounds: int, repetitions: int, seed: int, payoffs: PayoffMatrix) -> List[TournamentStanding]:
    score_totals = {player.name(): 0.0 for player in players}
    cooperation_totals = {player.name(): 0 for player in players}
    turns_played = {player.name(): 0 for player in players}
    matches_played = {player.name(): 0 for player in players}
    master_rng = random.Random(seed)

    for repetition in range(repetitions):
        for left_index, left_player in enumerate(players):
            for right_index in range(left_index, len(players)):
                right_player = players[right_index]
                match_seed = master_rng.randint(0, 2**31 - 1)
                result = play_match(left_player.clone(), right_player.clone(), rounds, match_seed, payoffs)
                score_totals[result.player_a] += result.score_a
                cooperation_totals[result.player_a] += result.history_a.count("C")
                turns_played[result.player_a] += rounds
                matches_played[result.player_a] += 1
                if left_index != right_index:
                    score_totals[result.player_b] += result.score_b
                    cooperation_totals[result.player_b] += result.history_b.count("C")
                    turns_played[result.player_b] += rounds
                    matches_played[result.player_b] += 1

    standings = []
    for player in players:
        name = player.name()
        average_score = score_totals[name] / turns_played[name] if turns_played[name] else 0.0
        cooperation_rate = cooperation_totals[name] / turns_played[name] if turns_played[name] else 0.0
        reported_rank = None
        for index, reported_name in enumerate(AXELROD_FIRST_REPORTED_RANKS, start=1):
            if name.startswith(reported_name):
                reported_rank = index
                break
        standings.append(
            TournamentStanding(
                rank=0,
                name=name,
                total_score=score_totals[name],
                average_score_per_turn=average_score,
                matches_played=matches_played[name],
                cooperation_rate=cooperation_rate,
                reported_rank=reported_rank,
            )
        )
    standings.sort(key=lambda row: (-row.average_score_per_turn, -row.total_score, row.name))
    for index, row in enumerate(standings, start=1):
        row.rank = index
    return standings


def print_table(standings: Sequence[TournamentStanding]) -> None:
    headers = ["Rank", "Strategy", "Avg/Turn", "Total", "Coop%", "Reported"]
    rows = []
    for row in standings:
        rows.append(
            [
                str(row.rank),
                row.name,
                f"{row.average_score_per_turn:.4f}",
                f"{row.total_score:.1f}",
                f"{row.cooperation_rate * 100:.1f}",
                "-" if row.reported_rank is None else str(row.reported_rank),
            ]
        )
    widths = [max(len(headers[i]), *(len(r[i]) for r in rows)) for i in range(len(headers))]
    print("  ".join(header.ljust(widths[i]) for i, header in enumerate(headers)))
    print("  ".join("-" * widths[i] for i in range(len(headers))))
    for row in rows:
        print("  ".join(row[i].ljust(widths[i]) for i in range(len(headers))))


def write_output(path: Path, standings: Sequence[TournamentStanding], output_format: str) -> None:
    if output_format == "json":
        path.write_text(json.dumps([asdict(row) for row in standings], indent=2), encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(standings[0]).keys()))
        writer.writeheader()
        for row in standings:
            writer.writerow(asdict(row))


def print_csv(standings: Sequence[TournamentStanding]) -> None:
    writer = csv.DictWriter(sys.stdout, fieldnames=list(asdict(standings[0]).keys()))
    writer.writeheader()
    for row in standings:
        writer.writerow(asdict(row))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run canonical iterated prisoner's dilemma experiments.")
    parser.add_argument("--experiment", choices=["axelrod-first", "custom"], default="axelrod-first")
    parser.add_argument("--strategies", help="Comma-separated named strategies for --experiment custom.")
    parser.add_argument("--rounds", type=int, default=200, help="Rounds per match. Axelrod first tournament used 200.")
    parser.add_argument("--repetitions", type=int, default=5, help="Tournament repetitions. Use 5 for the original stochastic setup.")
    parser.add_argument("--seed", type=int, default=0, help="Base RNG seed for reproducible stochastic tournaments.")
    parser.add_argument("--output", type=Path, help="Optional output file path.")
    parser.add_argument("--format", choices=["table", "json", "csv"], default="table")
    return parser.parse_args()


def load_players(args: argparse.Namespace) -> List[Strategy]:
    if args.experiment == "axelrod-first":
        return create_axelrod_first_players()
    if not args.strategies:
        raise ValueError("--strategies is required for --experiment custom")
    return [create_named_strategy(name.strip()) for name in args.strategies.split(",") if name.strip()]


def main() -> None:
    args = parse_args()
    players = load_players(args)
    standings = run_round_robin(players, args.rounds, args.repetitions, args.seed, PayoffMatrix())
    if args.format == "table":
        print_table(standings)
    elif args.format == "json":
        print(json.dumps([asdict(row) for row in standings], indent=2))
    else:
        print_csv(standings)
    if args.output:
        output_format = "json" if args.output.suffix.lower() == ".json" else "csv"
        write_output(args.output, standings, output_format)


if __name__ == "__main__":
    main()
