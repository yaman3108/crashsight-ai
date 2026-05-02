"""
Streamlit-based human review interface for CrashSight AI.

Displays detections with satellite imagery, matched articles,
and buttons for reviewers to confirm/reject/reclassify.

See: docs/architecture.md § 10

Run with:
    streamlit run src/review_ui/app.py
"""

# TODO: Display satellite tile with bounding box overlay
# TODO: Show class label and confidence score
# TODO: Show matched article (title, source, date, link)
# TODO: Reviewer action buttons: Confirm, Mark False Positive, Reclassify, Escalate, Skip
# TODO: Free-text notes field
# TODO: Log reviewer username and timestamp
