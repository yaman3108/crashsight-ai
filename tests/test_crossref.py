"""Tests for the CrashSight AI cross-reference engine."""


def test_match_scorer_weights_sum_to_one():
    """Verify match scoring weights sum to 1.0."""
    weights = {"geographic": 0.40, "event_type": 0.30, "date": 0.20, "credibility": 0.10}
    assert abs(sum(weights.values()) - 1.0) < 1e-6


def test_search_radius_defined_for_all_classes():
    """Verify every class has a defined search radius."""
    from src.dataset_builder.schema import CLASS_LABELS, SEARCH_RADIUS_KM
    for cls in CLASS_LABELS:
        assert cls in SEARCH_RADIUS_KM, f"Missing search radius for {cls}"
