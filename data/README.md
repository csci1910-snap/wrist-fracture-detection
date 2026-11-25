# Data

Nothing in `data/` is committed except this file. Every teammate downloads the data
locally with the steps below. All three datasets are on figshare under **CC BY 4.0**.

| Dataset | Role in this project | Download size | figshare record | Version | Downloaded | Paper |
|---|---|---|---|---|---|---|
| GRAZPEDWRI-DX | Main dataset: train, val, test | 16.3 GB | [10.6084/m9.figshare.14825193](https://doi.org/10.6084/m9.figshare.14825193) | v2 (2022-05-06) | 2026-10-13 | [Nagy et al., *Sci Data* 9, 222 (2022)](https://doi.org/10.1038/s41597-022-01328-z) |
| FracAtlas | Distribution-shift set: the 1,538 hand images (has normals) | 338 MB | [10.6084/m9.figshare.22363012](https://doi.org/10.6084/m9.figshare.22363012) | v7 (2026-06-13) | 2026-10-13 | [Abedeen et al., *Sci Data* 10, 521 (2023)](https://doi.org/10.1038/s41597-023-02432-4) |
| PediURF | Second distribution-shift set: all 5,265 cases (fractures only, no normals) | 2.3 GB | [10.6084/m9.figshare.29998954](https://doi.org/10.6084/m9.figshare.29998954) | v2 (2025-11-19) | 2026-10-13 | [Tang et al., *Sci Data* (2026)](https://doi.org/10.1038/s41597-026-06666-w) |

GRAZPEDWRI-DX needs about **41 GB** free: the 16 GB zip, 16 GB extracted, 6 GB of
cleaned images in `interim/` and 3 GB in `processed/`. You can delete the zip after
the 0.1 notebook has run.

## Target layout

Everything downloaded goes in `data/external/`. Anything we derive from it (resized
caches, splits, features) goes in `data/interim/` or `data/processed/`.

```
data/
├── README.md                  <- this file (the only tracked file in data/)
├── external/
│   ├── 14825193.zip           <- GRAZPEDWRI-DX "Download all" zip (the only manual step)
│   ├── grazpedwri/            <- extracted from 14825193.zip by notebooks/0.1
│   │   ├── dataset.csv
│   │   ├── images/            <- 20,327 PNGs (16-bit) from images_part1-4.zip
│   │   ├── yolov5/            <- from folder_structure.zip
│   │   ├── pascalvoc/
│   │   ├── supervisely/
│   │   └── notebooks/
│   ├── fracatlas/
│   │   └── FracAtlas/         <- dataset.csv, images/, Annotations/, Utilities/
│   └── pediurf/
│       ├── train.csv
│       ├── test.csv
│       └── PediURF/           <- train/, test/
├── interim/
└── processed/
```

## Download

Run these from the repo root in Git Bash, macOS or Linux. On Windows, `curl` and
`tar` are also built into PowerShell; use `curl.exe` there so PowerShell does not
substitute its own `curl` alias. You can also click the figshare record links
above and download in the browser.

### 1. GRAZPEDWRI-DX

Open the [figshare record](https://doi.org/10.6084/m9.figshare.14825193), click
**Download all**, and save `14825193.zip` (16.3 GB) as `data/external/14825193.zip`.

That is the only manual step. `notebooks/0.1_data-pipeline_fahim.ipynb` extracts
`dataset.csv` into `data/external/grazpedwri/`, then reads the zips inside the bundle
in place (they are stored uncompressed) and extracts `folder_structure.zip` there and
`images_part1-4.zip` into `images/`. The inner zips are never written to disk. Files
already extracted are skipped. A first run takes about 10 minutes on a 22-thread CPU.

### 2. FracAtlas

```bash
mkdir -p data/external/fracatlas && cd data/external/fracatlas
curl -L -o FracAtlas.zip https://ndownloader.figshare.com/files/65518038
unzip -q FracAtlas.zip                                         # creates FracAtlas/
cd -
```

### 3. PediURF

```bash
mkdir -p data/external/pediurf && cd data/external/pediurf
curl -L -o PediURF.zip https://ndownloader.figshare.com/files/57469948
curl -L -o train.csv   https://ndownloader.figshare.com/files/59685386
curl -L -o test.csv    https://ndownloader.figshare.com/files/59685638
unzip -q PediURF.zip                                           # creates PediURF/train/ and PediURF/test/
cd -
```

## Check the downloads

Expected counts after extracting:

- GRAZPEDWRI-DX: 20,327 PNGs in `images/` and 20,327 rows in `dataset.csv` (6,091 patients).
- FracAtlas: 4,085 images, but only 4,083 rows in `dataset.csv`.
- PediURF: 5,265 cases with two views each (4,212 train and 1,053 test cases).

## Splits

The split is defined by code and never changes. `notebooks/0.1_data-pipeline_fahim.ipynb`
splits GRAZPEDWRI-DX 70/15/15 by `patient_id` with seed 42, so no child is in two
splits, and writes the `split` column of `data/processed/graz.csv`.

| Split | Images | Children | Fractured images |
|---|---|---|---|
| train | 14,182 | 4,264 | 9,443 |
| val | 3,202 | 914 | 2,208 |
| test | 2,943 | 913 | 1,899 |
| total | 20,327 | 6,091 | 13,550 |

The shift test uses two completely new datasets, held out from training and model selection.
They need their own preprocessing, like the 0.1 data pipeline notebook does for
GRAZPEDWRI-DX, which is not done yet.

- **FracAtlas hand:** other hospitals, adults as well as children, hand images: the rows of
  its `dataset.csv` with `hand` = 1.
- **PediURF:** another hospital, children, forearm fractures. All cases are used, from both
  its `train.csv` and `test.csv`, since no model trains on it. Every image shows a fracture,
  so it measures recall only.

| Shift set | Cases | Images | Fractured | Not fractured |
|---|---|---|---|---|
| FracAtlas hand | no case ID | 1,538 | 440 | 1,098 |
| PediURF | 5,265 | 10,530 | 10,530 | 0 |

PediURF cases by fracture site: distal 3,374, midshaft 1,319, proximal 572.

Grouping: FracAtlas has no patient ID, so it has no grouping rule. PediURF has two views per
case folder, so results are grouped by case. Neither matters for leakage, because no model
trains on them. 257 of the FracAtlas hand images also show another body part (`mixed` = 1)
and 25 show hardware.

## Known quirks

- **GRAZPEDWRI-DX:** an empty `fracture_visible` means no fracture. One child can
  have up to 30 images, so the split is by `patient_id`.
- **FracAtlas:** 2 non-fractured images have no row in `dataset.csv` and are left
  out. There is no patient ID. It covers hand, leg, hip and shoulder; only the hand
  images are used.
- **PediURF:** every image shows a fracture, so it measures sensitivity only. In
  `test.csv` the first header cell is a case ID (`63478201302170280`) instead of
  `Category`. Two views share a case folder, so results are grouped by case.
