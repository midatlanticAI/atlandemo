"""
Vision Expert Modules for MNIST Digit Classification using DCT prototypes.

Each digit (0–9) is represented by a dedicated micro-expert that compares
an input image’s low-frequency DCT signature against a stored prototype and
outputs a confidence score.  No gradient training or deep nets are used –
a pure rule-based, explainable approach aligned with the Wave-Engine ethos.
"""

from __future__ import annotations

import time
from typing import Dict, Any
import numpy as np
from scipy.fftpack import dct

from .base_expert import BaseExpertModule, ExpertResponse

# -----------------------------------------------------------------------------
# Utility
# -----------------------------------------------------------------------------


def dct_signature(img: np.ndarray, k: int = 8) -> np.ndarray:
    """Return the top-left *k×k* 2-D DCT coefficients flattened.

    The MNIST image is first scaled to [0,1] and converted to float32.  We apply
    orthonormal DCT-II along rows then columns (same as JPEG) and take the
    lowest-frequency coefficients which capture coarse structure while being
    robust to noise.
    """
    if img.dtype != np.float32 and img.dtype != np.float64:
        img = img.astype(np.float32) / 255.0
    # 2-D DCT (rows then cols)
    coeffs = dct(dct(img, axis=0, norm="ortho"), axis=1, norm="ortho")
    return coeffs[:k, :k].flatten()


# -----------------------------------------------------------------------------
# Expert
# -----------------------------------------------------------------------------


class DCTDigitExpert(BaseExpertModule):
    """Rule-based expert for identifying a single MNIST digit class.

    Parameters
    ----------
    digit : int
        The digit (0–9) this expert represents.
    prototype : np.ndarray
        1-D array of reference DCT coefficients (length = k² where k is the
        *dct_size* used to build prototypes).
    dct_size : int
        The *k* used when generating *prototype*. Must match signatures at
        runtime.
    """

    def __init__(self, digit: int, prototype: np.ndarray, dct_size: int = 8):
        self.digit = digit
        self.prototype = prototype.astype(np.float32)
        self.dct_size = dct_size

        super().__init__(name=f"Digit{digit}Expert", domain="mnist_digit", version="1.0")

    # ------------------------------------------------------------------
    # BaseExpert hooks
    # ------------------------------------------------------------------

    def _define_wave_frequencies(self) -> Dict[str, float]:
        # Assign a unique but simple frequency for each digit expert
        return {f"digit_{self.digit}": 1.0 + 0.15 * self.digit}

    def can_handle(self, query: str, context: Dict[str, Any] | None = None) -> float:
        """Return a confidence estimate that this expert can answer *query*.

        For digit classification we compute similarity between the image’s
        DCT signature and our prototype; similarity is mapped to 0–1 range.
        """
        if query != "classify_digit" or context is None:
            return 0.0

        img = context.get("image")
        if img is None:
            return 0.0

        # Use cached signature if provided to avoid recomputation
        sig = context.get("dct_sig")
        if sig is None:
            sig = dct_signature(img, self.dct_size)

        # Euclidean distance between signatures
        dist = float(np.linalg.norm(sig - self.prototype))
        # Confidence via soft exponential decay so that smaller distances
        # yield values near 1 and typical distances (~5) yield ~0.4.
        confidence = float(np.exp(-dist / 5.0))
        return float(confidence)

    def process_query(self, query: str, context: Dict[str, Any] | None = None) -> ExpertResponse:
        if not context or "image" not in context:
            raise ValueError("DCTDigitExpert expects 'image' in context")

        start = time.perf_counter()
        img = context["image"]
        sig = context.get("dct_sig") or dct_signature(img, self.dct_size)

        dist = float(np.linalg.norm(sig - self.prototype))
        confidence = float(np.exp(-dist / 5.0))
        processing_time = time.perf_counter() - start

        reasoning = (
            f"DCT distance to digit {self.digit} prototype = {dist:.4f}; "
            f"confidence = {confidence:.3f}"
        )

        wave_patterns = self.generate_wave_patterns([f"digit_{self.digit}"], strength=confidence)

        return ExpertResponse(
            confidence=confidence,
            reasoning=reasoning,
            answer=self.digit,
            wave_patterns=wave_patterns,
            metadata={"distance": dist, "dct_size": self.dct_size},
            processing_time=processing_time,
        ) 


# -----------------------------------------------------------------------------
# Pixel-domain expert (high-accuracy)
# -----------------------------------------------------------------------------

