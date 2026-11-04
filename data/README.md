# Data

Nothing in `data/` is committed except this file. Every teammate downloads the data
locally with the steps below. All three datasets are on figshare under **CC BY 4.0**.

| Dataset | Role in this project | Download size | figshare record | Paper |
|---|---|---|---|---|
| GRAZPEDWRI-DX | Main dataset: train, val, test | 16.3 GB | [10.6084/m9.figshare.14825193](https://doi.org/10.6084/m9.figshare.14825193) | [Nagy et al., *Sci Data* 9, 222 (2022)](https://doi.org/10.1038/s41597-022-01328-z) |
| FracAtlas | Held-out test (hand X-rays, has normals) | 338 MB | [10.6084/m9.figshare.22363012](https://doi.org/10.6084/m9.figshare.22363012) | [Abedeen et al., *Sci Data* 10, 521 (2023)](https://doi.org/10.1038/s41597-023-02432-4) |
| PediURF | Held-out test (forearm fractures, no normals) | 2.3 GB | [10.6084/m9.figshare.29998954](https://doi.org/10.6084/m9.figshare.29998954) | [Tang et al., *Sci Data* (2026)](https://doi.org/10.1038/s41597-026-06666-w) |

You need about **40 GB** free: roughly 19 GB of zips plus the same again once
extracted. You can delete the zips after extracting.

## Target layout

Everything downloaded goes in `data/external/`. Anything we derive from it (resized
caches, splits, features) goes in `data/interim/` or `data/processed/`.

```
data/
├── README.md                  <- this file (the only tracked file in data/)
├── external/
│   ├── grazpedwri/
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

```bash
mkdir -p data/external/grazpedwri && cd data/external/grazpedwri
curl -L -o dataset.csv          https://ndownloader.figshare.com/files/35026432
curl -L -o folder_structure.zip https://ndownloader.figshare.com/files/34268819
curl -L -o images_part1.zip     https://ndownloader.figshare.com/files/34268828
curl -L -o images_part2.zip     https://ndownloader.figshare.com/files/34268849
curl -L -o images_part3.zip     https://ndownloader.figshare.com/files/34268864
curl -L -o images_part4.zip     https://ndownloader.figshare.com/files/34268891

unzip -q folder_structure.zip                                  # yolov5/ pascalvoc/ supervisely/ notebooks/
for i in 1 2 3 4; do unzip -q images_part$i.zip -d images; done  # the image zips are flat PNGs
cd -
```

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

Run `md5sum <file>` (or `certutil -hashfile <file> MD5` on Windows) and compare
the result with this table. The hashes are the ones figshare publishes.

| File | Bytes | MD5 |
|---|---|---|
| grazpedwri/dataset.csv | 1,850,724 | `f2e996300443654faa62983b7ef1b4c1` |
| grazpedwri/folder_structure.zip | 26,304,897 | `e484b434286428750e9c838a7ed6ada7` |
| grazpedwri/images_part1.zip | 4,046,496,654 | `964fae38f2f2b6657463922838ddec0e` |
| grazpedwri/images_part2.zip | 4,122,307,169 | `4c0e859f24166584bbb34800040d9b71` |
| grazpedwri/images_part3.zip | 3,851,047,067 | `9c61c1acc2930d414d1e8141e265b01e` |
| grazpedwri/images_part4.zip | 4,207,646,096 | `d35abc668fcec0b5805048760fe448de` |
| fracatlas/FracAtlas.zip | 338,436,460 | `fe9da2c7c285915ebee69dfdab8fd396` |
| pediurf/PediURF.zip | 2,278,335,773 | `230c654fa75278a981fb0addea1855ea` |
| pediurf/train.csv | 263,544 | `faffccb7f3fe9431aafa45f051954eb7` |
| pediurf/test.csv | 65,986 | `8d1f91b64c7b9d5831205c829739474d` |

Expected counts after extracting:

- GRAZPEDWRI-DX: 20,327 PNGs in `images/` and 20,327 rows in `dataset.csv` (6,091 patients).
- FracAtlas: 4,085 images, but only 4,083 rows in `dataset.csv`.
- PediURF: 5,265 cases with two views each (4,212 train and 1,053 test cases).

## Known quirks

- **GRAZPEDWRI-DX:** an empty `fracture_visible` means no fracture. Split by
  `patient_id`, because one child can have up to 30 images.
- **FracAtlas:** 2 non-fractured images have no row in `dataset.csv`, so leave
  them out. There is no patient ID.
- **PediURF:** every image shows a fracture, so it can only measure sensitivity.
  In `test.csv` the first header cell is a case ID (`63478201302170280`) where it
  should say `Category`, so rename that column after loading. Two views share a
  case folder, so group by folder.
