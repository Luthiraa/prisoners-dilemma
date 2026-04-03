from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import matplotlib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ipdlab.strategies import PayoffMatrix, Strategy, create_named_strategy
from scripts.tournament_analysis import build_field, style_axes


matplotlib.use("Agg")
import matplotlib.pyplot as plt


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


def evaluate(target_name: str, rounds: int, repetitions: int, seed_count: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    payoffs = PayoffMatrix()
    field = build_field()
    seed_rows: list[dict] = []
    head_rows: list[dict] = []
    match_rows: list[dict] = []

    for seed in range(seed_count):
        target = create_named_strategy(target_name)
        players = [target] + [player.clone() for player in field]
        unique_names: list[str] = []
        for player in players:
            if player.name() not in unique_names:
                unique_names.append(player.name())
        score_sum = {name: 0.0 for name in unique_names}
        match_count = {name: 0 for name in unique_names}
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
                    if player_a.name() == target.name() and player_b.name() != target.name():
                        head_rows.append({"seed": seed, "repetition": repetition, "opponent": player_b.name(), "target_avg": avg_a, "opponent_avg": avg_b, "margin": avg_a - avg_b})
                        match_rows.append({"seed": seed, "repetition": repetition, "opponent": player_b.name(), "target_avg": avg_a})
                    elif player_b.name() == target.name() and player_a.name() != target.name():
                        head_rows.append({"seed": seed, "repetition": repetition, "opponent": player_a.name(), "target_avg": avg_b, "opponent_avg": avg_a, "margin": avg_b - avg_a})
                        match_rows.append({"seed": seed, "repetition": repetition, "opponent": player_a.name(), "target_avg": avg_b})

        standings = sorted([(name, score_sum[name] / match_count[name]) for name in unique_names], key=lambda item: (-item[1], item[0]))
        target_display_name = target.name()
        target_avg = next(value for name, value in standings if name == target_display_name)
        target_rank = 1 + sum(1 for name, value in standings if value > target_avg)
        best_other_name, best_other_avg = next((name, value) for name, value in standings if name != target_display_name)
        seed_rows.append(
            {
                "seed": seed,
                "rank": target_rank,
                "average_score_per_turn": target_avg,
                "best_other": best_other_name,
                "best_other_average": best_other_avg,
                "gap_to_best_other": target_avg - best_other_avg,
            }
        )

    return pd.DataFrame(seed_rows), pd.DataFrame(head_rows), pd.DataFrame(match_rows)


def plot_seed_consistency(seed_df: pd.DataFrame, display_name: str, path: Path) -> None:
    fig, ax1 = plt.subplots(figsize=(13, 8))
    style_axes(ax1)
    ax1.plot(seed_df["seed"], seed_df["average_score_per_turn"], color="#ff7a18", linewidth=3, marker="o", markersize=8)
    ax1.set_xlabel("Tournament Seed")
    ax1.set_ylabel(f"{display_name} average score per turn")
    ax1.set_title(f"{display_name} Tournament Consistency", fontsize=20, weight="bold")
    for _, row in seed_df.iterrows():
        ax1.text(row["seed"], row["average_score_per_turn"] + 0.002, f"{row['average_score_per_turn']:.3f}", ha="center", fontsize=9, color="#000000")
    ax2 = ax1.twinx()
    ax2.plot(seed_df["seed"], seed_df["gap_to_best_other"], color="#44d7b6", linewidth=2.5, marker="s", markersize=6)
    ax2.set_ylabel("Gap to best other strategy", color="#000000")
    ax2.tick_params(colors="#000000")
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def plot_head_to_head(head_df: pd.DataFrame, display_name: str, path: Path) -> None:
    summary = head_df.groupby("opponent").agg(mean_margin=("margin", "mean")).reset_index().sort_values("mean_margin")
    fig, ax = plt.subplots(figsize=(15, max(12, len(summary) * 0.42)))
    colors = ["#2fbf71" if value >= 0 else "#d64550" for value in summary["mean_margin"]]
    ax.barh(summary["opponent"], summary["mean_margin"], color=colors, alpha=0.9)
    ax.axvline(0, color="#111111", linewidth=1.2)
    ax.set_xlabel(f"{display_name} mean head-to-head margin")
    ax.set_title(f"{display_name} vs Every Opponent", fontsize=20, weight="bold")
    ax.tick_params(axis="y", labelsize=10, colors="#000000")
    ax.tick_params(axis="x", colors="#000000")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(True, axis="x", alpha=0.18, linestyle="--")
    fig.subplots_adjust(left=0.28, right=0.97, top=0.95, bottom=0.05)
    fig.savefig(path, dpi=220)
    plt.close(fig)


def plot_match_distribution(match_df: pd.DataFrame, display_name: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(13, 8))
    bins = 24
    ax.hist(match_df["target_avg"], bins=bins, color="#3772ff", alpha=0.85, edgecolor="#ffffff", linewidth=0.7)
    ax.axvline(match_df["target_avg"].mean(), color="#ff006e", linewidth=3, label=f"Mean {match_df['target_avg'].mean():.3f}")
    ax.axvline(match_df["target_avg"].median(), color="#ffbe0b", linewidth=3, label=f"Median {match_df['target_avg'].median():.3f}")
    ax.set_title(f"{display_name} Match Score Distribution", fontsize=20, weight="bold")
    ax.set_xlabel("Per-match average score")
    ax.set_ylabel("Match count")
    ax.legend(frameon=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(True, axis="y", alpha=0.18, linestyle="--")
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", required=True)
    parser.add_argument("--rounds", type=int, default=200)
    parser.add_argument("--repetitions", type=int, default=20)
    parser.add_argument("--seed-count", type=int, default=10)
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    target = create_named_strategy(args.strategy)
    display_name = target.name()
    slug = args.strategy.lower()
    seed_df, head_df, match_df = evaluate(args.strategy, args.rounds, args.repetitions, args.seed_count)
    seed_df.to_csv(OUTPUT_DIR / f"{slug}_seed_validation.csv", index=False)
    head_df.to_csv(OUTPUT_DIR / f"{slug}_head_to_head.csv", index=False)
    match_df.to_csv(OUTPUT_DIR / f"{slug}_match_scores.csv", index=False)
    summary = {
        "strategy": display_name,
        "rounds": args.rounds,
        "repetitions": args.repetitions,
        "seed_count": args.seed_count,
        "rank_counts": seed_df["rank"].value_counts().sort_index().to_dict(),
        "mean_average_score_per_turn": float(seed_df["average_score_per_turn"].mean()),
        "min_gap_to_best_other": float(seed_df["gap_to_best_other"].min()),
        "negative_head_to_head_opponents": head_df.groupby("opponent")["margin"].mean().loc[lambda s: s < 0].sort_values().to_dict(),
    }
    (OUTPUT_DIR / f"{slug}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    plot_seed_consistency(seed_df, display_name, OUTPUT_DIR / f"{slug}_seed_consistency.png")
    plot_head_to_head(head_df, display_name, OUTPUT_DIR / f"{slug}_head_to_head.png")
    plot_match_distribution(match_df, display_name, OUTPUT_DIR / f"{slug}_match_distribution.png")
    print(seed_df.to_string(index=False))


if __name__ == "__main__":
    main()
