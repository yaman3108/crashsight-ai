"""
Training data augmentation pipeline for CrashSight AI.

Augmentations applied during training only:
- Rotation (0°, 90°, 180°, 270°)
- Horizontal flip
- Brightness and contrast jitter
- Gaussian noise
- Random crop

See: docs/architecture.md § 5.4
"""

# TODO: Implement augmentation pipeline using albumentations or torchvision
