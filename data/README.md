# Data Directory

This directory contains all training data, annotations, and output datasets.

## Structure

- `raw/` — Raw downloaded satellite tiles (gitignored, too large for git)
- `processed/` — Preprocessed, normalised tiles ready for training
- `annotations/` — COCO JSON or YOLO `.txt` bounding box annotation files
- `output_dataset/` — Final detection + cross-reference dataset (Parquet and CSV)

## Important

Most files in this directory are **gitignored** due to size. To get the training data:

1. Run the imagery downloader: `python -m src.dataset.downloader`
2. Or download a pre-built dataset from the project's GitHub Releases / Hugging Face page (when available)

## Dataset Split

Training data follows a 70/15/15 split:
- `processed/train/` — Training images and labels
- `processed/val/` — Validation images and labels
- `processed/test/` — Test images and labels (never used during training or hyperparameter tuning)
