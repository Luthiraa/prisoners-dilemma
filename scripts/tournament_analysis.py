from __future__ import annotations

import json
import math
import random
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List

import matplotlib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ipdlab.strategies import PayoffMatrix, Strategy, create_axelrod_first_players, create_named_strategy


matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT_DIR = ROOT / "outputs" / "analysis"
ROUNDS = 200
REPETITIONS = 1
SEED = 7

NAMED_FIELD = [
    "all_c",
    "all_d",
    "tit_for_tat",
    "spiteful",
    "soft_majo",
    "hard_majo",
    "per_cd",
    "per_ccd",
    "per_ddc",
    "mistrust",
    "pavlov",
    "tf2t",
    "hard_tft",
    "slow_tft",
    "gradual",
    "prober",
    "mem2",
    "grok",
]

NAME_REPLACEMENTS = {
    "First by Tideman and Chieruzzi": "Tideman & Chieruzzi",
    "First by Stein and Rapoport": "Stein & Rapoport",
    "First by Nydegger": "Nydegger",
    "First by Grofman": "Grofman",
    "First by Shubik": "Shubik",
    "First by Davis": "Davis",
    "First by Graaskamp": "Graaskamp",
    "First by Downing": "Downing",
    "First by Feld": "Feld",
    "First by Joss": "Joss",
    "First by Tullock": "Tullock",
    "First by Anonymous": "Anonymous",
}


@dataclass
class MatchRecord:
    repetition: int
    player_a: str
    player_b: str
    score_a: float
    score_b: float
    avg_a: float
    avg_b: float
    cooperation_a: float
    cooperation_b: float


def play_match(player_a: Strategy, player_b: Strategy, rounds: int, seed: int, payoffs: PayoffMatrix) -> MatchRecord:
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
    return MatchRecord(
        repetition=0,
        player_a=player_a.name(),
        player_b=player_b.name(),
        score_a=score_a,
        score_b=score_b,
        avg_a=score_a / rounds,
        avg_b=score_b / rounds,
        cooperation_a=history_a.count("C") / rounds,
        cooperation_b=history_b.count("C") / rounds,
    )


def build_field() -> list[Strategy]:
    players = [create_named_strategy(name) for name in NAMED_FIELD]
    players.extend(create_axelrod_first_players())
    deduped: list[Strategy] = []
    seen: set[str] = set()
    for player in players:
        if player.name() not in seen:
            deduped.append(player)
            seen.add(player.name())
    return deduped


def run_tournament(players: list[Strategy], rounds: int, repetitions: int, seed: int, payoffs: PayoffMatrix) -> pd.DataFrame:
    master_rng = random.Random(seed)
    rows: list[dict] = []
    for repetition in range(repetitions):
        for left_index, left_player in enumerate(players):
            for right_index in range(left_index, len(players)):
                right_player = players[right_index]
                match_seed = master_rng.randint(0, 2**31 - 1)
                result = play_match(left_player.clone(), right_player.clone(), rounds, match_seed, payoffs)
                result.repetition = repetition
                rows.append(asdict(result))
                if left_index != right_index:
                    rows.append(
                        {
                            "repetition": repetition,
                            "player_a": result.player_b,
                            "player_b": result.player_a,
                            "score_a": result.score_b,
                            "score_b": result.score_a,
                            "avg_a": result.avg_b,
                            "avg_b": result.avg_a,
                            "cooperation_a": result.cooperation_b,
                            "cooperation_b": result.cooperation_a,
                        }
                    )
    return pd.DataFrame(rows)


def compute_standings(matches: pd.DataFrame) -> pd.DataFrame:
    standings = (
        matches.groupby("player_a")
        .agg(
            total_score=("score_a", "sum"),
            average_score_per_turn=("avg_a", "mean"),
            average_cooperation=("cooperation_a", "mean"),
            match_count=("player_b", "count"),
            volatility=("avg_a", "std"),
        )
        .reset_index()
        .rename(columns={"player_a": "strategy"})
    )
    standings["volatility"] = standings["volatility"].fillna(0.0)
    standings = standings.sort_values(["average_score_per_turn", "total_score"], ascending=[False, False]).reset_index(drop=True)
    standings["rank"] = np.arange(1, len(standings) + 1)
    return standings


