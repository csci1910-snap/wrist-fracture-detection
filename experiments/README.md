# Experiment log

One row per notebook. Every number in `docs/checkpoint.md` comes from a row here.

- **Val AUC:** image-level ROC AUC on the val split, mean ± std when there are several seeds.
- **Hit rate:** share of fractured val images whose first box has IoU >= 0.5 with a true
  fracture box. 1.1 to 1.3 draw no boxes.
- **Source:** "2.1" is `models/2.1_model-comparison_fahim/val_metrics.csv`; "notebook" is the
  output saved in the merged notebook.
- **Train sets:** `all` = every train image; `clean` = first visits with no cast;
  `all-castpairs` = `all` plus the cast-pair crops from the 0.2 data pipeline notebook.

| Date | Who | Notebook | Model | Train set | Key settings | Seeds | Val AUC | Hit rate | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-15 | Zahra | 1_1_resnet50_features_baseline_zahra | Frozen ResNet-50 features, LR / GB | all | LR C=0.001, GB 400 trees, both picked by 5-fold CV | 1337, 3407 | 0.911 ± 0.000 / 0.908 ± 0.002 | n/a | old baseline, fracture or not |
| 2026-11-15 | Lloyd | 1.2_resnet50-features_baseline_lloyd | Frozen ResNet-50 features, LR / GB | all | LR C=0.001, GB 400 trees, both picked by 5-fold CV | 42 | 0.911 / 0.909 | n/a | old baseline, fracture or not |
| 2026-11-16 | Fahim | 1.3_resnet50-features-clean_fahim | Frozen ResNet-50 features, LR / GB | clean | 5-fold CV | 42, 1337, 3407 | 0.857 ± 0.000 / 0.858 ± 0.004 | n/a | old baseline, fracture or not |
| 2026-11-22 | Zahra | 1.4_grid-baseline_zahra | HOG + SIFT, LR / GB | all-castpairs | LR C=0.1; GB lr=0.1, 200 iterations; 40 negatives per image | 42 | 0.489 / 0.774 | 0.399 / 0.541 | her environment; `all` and `clean` runs are in the notebook |
| 2026-11-22 | Lloyd | 1.5_small-cnn-grid_lloyd | CNN from scratch, grid head | all-castpairs | 5 conv blocks, AdamW lr=1e-3, wd=1e-4, batch 64, pos_weight=10, early stop on val cell AUC (patience 5) | 42 | n/a | n/a | failed: CPU, about 40 min per epoch, stopped after 12 of 30 epochs |
| 2026-11-23 | Fahim | 1.5_small-cnn-grid_lloyd | CNN from scratch, grid head | all-castpairs | same; early stopping triggered after 24 epochs | 42 | 0.951 | 0.822 | GPU, about 70 s per epoch |
| 2026-11-24 | Zahra | 1.4_grid-baseline_zahra | HOG + SIFT, LR / GB | all-castpairs | same settings as last run; 3 seeds | 42, 1337, 3407 | 0.490 ± 0.002 / 0.749 ± 0.018 | 0.398 ± 0.001 / 0.529 ± 0.013 | edited and rerun for the checkpoint |
