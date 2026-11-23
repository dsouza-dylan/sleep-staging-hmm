# Data

The raw data is not committed to this repository because of its size (about 7 GB). Follow the instructions below to recreate this folder locally. After downloading, the expected structure is:

```
data/
├── SC-subjects.xls
├── sleep-cassette/
│   ├── SC4001E0-PSG.edf
│   ├── SC4001EC-Hypnogram.edf
│   ├── ...
│   ├── SC4822G0-PSG.edf
│   └── SC4822GC-Hypnogram.edf
└── processed/
```

`processed/` is created by `analysis/build_data.ipynb` and does not need to be downloaded.

---

## 1. Sleep-EDF Expanded, Sleep Cassette recordings

**Source:** [PhysioNet](https://physionet.org/content/sleep-edfx/1.0.0/), open access with no account required.

**Version used:** v1.0.0 ([doi:10.13026/C2X676](https://doi.org/10.13026/C2X676)).

**Files required:** all 306 files in the `sleep-cassette/` folder: 153 polysomnograms (`*-PSG.edf`) and their 153 hypnograms (`*-Hypnogram.edf`). The Sleep Telemetry recordings (`sleep-telemetry/`) are not used.

**Download steps** (any one of these):
- **AWS CLI**, fastest:
  ```
  aws s3 sync --no-sign-request s3://physionet-open/sleep-edfx/1.0.0/sleep-cassette/ data/sleep-cassette/
  ```
- **wget:**
  ```
  wget -r -N -c -np -nH --cut-dirs=4 -P data/sleep-cassette https://physionet.org/files/sleep-edfx/1.0.0/sleep-cassette/
  ```
- **Browser:** download the full ZIP (8.1 GB, which also includes the telemetry study) from the [dataset page](https://physionet.org/content/sleep-edfx/1.0.0/) and copy its `sleep-cassette/` folder here.

To check the download, compare the files with PhysioNet's [`SHA256SUMS.txt`](https://physionet.org/files/sleep-edfx/1.0.0/SHA256SUMS.txt).

---

## 2. Subject spreadsheet

**Source:** the same [PhysioNet dataset](https://physionet.org/content/sleep-edfx/1.0.0/).

**File required:** [`SC-subjects.xls`](https://physionet.org/files/sleep-edfx/1.0.0/SC-subjects.xls), with each subject's age, sex, and lights-off time for each night.

**Download steps:**
1. Download `SC-subjects.xls` from the link above.
2. Place it directly in `data/`, without renaming or converting it. `build_data.ipynb` reads it with `pandas` and the `python-calamine` package.

---

## Citation

Kemp, B., Zwinderman, A. H., Tuk, B., Kamphuisen, H. A. C., & Oberyé, J. J. L. (2000). *Analysis of a sleep-dependent neuronal feedback loop: The slow-wave microcontinuity of the EEG*. IEEE Transactions on Biomedical Engineering, 47(9), 1185–1194. https://doi.org/10.1109/10.867928

---

## Reproducibility notes
- All files were downloaded in November 2026. Most came from a [Kaggle mirror](https://www.kaggle.com/datasets/iamommpatel/physiobank-database-sleep-edfx-cassette), which is missing `SC4481F0-PSG.edf`; that file was downloaded from PhysioNet. All 306 recording files and `SC-subjects.xls` match PhysioNet's published SHA-256 checksums.
- The data contains 153 recordings from 78 subjects. Subjects 13, 36, and 52 have one night each; all others have two.
- PhysioNet versions are fixed, so v1.0.0 should give identical results.
- No raw files are modified. All processing takes place in `analysis/build_data.ipynb`.