def compute_space_coordinates(matrix: pd.DataFrame) -> pd.DataFrame:
    centered = matrix.values - matrix.values.mean(axis=0, keepdims=True)
    u, s, _ = np.linalg.svd(centered, full_matrices=False)
    coords = u[:, :2] * s[:2]
    coord_df = pd.DataFrame(coords, index=matrix.index, columns=["x", "y"]).reset_index().rename(columns={matrix.index.name or "index": "strategy"})
    coord_df["radius"] = np.sqrt(coord_df["x"] ** 2 + coord_df["y"] ** 2)
    coord_df["angle_deg"] = np.degrees(np.arctan2(coord_df["y"], coord_df["x"]))
    return coord_df


def normalize_strategy_labels(frame: pd.DataFrame) -> pd.DataFrame:
    updated = frame.copy()
    for column in updated.columns:
        if updated[column].dtype == object:
            updated[column] = updated[column].replace(NAME_REPLACEMENTS, regex=True)
    return updated


def style_axes(ax: plt.Axes) -> None:
    ax.set_facecolor("#07111f")
    ax.grid(True, alpha=0.14, linestyle="--", linewidth=0.8, color="#9fd3ff")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors="#d9ecff")
    ax.xaxis.label.set_color("#e9f6ff")
    ax.yaxis.label.set_color("#e9f6ff")
    ax.title.set_color("#f7fbff")


def add_cosmic_backdrop(ax: plt.Axes) -> None:
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    gradient = np.linspace(0, 1, 400)
    field = np.outer(np.ones(400), gradient)
    ax.imshow(
        field,
        extent=[x0, x1, y0, y1],
        origin="lower",
        cmap=plt.cm.get_cmap("mako") if "mako" in plt.colormaps() else plt.cm.Blues,
        alpha=0.22,
        aspect="auto",
        zorder=0,
    )


