# Checkpoint (Nov 24)

Team Snap. We find and box fractures in pediatric wrist X-rays (GRAZPEDWRI-DX) and check
whether models use shortcuts such as casts instead of the fracture.

## Pipeline

`python src/scripts/run_pipeline.py` runs these notebooks in order (see "Reproduce the
results" in `README.md`):

1. `0.1_data-pipeline_fahim`: extracts the data, splits it 70/15/15 by `patient_id` with
   seed 42 (train 14,182 / val 3,202 / test 2,943 images), removes the L/R markers and
   resizes to 256x512.
2. `0.2_data-pipeline-localization_fahim`: builds the targets for a 32x16 grid (fracture or
   not per cell, plus four distances to the box edges), the cast-pair crops and a location
   prior.
3. `1.4_grid-baseline_zahra`: HOG + SIFT features per cell; logistic regression and gradient
   boosting predict the cell score, regressors predict the box distances.
4. `1.5_small-cnn-grid_lloyd`: a CNN trained from scratch with the same grid output (uses a
   GPU if there is one).
5. `2.1_model-comparison_fahim`: scores every run on val with the same code and writes
   `models/2.1_model-comparison_fahim/val_metrics.csv`.

`1_1_resnet50_features_baseline_zahra`, `1.2_resnet50-features_baseline_lloyd` and
`1.3_resnet50-features-clean_fahim` are old baselines, so they are not included.

The shift test uses two new datasets: FracAtlas hand images (1,538: 440 fractured, 1,098
not) and PediURF (5,265 pediatric forearm cases, 10,530 images, all fractured). Neither is
used for training or model selection. Both still need their own preprocessing. Counts and
grouping are in `data/README.md`.

## Numbers

All numbers are on the val split: image-level ROC AUC, and the share of fractured images
whose first box has IoU >= 0.5 with a true box. The baselines are mean ± std over seeds 42,
1337 and 3407, all run on Fahim's PC; the CNN is one run (seed 42). The runs are logged in
`experiments/README.md`.

| Model | Train set | Val AUC | First box IoU >= 0.5 |
|---|---|---|---|
| HOG + SIFT, logistic regression | all-castpairs | 0.490 ± 0.002 | 39.8% ± 0.1 |
| HOG + SIFT, gradient boosting | all-castpairs | 0.749 ± 0.018 | 52.9% ± 1.3 |
| Small CNN from scratch | all-castpairs | 0.951 (one run) | 82.2% (one run) |

Train sets: `all` is every train image (14,182). `clean` is first visits with no cast
(7,589). `all-castpairs` is `all` plus 7,018 crops of cast images from the 0.2 data pipeline
notebook: 3,509 with the fracture and 3,509 with the fracture cut out, so a cast is a much
weaker sign of a fracture (21,200 images). We train on `all-castpairs` from now on.

Logistic regression is at chance per image. Gradient boosting is the non-deep baseline.

## Next

- **First deep model:** done. The small CNN (`1.5_small-cnn-grid_lloyd`) is in the table
  above: val AUC 0.951, first box IoU >= 0.5 on 82.2% (one run, seed 42).
- **Next deep model:** VGG models (VGG16, VGG19), trained on `all-castpairs`, as the professor suggested at
  the weekly update. We had planned YOLO. Owner: Fahim.
- **First ablation:** on the small CNN, one factor at a time: cast pairs (`all-castpairs` vs
  `all`), depth (5 conv blocks vs fewer) and the loss weight on fracture cells
  (`POS_WEIGHT`). Owner: Lloyd.
- **Responsible-AI evaluation (HW10P4):** a shift test on FracAtlas hand images (other
  hospitals, adults, hands) and PediURF (pediatric forearm, fractures only, so recall only).
  We report the drop from val and check whether the shortcuts we find in the
  interpretability work explain it.

## Risk

The model is meant for a child's first visit, before anyone knows there is a fracture. But
1,569 of the 3,202 val images are follow-up visits. In those, the fracture is already
diagnosed and usually in a cast. A model can score well on them by spotting the cast, without
finding the fracture. So val AUC can make the model look better than it would be at a first
visit.

Check: in 2.1, report AUC on the 1,633 first-visit val images (44% fractured, none with a
cast) next to AUC on all val images. If the first-visit AUC is much lower, the model relies
on the cast.
