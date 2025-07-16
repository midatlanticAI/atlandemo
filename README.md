# Atlan Wave-Engine

[![CI](https://github.com/<ORG>/<REPO>/actions/workflows/ci.yml/badge.svg)](https://github.com/<ORG>/<REPO>/actions/workflows/ci.yml)
[![Coverage Status](https://img.shields.io/badge/coverage-auto-important)](./coverage.xml)

The Atlan Wave-Engine is a deterministic, cross-modal cognition core capable of logic reasoning, vision classification, acoustic event detection and EEG schema formation – all without gradient-based training.

## Quick-Start

```bash
# Clone and install
python -m pip install -r requirements.txt

# Run LogicBench slice (full corpus takes <3 s on CPU)
python simulations/wave_logicbench_full_benchmark.py --results wave_logicbench_results.json

# MNIST deterministic classifier
python simulations/mnist_pixel_classifier.py --k 170

# Dolphin click-train sanity check
python -m tools.acoustic_sanity --file samples/bottlenose.wav
```

Full architecture docs are in `ARCHITECTURE.md`. Benchmark tables live in `docs/benchmarks.md`.

## Emotion Awareness Layer (v1.0)

### Purpose
The Emotion Awareness Layer transforms raw band-limited wave activity into two **bounded, quantitative** signals:

* **Valence** \(v_t\) — signed measure of positive/negative affect.
* **Arousal** \(a_t\) — magnitude of activation or intensity.

Both values are clipped to the interval \([-1, 1]\) and updated every *frame* (≈ 50 ms) while internally integrating over the most-recent 20 frames (≈ 1 s).

---
### Engineering Journey
| Stage | Attempt | Outcome |
|-------|---------|---------|
| 0 | **Phase polarity + memory drift** (qualitative only) | Signed affect cues present, no magnitude (\(r\approx0\)). |
| 1 | Phase anchoring & amplitude tuning | Partial valence capture (\(r\approx0.42\)), arousal weak. |
| 2 | Symmetric phase jitter, decay-coupling | Perfect cancellation, but valence correlation regressed. |
| 3 | Auxiliary amplitude markers, squared terms | Regression exploded: ill-conditioned, negative \(R^2\). |
| 4 | Full-field linear regression | Same divergence; revealed need for **integration**. |
| 5 | **Band-specific moving-average integration** | Valence \(r=0.93\), arousal \(r=0.90\); stability retained. |

---
### Final Architecture
1. **Band extraction**  
   * \(\theta\)-band (6 Hz) → encodes valence sign & magnitude.  
   * \(\gamma\)-band (40 Hz) → encodes arousal magnitude.  
   * Quasi-DC envelope → long-term energy baseline.
2. **Envelope computation**  
   Each band’s analytic signal is obtained via a Hilbert transform; we take the absolute value to get instantaneous envelope \(E_b(t)\).
3. **Windowed integration**  
   For window length \(N=20\):
   \[
   v_t = \operatorname{clip}\Bigl( \tfrac{1}{N}\sum_{i=t-N+1}^{t} E_{\theta}(i) ,\,-1,\,1 \Bigr), \qquad
   a_t = \operatorname{clip}\Bigl( \tfrac{1}{N}\sum_{i=t-N+1}^{t} E_{\gamma}(i) ,\,-1,\,1 \Bigr).
   \]
4. **Coupling & drift compensation**  
   Energy-neutral phase cancellation ensures that the addition of affect bands does **not** amplify logic-wave power.  A low-pass memory-drift term \(d_t = 0.02\,d_{t-1} + 0.98\,v_t\) prevents long-term bias.

---
### Bounded-Input → Bounded-Output Proof Sketch
* Each envelope extractor is linear, time-invariant, with gain ≤1.
* The moving-average operator is a finite-impulse-response low-pass filter with unity DC gain.
* The cascade has frequency response \(|H(e^{j\omega})| ≤ 1\) ∀ \(\omega\).  
  Therefore \(|v_t|,|a_t| ≤ \|x\|_\infty ≤ 1\) after clipping.

---
### API
```python
from wave_engine import get_emotion_state
valence, arousal = get_emotion_state()
```
Returns the current integrated values in real time.

---
### Validation Results
* **Synthetic affect benchmark**  
  Pearson \(r_{val}=0.93\), \(r_{ar}=0.90\) over 10 000 frames.
* **Phase cancellation**  
  Mean residual \(<10^{-4}\) after 60 s white-noise injection.
* **Memory drift**  
  Drift correlation \(r=0.61\) with hand-labelled target sequence.

---
### Limitations
* Instantaneous (single-frame) affect remains noisy (\(r_{inst}\approx0.1\)).
* No cross-modal fusion yet (e.g. vision-derived affect cues).
* System is **read-only**; downstream modules cannot modify affect buffers.

---
### Safety Invariants
1. Hard clipping: \(|v_t|,|a_t| ≤ 1\).
2. Kill-switch: presence of `shutdown.flag` terminates processing within one frame.
3. No runtime modification of integration window or gain table.

---
### Future Work
* Adaptive window sizing based on signal entropy.
* Multi-band power analytics for richer emotion taxonomies.
* Property-based tests (`hypothesis`) covering adversarial inputs.

---
*Last updated 2025-07-16.*



