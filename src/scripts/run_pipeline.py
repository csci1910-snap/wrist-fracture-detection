# Runs the checkpoint pipeline from the raw data zip to a saved val metric.
# Usage, from the repo root: python src/scripts/run_pipeline.py
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK_DIR = REPO_ROOT / 'notebooks'
OUTPUT_DIR = REPO_ROOT / 'reports' / 'pipeline_run'
RAW_ZIP = REPO_ROOT / 'data' / 'external' / '14825193.zip'
VAL_METRICS = REPO_ROOT / 'models' / \
    '2.1_model-comparison_fahim' / 'val_metrics.csv'

# in pipeline order; each notebook reads only outputs of the ones before it
NOTEBOOKS = [
    '0.1_data-pipeline_fahim',
    '0.2_data-pipeline-localization_fahim',
    '1.4_grid-baseline_zahra',
    '1.5_small-cnn-grid_lloyd',
    '2.1_model-comparison_fahim',
]

if not RAW_ZIP.is_file():
    print(f'Missing {RAW_ZIP}')
    print('Download it first: see "1. GRAZPEDWRI-DX" in data/README.md.')
    sys.exit(1)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
pipeline_start = time.time()

for name in NOTEBOOKS:
    print(f'Running {name} ...', flush=True)
    start = time.time()
    # executed copies go to reports/pipeline_run/, so notebooks/ stays unchanged
    command = [
        sys.executable, '-m', 'jupyter', 'nbconvert',
        '--to', 'notebook',
        '--execute',
        '--ExecutePreprocessor.timeout=-1',
        '--output-dir', str(OUTPUT_DIR),
        str(NOTEBOOK_DIR / f'{name}.ipynb'),
    ]
    result = subprocess.run(command)
    minutes = (time.time() - start) / 60
    if result.returncode != 0:
        print(f'FAILED: {name} after {minutes:.1f} min. See the error above.')
        sys.exit(1)
    print(f'Done: {name} in {minutes:.1f} min')

# self-check: the val metric exists and was written by this run, not an older one
assert VAL_METRICS.is_file(), f'{VAL_METRICS} was not written'
assert VAL_METRICS.stat(
).st_mtime > pipeline_start, f'{VAL_METRICS} is older than this run'

total_minutes = (time.time() - pipeline_start) / 60
print(
    f'\nPipeline finished in {total_minutes:.1f} min. Val metrics ({VAL_METRICS}):')
print(pd.read_csv(VAL_METRICS)[
      ['run', 'image_roc_auc', 'first_box_hit_rate']].to_string(index=False))