class PixelPrototypeDigitExpert(BaseExpertModule):
    """Nearest-prototype expert operating directly in pixel space.

    Each instance owns *n_prototypes* training images for its digit class.
    Classification computes the minimal Euclidean distance between the input
    (optionally z-score normalised) and stored prototypes.  The expert is fully
    deterministic and requires no gradient training.
    """

    def __init__(self, digit: int, prototypes: np.ndarray):
        if prototypes.ndim != 2:
            raise ValueError("prototypes must be 2-D array [n_prototypes, 784]")
        self.digit = digit
        # Store as float32 for a balance between precision and memory
        self.prototypes = prototypes.astype(np.float32)
        super().__init__(name=f"PixelDigit{digit}Expert", domain="mnist_digit", version="1.0")

    # ------------------------------------------------------------------
    # BaseExpert hooks
    # ------------------------------------------------------------------

    def _define_wave_frequencies(self) -> Dict[str, float]:
        return {f"digit_{self.digit}_px": 2.0 + 0.12 * self.digit}

    def _normalise(self, img: np.ndarray) -> np.ndarray:
        """z-score normalise flattened pixels to reduce brightness bias."""
        x = img.astype(np.float32).flatten()
        mean = x.mean()
        std = x.std() if x.std() > 1e-3 else 1.0
        return (x - mean) / std

    def can_handle(self, query: str, context: Dict[str, Any] | None = None) -> float:
        if query != "classify_digit" or context is None or "image" not in context:
            return 0.0

        img = context["image"]
        x = self._normalise(img)
        # Vectorised distance computation
        dists = np.linalg.norm(self.prototypes - x, axis=1)
        dist = float(dists.min())
        confidence = float(np.exp(-dist / 40.0))  # scaling tuned empirically
        return confidence

    def process_query(self, query: str, context: Dict[str, Any] | None = None) -> ExpertResponse:
        if not context or "image" not in context:
            raise ValueError("PixelPrototypeDigitExpert expects 'image' in context")

        start = time.perf_counter()
        img = context["image"]
        x = self._normalise(img)
        dists = np.linalg.norm(self.prototypes - x, axis=1)
        dist = float(dists.min())
        confidence = float(np.exp(-dist / 40.0))
        processing_time = time.perf_counter() - start

        reasoning = (
            f"Min pixel distance to digit {self.digit} prototype = {dist:.1f}; "
            f"confidence = {confidence:.3f}"
        )
        waves = self.generate_wave_patterns([f"digit_{self.digit}_px"], strength=confidence)
        return ExpertResponse(
            confidence=confidence,
            reasoning=reasoning,
            answer=self.digit,
            wave_patterns=waves,
            metadata={"min_distance": dist, "num_prototypes": len(self.prototypes)},
            processing_time=processing_time,
        ) 


# -----------------------------------------------------------------------------
# PCA-compressed prototype expert (speed + accuracy trade-off)
# -----------------------------------------------------------------------------

class PCAPrototypeDigitExpert(BaseExpertModule):
    """Digit expert operating in a shared PCA sub-space.

    All digits share the same *basis* (matrix of shape [n_components, 784]).
    Each expert stores one or more **projected** prototypes of shape
    [n_prototypes, n_components].  Distances are thus much cheaper than in the
    original 784-D space while retaining most variance (>90 % with 50 comps).
    """

    def __init__(
        self,
        digit: int,
        projected_prototypes: np.ndarray,  # shape (k, n_components)
        pca_basis: np.ndarray,             # shape (n_components, 784)
    ):
        if projected_prototypes.ndim != 2:
            raise ValueError("projected_prototypes must be 2-D [k, n_components]")
        self.digit = digit
        self.prototypes = projected_prototypes.astype(np.float32)
        self.basis = pca_basis.astype(np.float32)
        self.n_components = self.basis.shape[0]
        super().__init__(name=f"PCADigit{digit}Expert", domain="mnist_digit", version="1.0")

    # ------------------------------------------------------------------
    def _define_wave_frequencies(self) -> Dict[str, float]:
        return {f"digit_{self.digit}_pca": 3.0 + 0.1 * self.digit}

    def _project(self, img: np.ndarray) -> np.ndarray:
        x = img.astype(np.float32).flatten()
        mean = x.mean(); std = x.std() if x.std() > 1e-3 else 1.0
        x = (x - mean) / std
        return (self.basis @ x).astype(np.float32)  # (n_components,)

    def can_handle(self, query: str, context: Dict[str, Any] | None = None) -> float:
        if query != "classify_digit" or context is None or "image" not in context:
            return 0.0
        img = context["image"]
        vec = context.get("pca_vec") or self._project(img)
        dists = np.linalg.norm(self.prototypes - vec, axis=1)
        dist = float(dists.min())
        return float(np.exp(-dist / 15.0))

    def process_query(self, query: str, context: Dict[str, Any] | None = None) -> ExpertResponse:
        if not context or "image" not in context:
            raise ValueError("PCAPrototypeDigitExpert expects 'image' in context")
        start = time.perf_counter()
        img = context["image"]
        vec = context.get("pca_vec") or self._project(img)
        dists = np.linalg.norm(self.prototypes - vec, axis=1)
        dist = float(dists.min())
        confidence = float(np.exp(-dist / 15.0))
        processing_time = time.perf_counter() - start
        reasoning = (
            f"Min PCA distance to digit {self.digit} = {dist:.2f}; conf={confidence:.3f}"
        )
        waves = self.generate_wave_patterns([f"digit_{self.digit}_pca"], strength=confidence)
        return ExpertResponse(
            confidence=confidence,
            reasoning=reasoning,
            answer=self.digit,
            wave_patterns=waves,
            metadata={"min_distance": dist, "n_components": self.n_components},
            processing_time=processing_time,
        ) 