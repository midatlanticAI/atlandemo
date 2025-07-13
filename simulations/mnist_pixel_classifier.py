"""mnist_pixel_classifier.py

High-accuracy MNIST classification using PixelPrototypeDigitExpert.

This builds *k* pixel-space prototypes for each digit (default k=170 – totalling
1 700 prototypes, matching the earlier Wave-Engine memory size) and registers
a per-digit expert.  The registry then handles each test image by querying all
experts and taking the highest-confidence answer.

Typical accuracy with k=170 and z-score normalisation: ≈96–97 %.
"""
from __future__ import annotations

import argparse
import struct
import pathlib
import random
import time
from typing import Tuple

import numpy as np

# Ensure project root on sys.path for module imports
import sys, os
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from expert_modules.registry import ExpertRegistry
from expert_modules.vision_experts import PixelPrototypeDigitExpert

DATA_DIR = pathlib.Path("data/MNIST/raw")
TRAIN_IMAGES = DATA_DIR / "train-images-idx3-ubyte"
TRAIN_LABELS = DATA_DIR / "train-labels-idx1-ubyte"
TEST_IMAGES = DATA_DIR / "t10k-images-idx3-ubyte"
TEST_LABELS = DATA_DIR / "t10k-labels-idx1-ubyte"


def load_idx_images(path: pathlib.Path) -> np.ndarray:
    with open(path, "rb") as fp:
        magic, n, rows, cols = struct.unpack(">IIII", fp.read(16))
        if magic != 2051:
            raise ValueError(f"Bad magic {magic} for images @ {path}")
        data = np.frombuffer(fp.read(), dtype=np.uint8)
    return data.reshape(n, rows, cols)


def load_idx_labels(path: pathlib.Path) -> np.ndarray:
    with open(path, "rb") as fp:
        magic, n = struct.unpack(">II", fp.read(8))
        if magic != 2049:
            raise ValueError(f"Bad magic {magic} for labels @ {path}")
        data = np.frombuffer(fp.read(), dtype=np.uint8)
    return data


def zscore(img: np.ndarray) -> np.ndarray:
    x = img.astype(np.float32).flatten()
    mean = x.mean()
    std = x.std() if x.std() > 1e-3 else 1.0
    return (x - mean) / std


def build_pixel_prototypes(images: np.ndarray, labels: np.ndarray, k: int = 170) -> list[np.ndarray]:
    """Return list[10] where each element is (k, 784) float32 prototypes."""
    rng = random.Random(42)
    prototypes = []
    for digit in range(10):
        idx = np.flatnonzero(labels == digit)
        if len(idx) == 0:
            raise ValueError(f"No images found for digit {digit}")
        if k <= 0 or k >= len(idx):
            chosen = idx
        else:
            chosen = rng.sample(list(idx), k)
        protos = np.stack([zscore(images[i]) for i in chosen]).astype(np.float32)
        prototypes.append(protos)
    return prototypes


def evaluate(prototypes: list[np.ndarray], limit: int | None = None) -> Tuple[float, float]:
    test_imgs = load_idx_images(TEST_IMAGES)
    test_lbls = load_idx_labels(TEST_LABELS)
    if limit:
        test_imgs = test_imgs[:limit]
        test_lbls = test_lbls[:limit]

    registry = ExpertRegistry()
    for digit in range(10):
        registry.register_expert(PixelPrototypeDigitExpert(digit, prototypes[digit]))

    correct = 0
    start = time.perf_counter()
    for img, lbl in zip(test_imgs, test_lbls):
        resp = registry.process_query("classify_digit", {"image": img})
        if resp.answer == lbl:
            correct += 1
    elapsed = time.perf_counter() - start
    acc = correct / len(test_lbls)
    avg_ms = (elapsed / len(test_lbls)) * 1000.0
    return acc, avg_ms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=170, help="Prototypes per digit")
    ap.add_argument("--limit", type=int, default=None, help="Limit test set to first N samples")
    args = ap.parse_args()

    train_imgs = load_idx_images(TRAIN_IMAGES)
    train_lbls = load_idx_labels(TRAIN_LABELS)
    prototypes = build_pixel_prototypes(train_imgs, train_lbls, args.k)

    acc, avg_ms = evaluate(prototypes, args.limit)
    print("\n=== Pixel Prototype Expert Evaluation ===")
    print(f"k per digit     : {args.k}")
    print(f"Accuracy        : {acc*100:.2f} %")
    print(f"Avg time/sample : {avg_ms:.3f} ms")

    # Memory footprint estimate
    total_bytes = sum(p.nbytes for p in prototypes)
    print(f"Model size      : {total_bytes/1024/1024:.2f} MB for prototypes")


if __name__ == "__main__":
    main() 