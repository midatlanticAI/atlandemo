# Emotion Probe on Animal Vocalizations (2025-07-16)

This note records the first **cross-species affect probe** using the Atlan Emotion Awareness Layer.
No labels or supervised training were used; the system derives affect purely from band-specific wave energy as documented in the main README.

---
## Method
```
# repo root – Windows PowerShell
py -3 simulations/music_emotion_probe.py \
    samples/BlueJay.wav samples/Cardinal.wav \
    samples/bottlenose.wav \
    samples/humpback1.wav samples/humpback2.wav \
    samples/humpback3.wav samples/humpback4.wav
```
The probe script:
1. Down-samples audio to 200 Hz.
2. Extracts θ-band (4-8 Hz) and γ-band (30-50 Hz) envelopes.
3. Applies a 1 s moving-average window (≈20 engine frames).
4. Scales by MAD and clips to ±1 to mirror engine bounds.
5. Reports mean & median valence / arousal for the entire clip.

---
## Results
| Clip                | Valence (mean) | Arousal (mean) |
|---------------------|---------------:|---------------:|
| BlueJay.wav         | +0.02          | –0.00          |
| Cardinal.wav        | +0.02          | –0.01          |
| bottlenose.wav      | +0.12          | +0.08          |
| humpback1.wav       | +0.11          | +0.03          |
| humpback2.wav       | +0.05          | +0.04          |
| humpback3.wav       | +0.12          | +0.01          |
| humpback4.wav       | +0.11          | +0.12          |

Interpretation:
* **Birdsong** (BlueJay, Cardinal) sits near neutral valence and negligible arousal.
* **Dolphin clicks** are noticeably brighter (positive valence) and more energetic.
* **Humpback whale songs** maintain high positive valence; the longest clip (#4) also drives the highest arousal.

---
## Limitations & Next Steps
* Scaling is empirical; larger corpora are needed for robust calibration.
* Only seven short clips—expand to >100 clips across taxa.
* No human-rated baseline yet; plan a small MTurk study for correlation.
* Plots and CSV logs can be generated with `--plot` (visual) and a forthcoming `--save-csv` flag.

---
*Committed to repo tag `v1.1-emotion-animal-audio` for provenance.* 