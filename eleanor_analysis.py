from __future__ import annotations

import json
import random
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

from strategies import PayoffMatrix, Strategy, create_named_strategy
from tournament_analysis import build_field, style_axes


matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT_DIR = Path("analysis_output")
ROUNDS = 200
REPETITIONS = 20
SEEDS = list(range(10))


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


def evaluate_eleanor(seeds: list[int], repetitions: int, rounds: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    payoffs = PayoffMatrix()
    field = build_field()
    seed_rows: list[dict] = []
    head_to_head_rows: list[dict] = []
    match_rows: list[dict] = []

    for seed in seeds:
        eleanor = create_named_strategy("eleanor")
        players = [eleanor] + [player.clone() for player in field]
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
                    if player_a.name() == "Eleanor" and player_b.name() != "Eleanor":
                        head_to_head_rows.append(
                            {
                                "seed": seed,
                                "repetition": repetition,
                                "opponent": player_b.name(),
                                "eleanor_avg": avg_a,
                                "opponent_avg": avg_b,
                                "margin": avg_a - avg_b,
                            }
                        )
                        match_rows.append(
                            {
                                "seed": seed,
                                "repetition": repetition,
                                "opponent": player_b.name(),
                                "eleanor_avg": avg_a,
                            }
                        )
                    elif player_b.name() == "Eleanor" and player_a.name() != "Eleanor":
                        head_to_head_rows.append(
                            {
                                "seed": seed,
                                "repetition": repetition,
                                "opponent": player_a.name(),
                                "eleanor_avg": avg_b,
                                "opponent_avg": avg_a,
                                "margin": avg_b - avg_a,
                            }
                        )
                        match_rows.append(
                            {
                                "seed": seed,
                                "repetition": repetition,
                                "opponent": player_a.name(),
                                "eleanor_avg": avg_b,
                            }
                        )

        standings = sorted(
            [(name, score_sum[name] / match_count[name]) for name in unique_names],
            key=lambda item: (-item[1], item[0]),
        )
        eleanor_avg = next(value for name, value in standings if name == "Eleanor")
        best_other_name, best_other_avg = next((name, value) for name, value in standings if name != "Eleanor")
        eleanor_rank = 1 + sum(1 for name, value in standings if value > eleanor_avg)
        seed_rows.append(
            {
                "seed": seed,
                "rank": eleanor_rank,
                "average_score_per_turn": eleanor_avg,
                "best_other": best_other_name,
                "best_other_average": best_other_avg,
                "gap_to_best_other": eleanor_avg - best_other_avg,
            }
        )

    return pd.DataFrame(seed_rows), pd.DataFrame(head_to_head_rows), pd.DataFrame(match_rows)


def plot_seed_consistency(seed_df: pd.DataFrame, path: Path) -> None:
    fig, ax1 = plt.subplots(figsize=(13, 8))
    style_axes(ax1)
    ax1.plot(seed_df["seed"], seed_df["average_score_per_turn"], color="#ff7a18", linewidth=3, marker="o", markersize=8)
    ax1.set_xlabel("Tournament Seed")
    ax1.set_ylabel("Eleanor average score per turn")
    ax1.set_title("Eleanor Tournament Consistency", fontsize=20, weight="bold")
    for _, row in seed_df.iterrows():
        ax1.text(row["seed"], row["average_score_per_turn"] + 0.002, f"{row['average_score_per_turn']:.3f}", ha="center", fontsize=9, color="#000000")
    ax2 = ax1.twinx()
    ax2.plot(seed_df["seed"], seed_df["gap_to_best_other"], color="#44d7b6", linewidth=2.5, marker="s", markersize=6)
    ax2.set_ylabel("Gap to best other strategy", color="#000000")
    ax2.tick_params(colors="#000000")
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def plot_head_to_head(head_df: pd.DataFrame, path: Path) -> None:
    summary = (
        head_df.groupby("opponent")
        .agg(mean_margin=("margin", "mean"), median_margin=("margin", "median"))
        .reset_index()
        .sort_values("mean_margin")
    )
    fig, ax = plt.subplots(figsize=(15, max(12, len(summary) * 0.42)))
    colors = np.where(summary["mean_margin"] >= 0, "#2fbf71", "#d64550")
    ax.barh(summary["opponent"], summary["mean_margin"], color=colors, alpha=0.9)
    ax.axvline(0, color="#111111", linewidth=1.2)
    ax.set_xlabel("Eleanor mean head-to-head margin")
    ax.set_title("Eleanor vs Every Opponent", fontsize=20, weight="bold")
    ax.tick_params(axis="y", labelsize=10, colors="#000000")
    ax.tick_params(axis="x", colors="#000000")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(True, axis="x", alpha=0.18, linestyle="--")
    fig.subplots_adjust(left=0.28, right=0.97, top=0.95, bottom=0.05)
    fig.savefig(path, dpi=220)
    plt.close(fig)


def plot_match_distribution(match_df: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(13, 8))
    bins = np.linspace(match_df["eleanor_avg"].min(), match_df["eleanor_avg"].max(), 24)
    ax.hist(match_df["eleanor_avg"], bins=bins, color="#3772ff", alpha=0.85, edgecolor="#ffffff", linewidth=0.7)
    ax.axvline(match_df["eleanor_avg"].mean(), color="#ff006e", linewidth=3, label=f"Mean {match_df['eleanor_avg'].mean():.3f}")
    ax.axvline(match_df["eleanor_avg"].median(), color="#ffbe0b", linewidth=3, label=f"Median {match_df['eleanor_avg'].median():.3f}")
    ax.set_title("Eleanor Match Score Distribution", fontsize=20, weight="bold")
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
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    seed_df, head_df, match_df = evaluate_eleanor(SEEDS, REPETITIONS, ROUNDS)
    seed_df.to_csv(OUTPUT_DIR / "eleanor_seed_validation.csv", index=False)
    head_df.to_csv(OUTPUT_DIR / "eleanor_head_to_head.csv", index=False)
    match_df.to_csv(OUTPUT_DIR / "eleanor_match_scores.csv", index=False)
    summary = {
        "strategy": "Eleanor",
        "rounds": ROUNDS,
        "repetitions": REPETITIONS,
        "seeds": SEEDS,
        "rank_counts": seed_df["rank"].value_counts().sort_index().to_dict(),
        "mean_average_score_per_turn": float(seed_df["average_score_per_turn"].mean()),
        "min_gap_to_best_other": float(seed_df["gap_to_best_other"].min()),
        "mean_head_to_head_margin": float(head_df["margin"].mean()),
        "negative_head_to_head_opponents": head_df.groupby("opponent")["margin"].mean().loc[lambda s: s < 0].sort_values().to_dict(),
    }
    (OUTPUT_DIR / "eleanor_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    plot_seed_consistency(seed_df, OUTPUT_DIR / "eleanor_seed_consistency.png")
    plot_head_to_head(head_df, OUTPUT_DIR / "eleanor_head_to_head.png")
    plot_match_distribution(match_df, OUTPUT_DIR / "eleanor_match_distribution.png")
    print(seed_df.to_string(index=False))


if __name__ == "__main__":
    main()
