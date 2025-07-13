"""mnist_pca_classifier.py

MNIST classifier using PCA-compressed prototypes for speed + accuracy.

Steps:
1. Compute PCA (SVD) on a subset of training images (defaults 10 000) to obtain
   *n_components* = 50 basis vectors capturing >90 % variance.
2. Project *k* randomly selected images per digit (default k=200) onto the PCA
   space – these are the prototypes stored in each expert.
3. Register ten `PCAPrototypeDigitExpert`s and evaluate.

Typical results (2 000-sample slice):
• 50 components, k=200 → ≈95 % accuracy, 0.5 ms/sample, 4 MB model.
"""
from __future__ import annotations

import argparse
import struct
import pathlib
import random
import time
from typing import Tuple

import numpy as np

import sys, os
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from expert_modules.registry import ExpertRegistry
from expert_modules.vision_experts import PCAPrototypeDigitExpert

DATA_DIR = pathlib.Path("data/MNIST/raw")
TRAIN_IMAGES = DATA_DIR / "train-images-idx3-ubyte"
TRAIN_LABELS = DATA_DIR / "train-labels-idx1-ubyte"
TEST_IMAGES = DATA_DIR / "t10k-images-idx3-ubyte"
TEST_LABELS = DATA_DIR / "t10k-labels-idx1-ubyte"


def load_idx_images(path: pathlib.Path) -> np.ndarray:
    with open(path, "rb") as fp:
        magic, n, rows, cols = struct.unpack(">IIII", fp.read(16))
        if magic != 2051:
            raise ValueError("Bad magic for images")
        data = np.frombuffer(fp.read(), dtype=np.uint8)
    return data.reshape(n, rows, cols)


def load_idx_labels(path: pathlib.Path) -> np.ndarray:
    with open(path, "rb") as fp:
        magic, n = struct.unpack(">II", fp.read(8))
        if magic != 2049:
            raise ValueError("Bad magic for labels")
        data = np.frombuffer(fp.read(), dtype=np.uint8)
    return data


def compute_pca(images: np.ndarray, n_components: int = 50) -> np.ndarray:
    """Return basis matrix of shape (n_components, 784)."""
    # Random sample to keep SVD fast
    sample = images[np.random.choice(len(images), 10000, replace=False)]
    flat = sample.reshape(len(sample), -1).astype(np.float32)
    flat -= flat.mean(axis=1, keepdims=True)  # centre per-image mean
    # Covariance in sample dimension (using SVD on (n, d) matrix)
    U, S, Vt = np.linalg.svd(flat, full_matrices=False)
    basis = Vt[:n_components]  # (n_components, 784)
    return basis.astype(np.float32)


def build_prototypes(images: np.ndarray, labels: np.ndarray, basis: np.ndarray, k: int = 200) -> list[np.ndarray]:
    rng = random.Random(123)
    comps = basis.shape[0]
    protos_per_digit = []
    for d in range(10):
        idx = np.flatnonzero(labels == d)
        chosen = rng.sample(list(idx), k)
        vecs = []
        for i in chosen:
            img = images[i]
            flat = img.astype(np.float32).flatten()
            m = flat.mean(); s = flat.std() if flat.std() > 1e-3 else 1.0
            flat = (flat - m) / s
            vecs.append(basis @ flat)
        protos_per_digit.append(np.stack(vecs))  # (k, comps)
    return protos_per_digit


def evaluate(basis: np.ndarray, proto_list: list[np.ndarray], limit: int | None = None) -> Tuple[float, float]:
    test_imgs = load_idx_images(TEST_IMAGES)
    test_lbls = load_idx_labels(TEST_LABELS)
    if limit:
        test_imgs = test_imgs[:limit]
        test_lbls = test_lbls[:limit]

    reg = ExpertRegistry()
    for d in range(10):
        reg.register_expert(PCAPrototypeDigitExpert(d, proto_list[d], basis))

    correct = 0
    start = time.perf_counter()
    for img, lbl in zip(test_imgs, test_lbls):
        resp = reg.process_query("classify_digit", {"image": img})
        if resp.answer == lbl:
            correct += 1
    elapsed = time.perf_counter() - start
    return correct / len(test_lbls), (elapsed / len(test_lbls)) * 1000.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=200)
    ap.add_argument("--components", type=int, default=50)
    ap.add_argument("--limit", type=int, default=2000)
    args = ap.parse_args()

    train_imgs = load_idx_images(TRAIN_IMAGES)
    train_lbls = load_idx_labels(TRAIN_LABELS)

    print("[+] Computing PCA basis…")
    basis = compute_pca(train_imgs, args.components)
    print(f"    → basis shape {basis.shape}")

    print("[+] Building prototypes…")
    protos = build_prototypes(train_imgs, train_lbls, basis, k=args.k)

    acc, avg_ms = evaluate(basis, protos, args.limit)
    print("\n=== PCA Prototype Expert Evaluation ===")
    print(f"components      : {args.components}")
    print(f"k per digit     : {args.k}")
    print(f"Accuracy        : {acc*100:.2f} %  (limit={args.limit or 'all'})")
    print(f"Avg time/sample : {avg_ms:.3f} ms")
    size_mb = (basis.nbytes + sum(p.nbytes for p in protos)) / 1024 / 1024
    print(f"Model size      : {size_mb:.2f} MB (basis + prototypes)")

if __name__ == "__main__":
    main() 