"""
Output dataset schema definitions for CrashSight AI.

Defines the Parquet/CSV schema for the final detection dataset,
including all field types and validation rules.

See: docs/architecture.md § 9.3
"""

CATEGORY_LABELS = [
    "CONFIRMED_MATCH",   # match_score >= 0.85 AND official source
    "PROBABLE_MATCH",    # match_score 0.60-0.84 OR credible news
    "POSSIBLE_MATCH",    # match_score 0.30-0.59 OR indirect news
    "NO_MATCH_FOUND",    # match_score < 0.30 AND no report
    "FALSE_POSITIVE",    # human reviewer determined non-crash
    "NEEDS_REVIEW",      # conflicting signals or low confidence
]

CLASS_LABELS = [
    "PLANE_FOREST",
    "PLANE_WATER",
    "PLANE_OPEN_TERRAIN",
    "SHIP_SHALLOW_WATER",
    "SHIP_REEF_COASTAL",
    "CAR_SUBMERGED",
    "CAR_CLIFF_RAVINE",
    "TRAIN_DERAILMENT",
    "HELICOPTER_CRASH",
    "MILITARY_WRECK",
]

SEARCH_RADIUS_KM = {
    "PLANE_FOREST": 200,
    "PLANE_WATER": 500,
    "PLANE_OPEN_TERRAIN": 200,
    "SHIP_SHALLOW_WATER": 300,
    "SHIP_REEF_COASTAL": 300,
    "CAR_SUBMERGED": 50,
    "CAR_CLIFF_RAVINE": 50,
    "TRAIN_DERAILMENT": 150,
    "HELICOPTER_CRASH": 200,
    "MILITARY_WRECK": 500,
}

# TODO: Implement Pydantic or dataclass schema for output rows
# TODO: Implement Parquet writer with schema validation
# TODO: Implement CSV export