def plot_rank_lollipop(standings: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(13, 10))
    style_axes(ax)
    plot_df = standings.sort_values("average_score_per_turn")
    colors = plt.cm.turbo(np.linspace(0.1, 0.95, len(plot_df)))
    ax.hlines(plot_df["strategy"], 0, plot_df["average_score_per_turn"], color=colors, linewidth=3.0, alpha=0.88)
    ax.scatter(plot_df["average_score_per_turn"], plot_df["strategy"], s=150, c=colors, edgecolor="#f7fbff", linewidth=0.5, zorder=3)
    ax.scatter(plot_df["average_score_per_turn"], plot_df["strategy"], s=420, c=colors, alpha=0.10, linewidth=0, zorder=2)
    ax.set_title("Score Skyline", fontsize=20, weight="bold")
    ax.set_xlabel("Average Score Per Turn")
    ax.set_ylabel("")
    add_cosmic_backdrop(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_heatmap(matrix: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(15, 13))
    image = ax.imshow(matrix.values, cmap="inferno", aspect="auto")
    ax.set_facecolor("#050816")
    ax.set_xticks(np.arange(len(matrix.columns)))
    ax.set_yticks(np.arange(len(matrix.index)))
    ax.set_xticklabels(matrix.columns, rotation=90, fontsize=8, color="#dfefff")
    ax.set_yticklabels(matrix.index, fontsize=8, color="#dfefff")
    ax.set_title("Pairwise Pressure Map", fontsize=20, weight="bold", color="#f8fbff")
    cbar = fig.colorbar(image, ax=ax, fraction=0.025, pad=0.01, label="Average score per turn")
    cbar.ax.yaxis.label.set_color("#dfefff")
    cbar.ax.tick_params(colors="#dfefff")
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_strategy_space(space_df: pd.DataFrame, standings: pd.DataFrame, path: Path) -> None:
    merged = space_df.merge(standings, on="strategy", how="left")
    fig, ax = plt.subplots(figsize=(14, 11))
    style_axes(ax)
    ax.axhline(0, color="#9fd3ff", linewidth=1.1, alpha=0.35)
    ax.axvline(0, color="#9fd3ff", linewidth=1.1, alpha=0.35)
    for radius in [1, 2, 3]:
        ax.add_patch(plt.Circle((0, 0), radius, fill=False, color="#6ac6ff", alpha=0.12, linewidth=1.0))
    scatter = ax.scatter(
        merged["x"],
        merged["y"],
        s=200 + 2200 * merged["average_cooperation"],
        c=merged["average_score_per_turn"],
        cmap="turbo",
        alpha=0.93,
        edgecolor="#f5fbff",
        linewidth=0.55,
    )
    ax.scatter(
        merged["x"],
        merged["y"],
        s=600 + 2600 * merged["average_cooperation"],
        c=merged["average_score_per_turn"],
        cmap="turbo",
        alpha=0.10,
        linewidth=0,
        zorder=1,
    )
    for _, row in merged.iterrows():
        ax.text(row["x"] + 0.035, row["y"] + 0.035, row["strategy"], fontsize=8, color="#eef8ff")
    ax.text(0.02, 0.97, "High score\ncooperators", transform=ax.transAxes, va="top", color="#9fe870", fontsize=10, weight="bold")
    ax.text(0.82, 0.97, "punishers /\nvolatile", transform=ax.transAxes, va="top", color="#ffb37a", fontsize=10, weight="bold")
    ax.text(0.02, 0.08, "stable\nreciprocators", transform=ax.transAxes, va="bottom", color="#8fd3ff", fontsize=10, weight="bold")
    ax.text(0.82, 0.08, "exploiters /\nfragile", transform=ax.transAxes, va="bottom", color="#ff8db6", fontsize=10, weight="bold")
    ax.set_title("Strategy Orbit Map", fontsize=21, weight="bold")
    ax.set_xlabel("Coordinate X")
    ax.set_ylabel("Coordinate Y")
    add_cosmic_backdrop(ax)
    cbar = fig.colorbar(scatter, ax=ax, fraction=0.03, pad=0.02, label="Average score per turn")
    cbar.ax.yaxis.label.set_color("#dfefff")
    cbar.ax.tick_params(colors="#dfefff")
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_cooperation_bubble(standings: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(13, 10))
    style_axes(ax)
    scatter = ax.scatter(
        standings["average_cooperation"],
        standings["average_score_per_turn"],
        s=240 + 4000 * standings["volatility"],
        c=standings["rank"],
        cmap="Spectral_r",
        alpha=0.86,
        edgecolor="#f4fbff",
        linewidth=0.5,
    )
    ax.scatter(
        standings["average_cooperation"],
        standings["average_score_per_turn"],
        s=450 + 4500 * standings["volatility"],
        c="#7df9ff",
        alpha=0.06,
        linewidth=0,
    )
    for _, row in standings.iterrows():
        ax.text(row["average_cooperation"] + 0.005, row["average_score_per_turn"] + 0.005, row["strategy"], fontsize=8, color="#ecf8ff")
    ax.set_title("Cooperation Tension Field", fontsize=20, weight="bold")
    ax.set_xlabel("Average cooperation rate")
    ax.set_ylabel("Average score per turn")
    add_cosmic_backdrop(ax)
    cbar = fig.colorbar(scatter, ax=ax, fraction=0.03, pad=0.02, label="Rank")
    cbar.ax.yaxis.label.set_color("#dfefff")
    cbar.ax.tick_params(colors="#dfefff")
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_polar_constellation(space_df: pd.DataFrame, standings: pd.DataFrame, path: Path) -> None:
    merged = space_df.merge(standings, on="strategy", how="left")
    fig = plt.figure(figsize=(13, 13))
    ax = fig.add_subplot(111, projection="polar")
    theta = np.radians((merged["angle_deg"] + 360) % 360)
    radius = merged["average_score_per_turn"] + 0.35 * merged["average_cooperation"]
    colors = plt.cm.twilight_shifted(merged["average_cooperation"])
    ax.set_facecolor("#050816")
    ax.scatter(theta, radius, s=100 + 1500 * merged["volatility"], c=colors, alpha=0.90, edgecolor="#f4fbff", linewidth=0.5)
    label_df = merged.sort_values("average_score_per_turn", ascending=False).head(18)
    for _, row in label_df.iterrows():
        ax.text(math.radians((row["angle_deg"] + 360) % 360), row["average_score_per_turn"] + 0.35 * row["average_cooperation"] + 0.03, row["strategy"], fontsize=8, color="#eef8ff")
    ax.set_title("Tournament Constellation", va="bottom", fontsize=20, weight="bold", color="#f8fbff")
    ax.set_rticks([])
    ax.grid(alpha=0.25, color="#8dd4ff")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_summary_metric(summary: pd.DataFrame, metric: str, title: str, path: Path) -> None:
    plot_df = summary.sort_values(metric, ascending=True)
    plot_df = plot_df.reset_index(drop=True)
    display_labels = plot_df["strategy"].tolist()
    fig_height = max(12, len(plot_df) * 0.46)
    fig, ax = plt.subplots(figsize=(18, fig_height))
    style_axes(ax)
    colors = plt.cm.turbo(np.linspace(0.12, 0.95, len(plot_df)))
    values = plot_df[metric].to_numpy()
    y_positions = np.arange(len(plot_df))
    ax.barh(y_positions, values, color=colors, alpha=0.88, height=0.72)
    ax.scatter(values, y_positions, s=110, color="#f6fbff", edgecolor="#07111f", linewidth=0.7, zorder=3)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(display_labels, color="#000000", fontsize=11, fontweight="semibold")
    ax.set_xlabel("Average score per turn")
    ax.set_title(title, fontsize=21, weight="bold")
    ax.set_xlim(0, max(values) + 0.28)
    for y, value in zip(y_positions, values):
        ax.text(value + 0.015, y, f"{value:.3f}", va="center", fontsize=10, color="#f3fbff", fontweight="bold")
    fig.subplots_adjust(left=0.34, right=0.97, top=0.94, bottom=0.04)
    fig.savefig(path, dpi=220)
    plt.close(fig)


def save_outputs(matches: pd.DataFrame, standings: pd.DataFrame, space_df: pd.DataFrame, matrix: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    matches.to_csv(output_dir / "matches.csv", index=False)
    standings.to_csv(output_dir / "standings.csv", index=False)
    space_df.to_csv(output_dir / "space_coordinates.csv", index=False)
    matrix.to_csv(output_dir / "pairwise_matrix.csv")
    summary = {
        "rounds": ROUNDS,
        "repetitions": REPETITIONS,
        "seed": SEED,
        "players": standings["strategy"].tolist(),
        "top_10": standings.head(10).to_dict(orient="records"),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> None:
    output_dir = OUTPUT_DIR
    players = build_field()
    matches = run_tournament(players, rounds=ROUNDS, repetitions=REPETITIONS, seed=SEED, payoffs=PayoffMatrix())
    standings = compute_standings(matches)
    matrix = matches.pivot_table(index="player_a", columns="player_b", values="avg_a", aggfunc="mean").loc[standings["strategy"], standings["strategy"]]
    space_df = compute_space_coordinates(matrix)
    save_outputs(matches, standings, space_df, matrix, output_dir)
    plot_rank_lollipop(standings, output_dir / "ranking_skyline.png")
    plot_heatmap(matrix, output_dir / "pairwise_heatmap.png")
    plot_strategy_space(space_df, standings, output_dir / "strategy_space.png")
    plot_cooperation_bubble(standings, output_dir / "cooperation_bubble.png")
    plot_polar_constellation(space_df, standings, output_dir / "polar_constellation.png")
    print(f"Saved tournament outputs to {output_dir.resolve()}")
    print(standings[["rank", "strategy", "average_score_per_turn", "average_cooperation"]].head(15).to_string(index=False))


if __name__ == "__main__":
    main()
