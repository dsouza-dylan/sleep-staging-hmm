# Imports
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Path variables
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW  = os.path.join(BASE, "data", "sleep-cassette")
PROC = os.path.join(BASE, "data", "processed")
OUT  = os.path.join(BASE, "results")
FIG  = os.path.join(BASE, "figures")

for d in (PROC, OUT, FIG):
    os.makedirs(d, exist_ok=True)

# Constants
SEED = 150
N_FOLDS = 5
EPOCH_SEC = 30
EEG_CHANNEL = "EEG Fpz-Cz"
EOG_CHANNEL = "EOG horizontal"

STAGES = ["W", "N1", "N2", "N3", "REM"]

EEG_FEATURES = ["delta", "theta", "alpha", "sigma", "beta"]
EOG_FEATURES = ["eog_slow", "eog_fast"]
FEATURE_SETS = {"EEG": EEG_FEATURES, "EEG+EOG": EEG_FEATURES + EOG_FEATURES}

CLASSES = {
    2: ["Wake", "Asleep"],
    3: ["W", "NREM", "REM"],
    4: ["W", "Light", "Deep", "REM"],
    5: STAGES,
}
MERGES = {
    2: {"W": "Wake", "N1": "Asleep", "N2": "Asleep", "N3": "Asleep", "REM": "Asleep"},
    3: {"W": "W", "N1": "NREM", "N2": "NREM", "N3": "NREM", "REM": "REM"},
    4: {"W": "W", "N1": "Light", "N2": "Light", "N3": "Deep", "REM": "REM"},
    5: {s: s for s in STAGES},
}

LIGHTWAVE = "https://www.physionet.org/lightwave/?db=sleep-edfx/1.0.0"

# Plot style
BLUE, ORANGE, GRAY = "#2a78d6", "#eb6834", "#8a8984"
MODEL_LABELS = {"supervised": "Supervised", "unsupervised": "Unsupervised",
                "unsupervised_1to1": "Unsup. (one-to-one)",
                "classifier": "Supervised, no transitions", "gmm": "GMM (no transitions)",
                "diagonal": "Supervised, diagonal cov."}
MODEL_COLORS = {"supervised": BLUE, "unsupervised": ORANGE}
SEQUENTIAL = LinearSegmentedColormap.from_list("seq", ["#fcfcfb", "#86b6ef", "#1c5cab"])
DIVERGING  = LinearSegmentedColormap.from_list("div", ["#2a78d6", "#f0efec", "#e34948"])

plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 220, "savefig.bbox": "tight", "font.size": 9,
    "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 10,
    "axes.edgecolor": "#c3c2b7", "axes.axisbelow": True, "grid.color": "#e8e7e2",
    "legend.frameon": False, "lines.linewidth": 1.8,
})

# Helper functions
def lightwave_url(psg_path, epoch=0):
    minutes, seconds = divmod(int(epoch) * EPOCH_SEC, 60)
    hours, minutes = divmod(minutes, 60)
    return (f"{LIGHTWAVE}&record=sleep-cassette/{os.path.basename(psg_path)}"
            f"&t0={hours:02d}:{minutes:02d}:{seconds:02d}")

def psg_path(recording):
    names = [f for f in os.listdir(RAW) if f.startswith(recording) and f.endswith("-PSG.edf")]
    return os.path.join(RAW, names[0])

def load_features(path=None):
    path = path or os.path.join(PROC, "features.csv.gz")
    df = pd.read_csv(path, dtype={"subject": str})
    return df.sort_values(["recording", "epoch"], ignore_index=True)

def sequence_lengths(df):
    new = (df["recording"] != df["recording"].shift()) | (df["epoch"].diff() != 1)
    return np.diff(np.append(np.flatnonzero(new), len(df)))

def subject_folds(subjects):
    order = np.random.RandomState(SEED).permutation(sorted(set(subjects)))
    return [sorted(f.tolist()) for f in np.array_split(order, N_FOLDS)]

def collapse(stages, K):
    code = {s: CLASSES[K].index(c) for s, c in MERGES[K].items()}
    return pd.Series(stages).map(code).to_numpy()

def transition_counts(codes, lengths, K):
    counts = np.zeros((K, K))
    for seq in np.split(codes, np.cumsum(lengths)[:-1]):
        np.add.at(counts, (seq[:-1], seq[1:]), 1)
    return counts

def night_position(df):
    asleep = df["epoch"].where(df["stage"] != "W").groupby(df["recording"])
    first, last = asleep.transform("min"), asleep.transform("max")
    position = (df["epoch"] - first) / (last - first)
    return position.where(position.between(0, 1))

def heatmap(ax, values, rows, cols, fmt="{:.2f}", cmap=SEQUENTIAL, vmin=0, vmax=1):
    values = np.asarray(values, dtype=float)
    ax.imshow(values, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            label = fmt.format(values[i, j])
            dark = abs(values[i, j] - (vmin + vmax) / 2 if cmap is DIVERGING else values[i, j] - vmin)
            limit = 0.72 * (vmax - vmin) / 2 if cmap is DIVERGING else 0.6 * (vmax - vmin)
            ax.text(j, i, label, ha="center", va="center", fontsize=8,
                    color="white" if dark > limit else "#0b0b0b")
    ax.set_xticks(range(len(cols)), cols)
    ax.set_yticks(range(len(rows)), rows)
    ax.tick_params(length=0)
    for side in ax.spines.values():
        side.set_visible(False)

def save_figure(fig, name):
    fig.savefig(os.path.join(FIG, name))
