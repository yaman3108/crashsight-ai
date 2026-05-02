"""
Tile splitting and overlap logic for CrashSight AI.

Splits large satellite images into 512x512 tiles with configurable overlap
for model inference. Handles geo-referencing so tile coordinates map back
to real-world lat/lon.

See: docs/architecture.md § 7.4 (Tile Processing)
"""

# TODO: Implement tile splitting with 10% overlap
# TODO: Maintain geo-reference metadata per tile
# TODO: Support multiple input formats (GeoTIFF, JP2)
