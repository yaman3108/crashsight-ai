# 🛰️ CrashSight AI

**Detecting crash sites from satellite imagery using deep learning, then cross-referencing them with news and incident reports to build an open dataset of documented and undocumented accident locations worldwide.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Pre-Development](https://img.shields.io/badge/Status-Pre--Development-orange)]()
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)]()
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## What Is This?

Satellite imagery captures the entire Earth's surface in remarkable detail — but nobody is systematically scanning it for crash sites. CrashSight AI aims to change that.

The idea is simple: train a computer vision model to recognise the visual signatures of crashes (a plane in a forest, a car submerged in a lake, a ship grounded on a reef), scan satellite imagery globally, and then cross-reference any findings with news articles and official incident databases to see if they've been reported.

The result is an **open dataset** mapping detected anomalies to their most likely real-world event — or flagging them as potentially undocumented.

> ⚠️ **This project is in pre-development.** The architecture is defined, but code is being built. If you're interested in satellite imagery, computer vision, or geospatial ML — this is a ground-floor opportunity to contribute.

---

## How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Phase 1   │     │   Phase 2   │     │   Phase 3   │
│   Dataset   │────▶│   Model     │────▶│   Global    │
│   Assembly  │     │   Training  │     │   Scan      │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
┌─────────────┐     ┌─────────────┐     ┌──────▼──────┐
│   Phase 6   │     │   Phase 5   │     │   Phase 4   │
│   Human     │◀────│   Output    │◀────│   News      │
│   Review    │     │   Dataset   │     │   Cross-Ref │
└─────────────┘     └─────────────┘     └─────────────┘
```

1. **Dataset Assembly** — Collect satellite images of known crash sites from open sources (Sentinel-2, Landsat, Google Earth Engine) and label them.
2. **Model Training** — Train a YOLOv8 object detection model to recognise 10 crash classes.
3. **Global Scan** — Tile satellite imagery and run inference across prioritised zones (coastlines, remote roads, flight corridors).
4. **News Cross-Reference** — For each detection, search NewsAPI, GDELT, NTSB, and other databases for matching reports within a class-specific radius.
5. **Output Dataset** — Score matches and categorise each detection (confirmed, probable, possible, no match, false positive, needs review).
6. **Human Review** — A web interface for contributors to verify detections and assign final verdicts.

---

## Crash Classes

The model is designed to recognise these 10 types of crash sites from a satellite perspective:

| ID | Class | What It Looks Like From Above |
|----|-------|-------------------------------|
| 01 | `PLANE_FOREST` | Clearing, burn scar, or debris trail in forested terrain |
| 02 | `PLANE_WATER` | Debris or partial submersion in a body of water |
| 03 | `PLANE_OPEN_TERRAIN` | Wreckage visible on desert, farmland, or tundra |
| 04 | `SHIP_SHALLOW_WATER` | Vessel visible on seabed through clear shallow water |
| 05 | `SHIP_REEF_COASTAL` | Vessel grounded on reef or coastline |
| 06 | `CAR_SUBMERGED` | Vehicle outline visible through still, clear water |
| 07 | `CAR_CLIFF_RAVINE` | Debris or disturbance at cliff base or ravine floor |
| 08 | `TRAIN_DERAILMENT` | Carriages visible off tracks on embankments or terrain |
| 09 | `HELICOPTER_CRASH` | Rotor blade debris spread pattern in open terrain |
| 10 | `MILITARY_WRECK` | Historical military vehicle/aircraft wrecks in accessible terrain |

> Want to propose a new class? [Open an issue](../../issues/new?template=class_proposal.md) with at least 50 sample images.

---

## Current Status

This project is at **v0.1 — concept and architecture phase**. Here's what exists and what's needed:

- [x] Full system architecture and specification ([docs/architecture.md](docs/architecture.md))
- [x] Repository structure and contribution guidelines
- [ ] Training dataset: collect and annotate 200+ samples for 3 initial classes
- [ ] Baseline YOLOv8 model trained and evaluated
- [ ] Minimal scan pipeline covering one coastal region
- [ ] Basic news cross-reference implementation
- [ ] First output dataset published

---

## Getting Involved

**No contribution is too small.** Whether you label 10 images, fix a typo in the docs, or build an entire pipeline phase — it all matters.

### Quick Start

```bash
# Clone the repo
git clone https://github.com/yaman3108/crashsight-ai.git
cd crashsight-ai

# Set up the environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Where to Start

| If you're good at... | Start here |
|---|---|
| **Geospatial / Remote Sensing** | Help build the imagery download pipeline and scan grid |
| **Computer Vision / ML** | Help curate training data and train the baseline model |
| **NLP** | Build the news cross-reference and entity extraction engine |
| **Web Dev** | Build the human review interface (Streamlit or FastAPI) |
| **Research / Domain Knowledge** | Propose new crash classes or data sources |
| **Documentation** | Write labelling guides for each crash class |

Check the [Issues](../../issues) tab for tasks labelled `good first issue` and `help wanted`.

Read the full [Contributing Guide](CONTRIBUTING.md) before submitting a PR.

---

## Repository Structure

```
crashsight-ai/
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE
├── requirements.txt
├── data/                    # Training data (mostly gitignored)
├── docs/
│   ├── architecture.md      # ← Full system specification
│   ├── labelling_guides/    # Per-class annotation instructions
│   └── model_cards/         # Model version documentation
├── models/                  # Weights and training configs
├── notebooks/               # Exploration and demo notebooks
├── src/                     # All source code
│   ├── dataset/             # Imagery download, tiling, augmentation
│   ├── model/               # Training, evaluation, inference
│   ├── scanner/             # Global scan grid and batch inference
│   ├── crossref/            # News and report cross-referencing
│   ├── dataset_builder/     # Output dataset assembly
│   └── review_ui/           # Human review web interface
└── tests/                   # Unit and integration tests
```

---

## Documentation

- **[Full Architecture Specification](docs/architecture.md)** — The complete technical blueprint. Read this if you want to understand the system in depth.
- **[Contributing Guide](CONTRIBUTING.md)** — How to report bugs, propose changes, and submit pull requests.
- **[Security Policy](SECURITY.md)** — How to handle sensitive findings.

---

## Technology Stack

| Component | Primary Tool |
|---|---|
| Model Training | PyTorch + Ultralytics YOLOv8 |
| Satellite Data | Google Earth Engine API |
| Image Processing | OpenCV, rasterio, GDAL |
| Geospatial Ops | GeoPandas, Shapely |
| News Retrieval | NewsAPI, GDELT |
| NLP | spaCy, HuggingFace Transformers |
| Database | PostgreSQL + PostGIS |
| Review Interface | Streamlit |
| Experiment Tracking | Weights & Biases |

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Ethical Note

This project does not seek to identify individuals, replace official investigation bodies, or process private data. If a detection appears to represent a recent emergency, it is escalated per the protocol described in [SECURITY.md](SECURITY.md). See [docs/architecture.md § 12](docs/architecture.md#12-ethical-considerations--legal-constraints) for full ethical guidelines.

---

*CrashSight AI is a community-driven research project. Built by curious people who looked at the sky and wondered what we're missing on the ground.*
