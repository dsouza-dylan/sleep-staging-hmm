# Sleep Staging with Hidden Markov Models

Four notebooks on the Sleep Cassette subset of Sleep-EDF Expanded (153 overnight recordings from 78 healthy subjects), asking whether a hidden Markov model trained without labels can find the expert-scored sleep stages, and how much labels help:

**Data** (`build_data.ipynb`) pairs each recording with its expert hypnogram, trims it to the main sleep period, and computes log band power from one EEG and one EOG channel for every 30-second epoch.

**Exploration** (`eda.ipynb`) checks how well the features separate the stages, whether they are close to Gaussian, and how the experts' stages follow each other over the night.

**Training** (`train_hmm.ipynb`) fits a supervised HMM by maximum likelihood and an unsupervised HMM by Baum–Welch for K = 2 to 5 stages, decodes held-out subjects with Viterbi under 5-fold subject-level cross-validation, and runs an ablation, a learning curve, and a label-free sensitivity check.

**Evaluation** (`evaluate_models.ipynb`) compares the models with Cohen's kappa, macro-F1, and per-stage results, and interprets the unsupervised states, the learned transitions, and the convergence of Baum–Welch.


## Setup

Requires **Python 3.12**.

```bash
pip install -r requirements.txt
```

Download the data as described in [`data/README.md`](data/README.md): the 306 Sleep Cassette EDF files into `data/sleep-cassette/` and `SC-subjects.xls` into `data/`.


## Run

Open the notebooks in `analysis/` (with VS Code or Jupyter) and run them in order:
`build_data.ipynb` → `eda.ipynb` → `train_hmm.ipynb` → `evaluate_models.ipynb`

Fitted models are saved in `results/fits/` and reloaded on later runs; delete that folder after changing the features.


## AI and human contribution
The committed pieces of code reflect a byproduct of pair-programming with Claude Code, wherein the authors set direction through prompts and iteratively refined Claude-generated code and explanations through review and in-notebook testing, as well as clarifications within the notebook writeup. The model Opus 5.5 was used to improve the code readability, notebook structure, as well as for drafting helper functions. These outputs were human-verified at every iteration, and analytical choices such as model selection, project direction (comparison of supervised versus unsupervised), and repository architecture were made by the authors. Finally, Claude Code was used to engineer robustness checks, which were human-verified and used to validate our findings.