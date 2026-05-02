# CrashSight AI — Project Specification & Contributor Guide

**Version:** 0.1.0 (Open Concept / Community RFC)
**Status:** Pre-development — open for contributions and discussion
**License:** MIT (suggested)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Goals & Non-Goals](#2-goals--non-goals)
3. [Terminology & Definitions](#3-terminology--definitions)
4. [System Architecture (High-Level)](#4-system-architecture-high-level)
5. [Phase 1 — Dataset Construction](#5-phase-1--dataset-construction)
6. [Phase 2 — Model Design & Training](#6-phase-2--model-design--training)
7. [Phase 3 — Global Satellite Scan Pipeline](#7-phase-3--global-satellite-scan-pipeline)
8. [Phase 4 — News & Report Cross-Reference Engine](#8-phase-4--news--report-cross-reference-engine)
9. [Phase 5 — Output Dataset & Categorisation Schema](#9-phase-5--output-dataset--categorisation-schema)
10. [Phase 6 — Validation & Human Review Interface](#10-phase-6--validation--human-review-interface)
11. [Technology Stack (Suggested)](#11-technology-stack-suggested)
12. [Ethical Considerations & Legal Constraints](#12-ethical-considerations--legal-constraints)
13. [Folder & Repository Structure](#13-folder--repository-structure)
14. [How to Publish on GitHub & Invite Contributors](#14-how-to-publish-on-github--invite-contributors)
15. [Roadmap & Open Questions](#15-roadmap--open-questions)

---

## 1. Project Overview

**CrashSight AI** is an open-source research project that combines satellite image analysis, deep learning-based object detection, and automated news cross-referencing to attempt to detect unregistered or undiscovered crash and accident sites across the globe.

The core hypothesis is this: satellite imagery of the Earth's surface, when analysed by a trained computer vision model, may reveal physical signatures of crash events — submerged vehicles, wreckage in forests, debris on coastlines — that have never been formally documented or reported. By then cross-referencing detected anomalies with news articles, official accident reports, and public records, the system can either confirm, partially link, or flag a finding for further human investigation.

The final output of this project is a **structured, publicly accessible dataset** containing:
- GPS coordinates of detected anomalies
- The classified crash type
- Matched news articles or reports (if found)
- A confidence and categorisation label
- Metadata about the detection event

This project is **not** intended to be a finished production system. It is an architectural blueprint and a starting point for researchers, developers, and ML engineers who want to build something genuinely impactful.

---

## 2. Goals & Non-Goals

### Goals
- Define a complete, reproducible pipeline from raw satellite imagery to a labelled output dataset.
- Train a classification and detection model on a curated dataset of known crash site imagery.
- Describe a scalable method for scanning large areas of satellite imagery for anomalies.
- Automate the cross-referencing of detected anomalies with publicly available news and incident reports.
- Produce a well-structured, open dataset that other researchers can use or build upon.
- Provide clear contribution guidelines so the community can extend this work.

### Non-Goals
- This project does **not** aim to replace official investigation bodies (NTSB, AAIB, coast guards, etc.).
- This project does **not** intend to process private or restricted satellite data without authorisation.
- This project does **not** aim to produce results with legal authority or evidentiary weight.
- This project does **not** involve real-time monitoring (at this stage).
- Identifying individuals, survivors, or human remains is explicitly **out of scope**.

---

## 3. Terminology & Definitions

| Term | Definition |
|---|---|
| **Anomaly** | A region of a satellite image flagged by the model as potentially containing crash-related visual patterns. |
| **Detection** | A confirmed model output identifying an anomaly with a class label and confidence score. |
| **Class** | The type of crash/accident event the model assigns to a detection (e.g., `PLANE_FOREST`, `SHIP_UNDERWATER`). |
| **Cross-reference** | The process of searching news and report databases for events matching the class, location, and estimated timeframe of a detection. |
| **Match** | A news article or report that is geographically and temporally consistent with a detection. |
| **Confidence Score** | A float (0.0–1.0) indicating the model's certainty in a given detection. |
| **Search Radius** | The maximum geographic distance used when searching for related news reports, which varies by crash class. |
| **Output Dataset** | The final structured file(s) containing all detections, their metadata, and any matched reports. |

---

## 4. System Architecture (High-Level)

The pipeline consists of six sequential phases:

```
[ Phase 1 ]          [ Phase 2 ]          [ Phase 3 ]
  Dataset      →     Model Train    →     Global Scan
  Assembly           & Validation         Pipeline
                                               ↓
[ Phase 6 ]          [ Phase 5 ]          [ Phase 4 ]
  Human        ←     Output Dataset ←    News Cross-Ref
  Review UI          Construction         Engine
```

Each phase is designed to be modular. Contributors can work on any single phase independently without requiring the entire system to be operational.

---

## 5. Phase 1 — Dataset Construction

### 5.1 Objective
Construct a labelled training and validation dataset of satellite images containing known crash or accident sites, as well as negative examples (similar-looking but non-crash environments).

### 5.2 Crash Classes (Initial Set)
The model must be trained to recognise the following distinct classes. Each class has its own visual signature at satellite resolution:

| Class ID | Class Label | Description |
|---|---|---|
| 01 | `PLANE_FOREST` | Commercial or private aircraft crashed into forested terrain, visible as a clearing, burn scar, debris trail, or scattered wreckage among trees. |
| 02 | `PLANE_WATER` | Aircraft that has impacted a body of water and is either partially submerged, floating as debris, or visible on the surface. |
| 03 | `PLANE_OPEN_TERRAIN` | Aircraft that has crashed on open ground, desert, tundra, or farmland — where the wreckage is visible on the surface. |
| 04 | `SHIP_SHALLOW_WATER` | A ship or large vessel visible on the seabed or partially submerged in shallow coastal waters, visible from satellite due to water transparency. |
| 05 | `SHIP_REEF_COASTAL` | Vessels that have run aground on reefs or coastlines and are at least partially above water or clearly visible through shallow surf. |
| 06 | `CAR_SUBMERGED` | Vehicles submerged in lakes, rivers, or ponds — recognisable by the shadow or outline of the vehicle visible through relatively still, clear water. |
| 07 | `CAR_CLIFF_RAVINE` | Vehicles that have gone off a cliff or into a ravine, potentially visible as debris or as a disturbance at the cliff base. |
| 08 | `TRAIN_DERAILMENT` | A train that has derailed and whose carriages are visible off the tracks, either on embankments, in water, or in terrain. |
| 09 | `HELICOPTER_CRASH` | Smaller rotorcraft wreckage, often identifiable by rotor blade debris spread pattern, in open terrain, forests, or hillsides. |
| 10 | `MILITARY_WRECK` | Historical or recent military aircraft or vehicle wrecks visible in accessible terrain, deserts, jungles, or shallow coastal areas. |

> **Contributor Note:** Additional classes can be proposed by opening a GitHub Issue with the label `class-proposal`. Any new class must include at minimum 50 labelled sample images before it is added to training.

### 5.3 Data Sources for Training Images
The following sources should be used to gather known, labelled crash site imagery:

- **Google Earth Pro** — Manual identification and export of known crash sites.
- **Sentinel-2 (via Copernicus Open Access Hub)** — Free, 10m resolution multispectral satellite data.
- **Landsat 8/9 (via USGS EarthExplorer)** — Free, 30m resolution imagery, good for large wrecks.
- **Maxar Open Data Program** — Higher resolution imagery, available for some disaster events.
- **Aviation Safety Network (ASN) Database** — Contains GPS-referenced crash locations that can be used to pull imagery.
- **Wikimedia Commons / Wikipedia crash articles** — Many major crashes have published aerial or satellite photographs.
- **NOAA Wrecks and Obstructions Database** — For known shipwreck coordinates.
- **NASA Earthdata** — Additional multispectral and SAR data.

### 5.4 Dataset Composition Requirements
- **Minimum images per class:** 200 positive samples, 200 hard negative samples (visually similar but not a crash — e.g., a boat anchor, a forest clearing, a lake shadow).
- **Resolution:** All images standardised to 512×512 pixels at a representative ground sampling distance (GSD) of 0.5m–10m depending on class size.
- **Annotation format:** COCO JSON or YOLO `.txt` bounding box annotations.
- **Train / Val / Test split:** 70% / 15% / 15%.
- **Augmentation:** Rotation (0°, 90°, 180°, 270°), horizontal flip, brightness and contrast jitter, Gaussian noise, random crop — applied during training only, not to the val/test sets.

### 5.5 Labelling Protocol
- Annotators must draw **tight bounding boxes** around the crash site or anomaly.
- Each image must receive a class label and an annotator confidence flag: `HIGH`, `MEDIUM`, or `LOW`.
- Images with `LOW` confidence require a second annotator review before being included in training.
- All annotations must be reviewed against a **labelling guideline document** (to be created per class in `/docs/labelling_guides/`).

---

## 6. Phase 2 — Model Design & Training

### 6.1 Objective
Train a computer vision model that can reliably detect and classify crash anomalies in satellite imagery, with an acceptable false positive rate, given the constraints of real-world satellite image variability.

### 6.2 Recommended Model Architecture
Given that this is an object detection task operating on small, sometimes ambiguous targets:

- **Primary recommendation:** YOLOv8 (Ultralytics) or YOLOv9 — fast, well-documented, supports transfer learning from COCO weights.
- **Alternative for higher accuracy:** DETR (Detection Transformer) — better at detecting small objects in complex backgrounds but slower to train.
- **Baseline for comparison:** EfficientDet-D4 — good accuracy-to-compute ratio.

All model choices should support export to ONNX for portability.

### 6.3 Transfer Learning Strategy
- Start from weights pretrained on **COCO** (which includes aerial/overhead scene classes).
- Fine-tune on the crash site dataset described in Phase 1.
- Freeze backbone layers for the first 10 epochs; unfreeze and continue for a further 20–40 epochs.
- Use cosine annealing learning rate schedule.

### 6.4 Training Configuration (Suggested Starting Point)
```yaml
model: yolov8m.pt           # Medium variant — balance of speed and accuracy
epochs: 50
batch_size: 16
image_size: 512
optimizer: AdamW
lr0: 0.001
lrf: 0.01
weight_decay: 0.0005
augment: true
conf_threshold: 0.40        # Detection confidence threshold
iou_threshold: 0.45         # NMS IoU threshold
```

### 6.5 Evaluation Metrics
The model must be evaluated against the following metrics on the held-out test set before being approved for the scanning pipeline:

- **mAP@0.5** (mean Average Precision at IoU=0.5) — target ≥ 0.60
- **mAP@0.5:0.95** — target ≥ 0.40
- **Per-class Recall** — target ≥ 0.55 for all classes
- **False Positive Rate** — must be documented per class; no class may exceed 40% FPR on the test set
- **Confusion Matrix** — must be published in the model release notes

### 6.6 Model Versioning
- All trained model weights must be tagged with a version number and stored in `/models/`.
- Each model version must have an accompanying `model_card.md` describing training data, performance metrics, known failure modes, and intended use.

---

## 7. Phase 3 — Global Satellite Scan Pipeline

### 7.1 Objective
Apply the trained model systematically to satellite imagery covering the Earth's land and accessible coastal/shallow water surface area to identify potential crash anomalies.

### 7.2 Imagery Source for Scanning
Due to the scale of this task and API limitations, the following approach is recommended:

- **Google Earth Engine (GEE)** — The primary platform for large-scale satellite image access and processing. GEE provides programmatic access to Sentinel-2, Landsat, and other datasets. A free research account is available at [https://earthengine.google.com/](https://earthengine.google.com/).
- **Copernicus Data Space** — An alternative large-scale source for Sentinel-2 imagery.
- **OpenAerialMap** — For higher-resolution imagery where available.

> **Important:** This pipeline does **not** involve scraping or unauthorised access to Google Maps or Google Satellite imagery. All imagery access must be through official APIs or open datasets with appropriate terms of service.

### 7.3 Scan Grid Strategy
The Earth cannot be scanned uniformly in a single pass at high resolution. A **tiered, priority-based scanning approach** is recommended:

**Tier 1 — High-Priority Zones (scan first):**
- Coastlines and shallow sea areas (within 50km of shoreline) — for ship and submerged vehicle classes.
- Known high-traffic aviation corridors and remote landing zones — for aircraft classes.
- Major road and railway networks in remote/mountainous regions — for vehicle and train classes.
- Historical conflict zones where military wrecks are more prevalent.

**Tier 2 — Secondary Zones:**
- Inland lakes and rivers above a minimum surface area.
- Forested regions near known airports or flight paths.
- Remote roads with low population density (higher chance of unreported accidents).

**Tier 3 — Deprioritised Zones (scan last or skip v1.0):**
- Dense urban areas (low probability of undetected crashes, high false-positive noise from infrastructure).
- Polar regions (limited imagery, low road/flight density).
- Open ocean beyond continental shelves (beyond current model capability).

### 7.4 Tile Processing
1. Divide the scan zone into overlapping tiles of **512×512 pixels** with a **10% overlap** to prevent edge-detection misses.
2. For each tile, run inference using the trained model.
3. Apply **Non-Maximum Suppression (NMS)** across overlapping tiles to merge duplicate detections.
4. Detections with confidence score below the minimum threshold (default: 0.40) are discarded.
5. Detections above threshold are saved to a **raw detections database** with the following fields:
   - `detection_id` (UUID)
   - `latitude`, `longitude` (centroid of bounding box)
   - `bounding_box` (lat/lon corners)
   - `class_label`
   - `confidence_score`
   - `imagery_source`
   - `imagery_date` (date of the satellite image used)
   - `tile_id`
   - `scan_date`

### 7.5 Handling Temporal Ambiguity
Satellite images are not always from the same date, and some crash sites may now be partially cleared or overgrown. The system must:
- Record the **date of the satellite image** used for each detection (not just the scan date).
- Flag detections where the imagery is older than 5 years as `IMAGERY_AGED`.
- Where multiple passes of an area exist at different dates, compare detections across dates to check for consistency.

---

## 8. Phase 4 — News & Report Cross-Reference Engine

### 8.1 Objective
For each detection produced by Phase 3, automatically search publicly available news archives, official incident databases, and regional news sources to find any reports that plausibly correspond to the detected anomaly.

### 8.2 Search Radius by Class
The geographic search radius for news matching must reflect the realistic reporting distance for each class:

| Class | Search Radius | Reasoning |
|---|---|---|
| `PLANE_FOREST` | 200 km | Regional and national news typically covers aviation incidents; remote areas may only appear in regional sources. |
| `PLANE_WATER` | 500 km | Maritime and aviation incidents at sea are reported nationally and internationally. |
| `PLANE_OPEN_TERRAIN` | 200 km | Similar to forested terrain; remote areas may be under-reported. |
| `SHIP_SHALLOW_WATER` | 300 km | Maritime incidents in coastal zones are covered regionally and nationally. |
| `SHIP_REEF_COASTAL` | 300 km | Same as above. |
| `CAR_SUBMERGED` | 50 km | Vehicle incidents are local news; unlikely to be covered beyond the immediate region. |
| `CAR_CLIFF_RAVINE` | 50 km | Same as above. |
| `TRAIN_DERAILMENT` | 150 km | Train incidents are regional or national news depending on severity. |
| `HELICOPTER_CRASH` | 200 km | Aviation incidents with a smaller footprint; regional coverage likely. |
| `MILITARY_WRECK` | 500 km | Historical wrecks may be covered nationally or internationally; may have historical records rather than news. |

### 8.3 Search Sources
The cross-reference engine should query the following:

**News Archives:**
- **NewsAPI** (`https://newsapi.org`) — Access to thousands of global news sources with keyword and location filtering.
- **GDELT Project** (`https://www.gdeltproject.org`) — Monitors news across the globe; supports geographic and event-type queries; free.
- **MediaStack API** — Alternative to NewsAPI with broader geographic coverage.
- **Internet Archive / Wayback Machine** — For older news articles that may no longer be hosted.

**Official Incident Databases:**
- **Aviation Safety Network (ASN)** — Searchable database of aviation accidents worldwide.
- **NTSB Aviation Accident Database** (USA) — `https://www.ntsb.gov/Pages/AviationQuery.aspx`
- **AAIB Reports** (UK) — `https://www.gov.uk/aaib-reports`
- **IMO GISIS Database** (maritime incidents) — `https://gisis.imo.org`
- **NOAA Wrecks & Obstructions** — For known shipwrecks with coordinates.
- **ICAO Accident/Incident Database** — For international aviation events.

### 8.4 Search Query Construction
For each detection, a structured query is assembled:

```python
query = {
    "keywords": [class_label_to_keywords(class_label)],   # e.g., ["plane crash", "aircraft wreck", "aviation accident"]
    "location": {
        "lat": detection.latitude,
        "lon": detection.longitude,
        "radius_km": search_radius[class_label]
    },
    "date_range": {
        "earliest": detection.imagery_date - timedelta(days=3650),  # 10 years before image
        "latest": detection.imagery_date + timedelta(days=365)      # 1 year after image
    }
}
```

> The wide date window accounts for the fact that crash sites can persist visually for years or decades. The date range should be tightened progressively as confidence increases.

### 8.5 Match Scoring
Each candidate news article or report is scored against the detection using the following criteria:

| Criterion | Weight | Method |
|---|---|---|
| Geographic proximity | 40% | Distance from detection centroid to the article's reported location (where available). Closer = higher score. |
| Event type alignment | 30% | NLP keyword match between the article text and the class label's keyword list. |
| Date plausibility | 20% | Whether the article date falls within the detection's plausible event window. |
| Source credibility | 10% | Known official sources (NTSB, ASN, IMO) score higher than unverified blogs. |

A combined match score between 0.0 and 1.0 is assigned. Articles scoring above **0.60** are considered candidate matches.

### 8.6 NLP Tools for Article Processing
- **spaCy** or **HuggingFace Transformers** — For named entity recognition (NER) to extract location names, dates, and vehicle types from article text.
- **GeoPy** or **Nominatim** — For converting location mentions in articles to GPS coordinates.
- **Sentence-BERT** — For semantic similarity between article descriptions and class keywords.

---

## 9. Phase 5 — Output Dataset & Categorisation Schema

### 9.1 Objective
Produce a structured, clean, open dataset that aggregates all detections, their cross-referenced reports, and their confidence-based categorisation labels, in a format that is immediately usable by other researchers.

### 9.2 Categorisation Labels
Every detection entry in the output dataset must receive one of the following top-level category labels:

| Label | Criteria | Description |
|---|---|---|
| `CONFIRMED_MATCH` | Match score ≥ 0.85 AND official source found | A detection that has a high-confidence corresponding official incident report. |
| `PROBABLE_MATCH` | Match score 0.60–0.84 OR credible news found | A detection with a plausible corresponding news or incident report. |
| `POSSIBLE_MATCH` | Match score 0.30–0.59 OR indirect news found | A detection where a loosely related report exists in the area and time range. |
| `NO_MATCH_FOUND` | Match score < 0.30 AND no relevant report found | A detection where the scan found something visually consistent but no report of any kind was located. This does not mean the detection is wrong — it may represent an undocumented event. |
| `FALSE_POSITIVE` | Human reviewer determined non-crash | A detection that was reviewed by a human and determined to be a visual artefact, misidentification, or natural feature. |
| `NEEDS_REVIEW` | Conflicting match signals or low model confidence | A detection that could not be cleanly categorised automatically and requires human examination. |

### 9.3 Output Dataset Schema
The final dataset is stored as a **Parquet file** (for efficiency) with a **CSV export** for accessibility. Each row represents a single detection event.

```
Field Name              Type        Description
─────────────────────────────────────────────────────────────────────
detection_id            UUID        Unique identifier
class_label             string      One of the 10 defined crash classes
model_confidence        float       0.0–1.0, model's confidence score
latitude                float       Centroid latitude of detection
longitude               float       Centroid longitude of detection
bounding_box_geojson    string      GeoJSON polygon of detection bounding box
country_code            string      ISO 3166-1 alpha-2 country code
region_name             string      Approximate region or state/province name
imagery_source          string      Dataset used (e.g., "Sentinel-2")
imagery_date            date        Date of the satellite image
scan_date               date        Date the model ran on this tile
match_score             float       Best news/report match score (0.0–1.0)
category_label          string      One of the 6 category labels above
matched_article_url     string      URL of best-matching news article (if any)
matched_article_title   string      Title of best-matching article (if any)
matched_article_date    date        Publication date of matched article (if any)
matched_source_type     string      "official_report" | "news" | "none"
matched_source_name     string      Name of the database or outlet
notes                   string      Free-text notes from human reviewers
human_reviewed          boolean     Whether a human has reviewed this entry
human_verdict           string      Human reviewer's label (if reviewed)
flagged_for_action      boolean     Whether this detection has been escalated
```

### 9.4 Dataset Release Cadence
- **v0.1** — First release: scan of one geographic region (suggested: Mediterranean coast or Southeast Asia) for initial validation.
- **v0.5** — Expanded scan covering one full continent.
- **v1.0** — Global scan (Tier 1 zones complete).
- All releases published to the project's GitHub Releases and optionally mirrored on **Hugging Face Datasets** (`datasets` library compatible format).

---

## 10. Phase 6 — Validation & Human Review Interface

### 10.1 Objective
Provide a simple, browser-based tool that allows human contributors to review model detections, inspect the satellite imagery, read matched articles, and assign a final verdict.

### 10.2 Interface Requirements
The review interface must display:
- The satellite image tile with the detection bounding box overlaid.
- The class label and model confidence score.
- The matched news article (if any), including title, source, date, and a link.
- The current category label assigned automatically.
- Buttons for the reviewer to: `Confirm`, `Mark False Positive`, `Reclassify`, `Escalate`, or `Skip`.
- A free-text notes field.

### 10.3 Implementation Options
- **Lightweight web app:** FastAPI (backend) + React or vanilla HTML/JS (frontend). Can be run locally.
- **Label Studio:** An open-source data labelling tool that can be configured for this review task without writing a custom interface.
- **Streamlit:** The fastest option to prototype; suitable for early-stage review.

### 10.4 Reviewer Access
- Any GitHub contributor can apply to become a reviewer.
- Reviewers must complete a brief calibration task (reviewing 10 pre-labelled examples) to confirm they understand the criteria.
- Reviewers' verdicts are logged with their GitHub username and timestamp for traceability.
- Conflicts between reviewers on the same entry are escalated to a maintainer.

---

## 11. Technology Stack (Suggested)

| Component | Suggested Tool | Alternative |
|---|---|---|
| Model Training | PyTorch + Ultralytics YOLOv8 | TensorFlow + EfficientDet |
| Satellite Data Access | Google Earth Engine Python API | Sentinel Hub API |
| Image Processing | OpenCV, rasterio, GDAL | Pillow, scikit-image |
| Geospatial Operations | GeoPandas, Shapely, PyProj | QGIS (manual) |
| News Retrieval | NewsAPI, GDELT Python client | BeautifulSoup scraping |
| NLP / Entity Extraction | spaCy, HuggingFace Transformers | NLTK |
| Database | PostgreSQL + PostGIS | SQLite with SpatiaLite |
| Dataset Storage | Parquet (via Pandas/Polars) | CSV, HDF5 |
| Review Interface | Streamlit or Label Studio | FastAPI + React |
| Experiment Tracking | Weights & Biases (W&B) | MLflow |
| Containerisation | Docker + Docker Compose | Conda environments |
| CI/CD | GitHub Actions | None (manual) |

---

## 12. Ethical Considerations & Legal Constraints

These must be read and understood by all contributors before participating.

### 12.1 Privacy
- This project does not seek to identify individuals.
- If any detection is found to be in a context where identification of a person could be possible (e.g., a very recent event), that detection must be immediately flagged as `NEEDS_REVIEW` and not published until reviewed by a maintainer.
- No imagery or data that is not publicly available through official open data programmes will be used.

### 12.2 Use of Satellite Imagery
- All imagery must be accessed through platforms and APIs that permit programmatic access for research purposes.
- **Do not** use imagery downloaded in violation of Google Maps Platform Terms of Service.
- Sentinel-2 and Landsat data are freely available under open licences and are the recommended sources.

### 12.3 Reporting Obligations
- If the project produces a detection that appears to represent a **recent, active emergency** (evidence of a crash that may have occurred in the past 72 hours), contributors should escalate this to maintainers immediately. Maintainers will evaluate whether relevant authorities should be notified.
- The project does not have the resources or authority to conduct search and rescue operations. However, in cases where a finding is highly credible and appears to represent an unregistered event, the responsible course of action is to notify the appropriate national authority (e.g., the relevant aviation authority or coast guard) and document that this was done.

### 12.4 Misuse Prevention
- The output dataset must not be used to support illegal activity.
- The project is not intended to identify the location of military assets or sensitive infrastructure.
- A `SECURITY.md` file must be maintained in the repository instructing contributors on how to report sensitive findings.

---

## 13. Folder & Repository Structure

```
crashsight-ai/
│
├── README.md                        # Project overview and quick-start
├── CONTRIBUTING.md                  # Contribution guidelines
├── CODE_OF_CONDUCT.md               # Community standards
├── SECURITY.md                      # How to report sensitive findings
├── LICENSE                          # MIT or Apache 2.0
│
├── data/
│   ├── raw/                         # Raw downloaded satellite tiles (gitignored)
│   ├── processed/                   # Preprocessed, normalised tiles
│   ├── annotations/                 # COCO/YOLO annotation files
│   └── output_dataset/              # Final detection + cross-ref dataset
│       ├── detections_v0.1.parquet
│       └── detections_v0.1.csv
│
├── docs/
│   ├── architecture.md              # Full pipeline description (this document)
│   ├── labelling_guides/            # Per-class image labelling instructions
│   │   ├── PLANE_FOREST.md
│   │   ├── SHIP_SHALLOW_WATER.md
│   │   └── ...
│   └── model_cards/                 # Model version documentation
│
├── models/
│   ├── weights/                     # Trained model weights (gitignored, stored in releases)
│   └── configs/                     # Training configuration YAML files
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_training.ipynb
│   ├── 03_scan_pipeline_demo.ipynb
│   └── 04_cross_reference_demo.ipynb
│
├── src/
│   ├── dataset/
│   │   ├── downloader.py            # Imagery download utilities
│   │   ├── tile_generator.py        # Tile splitting and overlap logic
│   │   └── augmentation.py          # Training augmentation pipeline
│   │
│   ├── model/
│   │   ├── train.py                 # Training entry point
│   │   ├── evaluate.py              # Evaluation and metrics
│   │   └── predict.py               # Inference on new tiles
│   │
│   ├── scanner/
│   │   ├── grid_generator.py        # Scan grid construction
│   │   ├── scan_runner.py           # Batch inference over scan grids
│   │   └── nms_merger.py            # Cross-tile NMS
│   │
│   ├── crossref/
│   │   ├── news_fetcher.py          # NewsAPI / GDELT queries
│   │   ├── official_db_fetcher.py   # ASN, NTSB, IMO queries
│   │   ├── match_scorer.py          # Match scoring logic
│   │   └── nlp_utils.py             # NER, semantic similarity
│   │
│   ├── dataset_builder/
│   │   ├── schema.py                # Output dataset schema definitions
│   │   └── builder.py               # Assembles final output dataset
│   │
│   └── review_ui/
│       ├── app.py                   # Streamlit review interface
│       └── components/
│
├── tests/
│   ├── test_model.py
│   ├── test_crossref.py
│   └── test_dataset_builder.py
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
└── .github/
    ├── workflows/
    │   ├── ci.yml                   # Lint, test on push
    │   └── model_eval.yml           # Model evaluation on PR to main
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   ├── class_proposal.md
    │   └── data_source_proposal.md
    └── PULL_REQUEST_TEMPLATE.md
```

---

## 14. How to Publish on GitHub & Invite Contributors

Follow these steps in order to publish this project and build a contributor community.

### Step 1 — Prepare the Repository
1. Create a new GitHub repository named `crashsight-ai` (or your preferred name).
2. Set visibility to **Public**.
3. Initialise with a `README.md`.
4. Choose a licence — **MIT** is recommended for maximum openness. Apache 2.0 is also appropriate if you want patent protection clauses.

### Step 2 — Write the Core Documents
Before inviting contributors, these files must exist and be well-written:
- **`README.md`** — Explain what the project is, why it matters, what stage it is in, and how to get involved. Include a clear diagram or table of the pipeline. Add badges (build status, licence, Python version).
- **`CONTRIBUTING.md`** — Explain how to report bugs, propose changes, submit pull requests, and what the code review process looks like.
- **`CODE_OF_CONDUCT.md`** — Use the Contributor Covenant template (`https://www.contributor-covenant.org`). This is essential before the project goes public.
- **`SECURITY.md`** — Explain what to do if a contributor finds a sensitive detection or a security vulnerability.

### Step 3 — Set Up GitHub Issues as Your Contribution Board
Create the following **Issue Labels** in your repository settings:
- `good first issue` — For simple, self-contained tasks suitable for new contributors.
- `help wanted` — For tasks where you actively want community input.
- `class-proposal` — For proposing new crash class types.
- `data-source` — For proposing new imagery or report sources.
- `model-improvement` — For architecture or training suggestions.
- `bug` — For defects in existing code or data.
- `documentation` — For improvements to docs and guides.
- `review-queue` — For tracking human review tasks.

Immediately after publishing, create **5–10 starter issues** with `good first issue` so that new visitors have something actionable to do.

### Step 4 — Create a GitHub Project Board
Use GitHub Projects (the Kanban-style board feature) to track work across phases:
- Columns: `Backlog` → `In Progress` → `In Review` → `Done`
- Assign issues to phases (Phase 1, Phase 2, etc.) using Milestones.

### Step 5 — Publish to the Community
Once the repository is ready with at minimum a clear README, CONTRIBUTING guide, and a handful of open issues:
- Post to **Reddit**: `/r/MachineLearning`, `/r/computervision`, `/r/datasets`, `/r/geospatial`
- Post to **HuggingFace Community** forums.
- Submit to **Papers With Code** once any model is trained and evaluated.
- Cross-post on **LinkedIn** (relevant communities: AI/ML, Remote Sensing, GIS).
- Consider writing a brief post on **Dev.to** or **Medium** explaining the concept and inviting collaborators.

### Step 6 — Host the Dataset
When the first version of the output dataset is ready:
- Publish it to **Hugging Face Datasets** (`https://huggingface.co/datasets`) — this provides versioning, a dataset viewer, and wide discoverability.
- Mirror the CSV version in GitHub Releases.
- Write a `dataset_card.md` following HuggingFace's template, describing the data, its limitations, and intended use.

### Step 7 — Ongoing Community Maintenance
- Respond to all Issues and Pull Requests within **72 hours** where possible.
- Tag reliable contributors as **Collaborators** after they have made meaningful contributions.
- Publish a brief `CHANGELOG.md` with every new dataset or model release.
- Hold periodic **"contribution sprints"** via GitHub Discussions where the community focuses on a specific task (e.g., labelling a new class, reviewing a batch of detections).

---

## 15. Roadmap & Open Questions

### Immediate Priorities (v0.1 milestone)
- [ ] Collect and annotate 200 positive samples for at least 3 crash classes.
- [ ] Train a baseline YOLOv8m model and publish the model card.
- [ ] Build a minimal scan pipeline covering one coastal region.
- [ ] Implement a basic NewsAPI cross-reference query for `PLANE_FOREST` class.
- [ ] Publish the first output dataset (even if small) to establish format.

### Medium-Term Goals (v0.5 milestone)
- [ ] All 10 crash classes with full annotation sets.
- [ ] Full Tier 1 scan complete for one continent.
- [ ] Human review interface deployed and tested.
- [ ] Output dataset published on Hugging Face.

### Long-Term Vision (v1.0 and beyond)
- [ ] Global Tier 1 scan complete.
- [ ] Integration with Change Detection to flag new anomalies over time.
- [ ] Automated alerting pipeline for high-confidence recent detections.
- [ ] Multilingual news cross-referencing to improve coverage in non-English regions.
- [ ] Community-maintained labelling portal for continuous dataset expansion.

### Open Questions for Community Discussion
1. **What is the acceptable false positive rate for a "published" detection?** This is a significant ethical question given the sensitive nature of some crash sites.
2. **Should the system attempt to estimate the age of a wreck** based on vegetation regrowth, rust patterns, or debris scatter? This would improve matching accuracy but adds significant complexity.
3. **How should indigenous land rights and cultural heritage be handled** when a detected site falls within protected areas?
4. **Is there a viable path to using commercial satellite imagery** (Planet Labs, Maxar) under a research licence?
5. **Should the project scope include detecting crash sites in urban environments**, or does the noise-to-signal ratio make this infeasible at this stage?

---

*This document was written as an open architectural specification. It is intended to evolve through community contribution. If you have suggestions, corrections, or additions, please open an Issue or a Pull Request.*

*Last updated: 2026*
