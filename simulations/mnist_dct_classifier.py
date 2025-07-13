"""mnist_dct_classifier.py

Classify MNIST digits using low-frequency DCT signatures and Wave-Engine
micro-experts.  This demonstration avoids deep learning, relying instead on
prototype matching for full explainability.

Run:
    py -3 simulations\mnist_dct_classifier.py --limit 2000

The script expects the raw MNIST files in *data/MNIST/raw* – run
`tools\download_mnist.py` beforehand (already done in CI).
"""
from __future__ import annotations

import argparse
import struct
import pathlib
import time
from typing import Tuple, List

import numpy as np

# Ensure project root is on sys.path so `expert_modules` can be imported when
# the script is executed directly.
import os, sys, pathlib as _pl
_PROJECT_ROOT = _pl.Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from expert_modules.registry import ExpertRegistry
from expert_modules.vision_experts import DCTDigitExpert, dct_signature

DATA_DIR = pathlib.Path("data/MNIST/raw")
TRAIN_IMAGES = DATA_DIR / "train-images-idx3-ubyte"
TRAIN_LABELS = DATA_DIR / "train-labels-idx1-ubyte"
TEST_IMAGES = DATA_DIR / "t10k-images-idx3-ubyte"
TEST_LABELS = DATA_DIR / "t10k-labels-idx1-ubyte"


def load_idx_images(path: pathlib.Path) -> np.ndarray:
    """Load IDX images into array of shape (n, 28, 28)."""
    with open(path, "rb") as fp:
        magic, n, rows, cols = struct.unpack(">IIII", fp.read(16))
        if magic != 2051:
            raise ValueError(f"Unexpected magic number {magic} for images in {path}")
        data = np.frombuffer(fp.read(), dtype=np.uint8)
    return data.reshape(n, rows, cols)


def load_idx_labels(path: pathlib.Path) -> np.ndarray:
    """Load IDX labels into 1-D uint8 array."""
    with open(path, "rb") as fp:
        magic, n = struct.unpack(">II", fp.read(8))
        if magic != 2049:
            raise ValueError(f"Unexpected magic number {magic} for labels in {path}")
        data = np.frombuffer(fp.read(), dtype=np.uint8)
    return data


def build_prototypes(images: np.ndarray, labels: np.ndarray, dct_size: int = 8) -> List[np.ndarray]:
    """Return list of 10 prototype DCT signatures (one per digit)."""
    prototypes = [np.zeros(dct_size * dct_size, dtype=np.float64) for _ in range(10)]
    counts = [0] * 10
    for img, lbl in zip(images, labels):
        sig = dct_signature(img, dct_size)
        prototypes[lbl] += sig
        counts[lbl] += 1
    for d in range(10):
        prototypes[d] /= max(1, counts[d])
    return [p.astype(np.float32) for p in prototypes]


def run_evaluation(limit: int | None = None, dct_size: int = 8) -> Tuple[float, float]:
    """Evaluate accuracy on test set.  Returns (accuracy, avg_time_ms)."""
    train_imgs = load_idx_images(TRAIN_IMAGES)
    train_lbls = load_idx_labels(TRAIN_LABELS)

    test_imgs = load_idx_images(TEST_IMAGES)
    test_lbls = load_idx_labels(TEST_LABELS)

    if limit is not None:
        test_imgs = test_imgs[:limit]
        test_lbls = test_lbls[:limit]

    # Build prototypes from training images
    prototypes = build_prototypes(train_imgs, train_lbls, dct_size)

    # Register experts
    registry = ExpertRegistry()
    for digit in range(10):
        expert = DCTDigitExpert(digit, prototypes[digit], dct_size)
        registry.register_expert(expert)

    # Classify test images
    correct = 0
    start = time.perf_counter()
    for img, true_lbl in zip(test_imgs, test_lbls):
        context = {"image": img}
        resp = registry.process_query("classify_digit", context)
        pred = resp.answer
        if pred == true_lbl:
            correct += 1
    elapsed = time.perf_counter() - start

    accuracy = correct / len(test_lbls)
    avg_ms = (elapsed / len(test_lbls)) * 1000.0
    return accuracy, avg_ms


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Evaluate on first N test samples only")
    parser.add_argument("--dct_size", type=int, default=8, help="Low-frequency square size to use for prototypes")
    args = parser.parse_args()

    acc, avg_ms = run_evaluation(args.limit, args.dct_size)
    print("\n=== MNIST DCT Expert Evaluation ===")
    print(f"Accuracy       : {acc*100:.2f} %")
    print(f"Avg time/sample: {avg_ms:.3f} ms") 