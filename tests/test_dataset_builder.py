"""Tests for the CrashSight AI output dataset builder."""

from src.dataset_builder.schema import CATEGORY_LABELS, CLASS_LABELS


def test_category_labels_count():
    """Verify we have exactly 6 category labels."""
    assert len(CATEGORY_LABELS) == 6


def test_class_labels_count():
    """Verify we have exactly 10 crash classes."""
    assert len(CLASS_LABELS) == 10
