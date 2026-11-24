# Shortcut Learning in Pediatric Wrist Fracture Detection

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Detecting fractures in pediatric wrist X-rays, and checking whether models rely on shortcuts like casts or age instead of the fracture.

## Team

**Call sign:** Snap

**Members:**

- Fahim Ahamed
- Zahra Khan
- Lloyd Empedrado

## Meeting notes

Weekly meeting notes live in the
[project wiki](https://github.com/csci1910-snap/wrist-fracture-detection/wiki),
one page per week.

## Team protocols

Everyone follows these, no exceptions.

1. **Never push to `main`.** Every change goes on its own branch and gets merged
   through a pull request (PR). At least one teammate reviews a PR before it is merged.
   A branch ruleset (`protect-main`) enforces this: GitHub rejects direct pushes and
   force pushes to `main`, and a PR needs one approval from someone other than its
   author before it can be merged.
2. **One issue per task.** Before starting work, open a GitHub issue (or pick an
   existing one) and assign yourself. Name your branch after it, e.g.
   `12-age-baseline`, and write `Closes #12` in the PR description.
3. **Clear commit messages.** Write the subject in the imperative, say what changed,
   and keep it under about 72 characters, e.g. `Add patient-level split script`
   and not `update` or `fix stuff`. If you commit through the GitHub website, check
   the message and description before you click commit, because the site pre-fills
   generic ones like `Update README.md`.
4. **Describe notebooks in the commit description.** When a commit adds or changes
   a notebook, give each one a line or two in the commit description (the part below
   the subject): what it does, which data and model it uses, and the key result.
   For example:

   ```
   Add ResNet-50 baseline notebook

   notebooks/1.1_resnet50-baseline_fahim.ipynb: fine-tunes ImageNet ResNet-50
   on the full GRAZPEDWRI-DX train split (8 epochs, 256x512). Test AUC 0.988,
   clean-test AUC 0.984.
   ```

5. **Same plotting style for everyone.** All figures use the shared style in
   `src/snap/plots.py` so the plots look the same across notebooks and the report.
   *The standard plotting code will be added soon.* Until then, keep plots simple
   and label every axis.
6. **Notebook names follow `<stage>.<n>_<topic>_<author>.ipynb`.**

   | Part | Rule | Example |
   |---|---|---|
   | `<stage>` | `0` data prep and analysis, `1` modeling, `2` evaluation | `1` |
   | `<n>` | Running number inside the stage. Take the next free one in the folder. | `1` |
   | `<topic>` | A few lowercase words joined with hyphens | `resnet50-baseline` |
   | `<author>` | Your first name, lowercase | `fahim` |
   | **Result** | | `1.1_resnet50-baseline_fahim.ipynb` |

   Underscores separate the four parts, and hyphens join the words inside the topic.
   More examples:

   ```
   0.1_dataset-overview_fahim.ipynb
   0.2_shortcut-tables_member2.ipynb
   1.1_resnet50-baseline_fahim.ipynb
   1.2_clean-only-training_member3.ipynb
   2.1_letter-masking_fahim.ipynb
   ```

   Sorted by name, the notebooks then read in pipeline order: data, then models,
   then evaluation. Code that more than one notebook needs goes in `src/snap/`
   instead of being copied between notebooks.

7. **Commit only what belongs in the repo.** Never commit data, model checkpoints,
   caches, zips, or personal scratch files. Add files by name (`git add path/to/file`)
   instead of `git add .` or `git add -A`, and run `git status` before every commit to
   see exactly what will be included. The `.gitignore` blocks the common large files,
   but it can't catch everything.

## Setup

With conda (installs `requirements.txt` and this package in editable mode):

```bash
conda env create -f environment.yml
conda activate wrist-fracture-detection
```

Or with pip, in any Python 3.12 environment:

```bash
pip install -r requirements.txt
pip install -e .
```

A GPU is optional. Everything runs on CPU, just slower. If you have an NVIDIA GPU
and want to use it, install `torch` and `torchvision` first with the CUDA command from
[pytorch.org](https://pytorch.org/get-started/locally/), then run the steps above.

## Data

The data is not in this repo. See [data/README.md](data/README.md) for download
links, checksums and the expected folder layout.

## Reproduce the results

One command runs the pipeline from the raw data zip to a saved validation metric.

1. Do the [Setup](#setup) steps and activate the environment.
2. Download `14825193.zip` into `data/external/` (step 1 in
   [data/README.md](data/README.md)). This is the only manual step.
3. From the repo root, run:

   ```bash
   python src/scripts/run_pipeline.py
   ```

The script runs these notebooks in order and stops at the first one that fails:

| Step | Notebook | Writes |
|---|---|---|
| 1 | `0.1_data-pipeline_fahim` | `data/processed/graz.csv` (split 70/15/15 by `patient_id`, seed 42), cleaned 256x512 images |
| 2 | `0.2_data-pipeline-localization_fahim` | grid cell targets, cast pairs, location prior, YOLO export |
| 3 | `1.4_grid-baseline_zahra` | HOG + SIFT features, LR and GB runs in `models/1.4_grid-baseline_zahra/<run>/` |
| 4 | `1.5_small-cnn-grid_lloyd` | small CNN runs in `models/1.5_small-cnn-grid_lloyd/<run>/` |
| 5 | `2.1_model-comparison_fahim` | `models/2.1_model-comparison_fahim/val_metrics.csv`, one row per run |

- The result is `models/2.1_model-comparison_fahim/val_metrics.csv`. The script prints it at the end.
- Executed copies of the notebooks go to `reports/pipeline_run/`, so `notebooks/` is not changed.
- `1_1_resnet50_features_baseline_zahra`, `1.2_resnet50-features_baseline_lloyd` and
  `1.3_resnet50-features-clean_fahim` are old baselines, so they are not included.
- Expected time: about 2 hours for 0.1 to 1.4 on a 22-thread CPU (1.4 features about 40 min,
  training about 25 min per seed). 1.5 uses a GPU if it finds one: about 70 s per epoch and
  about 30 min per run. Without a GPU it runs on the CPU, much slower.
- Disk: about 41 GB for the data (see [data/README.md](data/README.md)), plus a few GB for
  the YOLO export in 0.2 and the model outputs.
- The notebooks use the `python3` kernel, which starts the first `python` on your `PATH`.
  Run the command inside the activated environment.

### Reproducibility run

A teammate who did not write the script ran it from a fresh clone.

| Who | Date | Machine | Run time | Differences from the committed numbers |
|---|---|---|---|---|
| Zahra Khan | | | | |

## Project Organization

```
├── Makefile           <- Makefile with convenience commands like `make data` or `make lint`
├── README.md          <- The top-level README for developers using this project.
├── environment.yml    <- Conda environment; installs requirements.txt and this package
├── requirements.txt   <- Python dependencies
├── data               <- Not tracked except data/README.md (how to download)
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks, named `<stage>.<n>_<topic>_<author>.ipynb`
│                         (stage 0 data prep and analysis, 1 modeling, 2 evaluation),
│                         e.g. `0.1_dataset-overview_fahim.ipynb`. See Team protocols.
│
├── pyproject.toml     <- Package metadata for snap and configuration for ruff
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
└── src                <- Source code for use in this project.
    │
    ├── scripts        <- Standalone utility scripts (data checks, splits, preprocessing)
    │
    └── snap           <- The project's Python package (`import snap`)
        │
        ├── __init__.py             <- Makes snap a Python module
        │
        ├── config.py               <- Store useful variables and configuration
        │
        ├── dataset.py              <- Scripts to download or generate data
        │
        ├── features.py             <- Code to create features for modeling
        │
        ├── modeling
        │   ├── __init__.py
        │   ├── predict.py          <- Code to run model inference with trained models
        │   └── train.py            <- Code to train models
        │
        └── plots.py                <- Code to create visualizations
```

