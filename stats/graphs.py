from stats.mongo import server_metrics
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import time
import math

PUSH_INTERVAL_SECONDS = 10
GAP_THRESHOLD = timedelta(seconds=PUSH_INTERVAL_SECONDS * 2)

DARK_BG = "#0f1117"
AX_BG = "#161b22"
GRID_COLOR = "#30363d"
LINE_COLOR = "#58a6ff"
FILL_COLOR = "#58a6ff"


def plot_metric(metric, minutes=60, ylabel="", multiply=1.0):
    """
    Produce a dark-themed graph with gap detection and area shading.

    - Breaks line when server is offline
    - Shades area under curve
    - Optimized for Discord embeds
    """
    since = datetime.utcnow() - timedelta(minutes=minutes)

    cursor = server_metrics.find(
        {"timestamp": {"$gte": since}},
        {"timestamp": 1, metric: 1},
    ).sort("timestamp", 1)

    times = []
    values = []

    last_ts = None

    for doc in cursor:
        if metric not in doc:
            continue

        ts = doc["timestamp"]
        val = doc[metric] * multiply
        if last_ts is not None and (ts - last_ts) > GAP_THRESHOLD:
            times.append(ts)
            values.append(float("nan"))

        times.append(ts)
        values.append(val)
        last_ts = ts

    if not times:
        return None

    fig, ax = plt.subplots(figsize=(9, 4.5))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(AX_BG)

    ax.plot(
        times,
        values,
        color=LINE_COLOR,
        linewidth=2.2,
        solid_capstyle="round",
    )

    ax.fill_between(
        times,
        values,
        0,
        color=FILL_COLOR,
        alpha=0.25,
        interpolate=False,
    )

    ax.grid(
        True,
        which="major",
        linestyle="--",
        linewidth=0.6,
        color=GRID_COLOR,
        alpha=0.6,
    )

    ax.set_xlabel("Time", color="white", labelpad=8)
    ax.set_ylabel(ylabel or metric, color="white", labelpad=8)

    ax.tick_params(colors="white", labelsize=9)

    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)

    ax.set_title(
        f"{metric.replace('_', ' ').title()} — last {minutes} min",
        color="white",
        fontsize=12,
        pad=12,
        loc="left",
    )

    plt.tight_layout()

    path = f"/tmp/{metric}_{int(time.time())}.png"
    plt.savefig(
        path,
        dpi=140,
        facecolor=fig.get_facecolor(),
        bbox_inches="tight",
    )
    plt.close(fig)

    return path
