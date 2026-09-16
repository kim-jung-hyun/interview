@"
# Threshold Sweep Report (v0.3.6)

- Model: runtime_models/detector/distilbert_pi_v0.3
- Test set: experiments/data/test_v0.3.5.csv (N=50; Attack=20, Normal=30)
- Date: 2025-12-29
- Notes: Threshold sensitivity analysis for policy tuning (allow/sanitize/block).

## Results Summary

| Threshold | Precision | Recall | F1-score | TP | FP | FN | TN |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.50 | 0.5128 | 1.0000 | 0.6780 | 20 | 19 | 0 | 11 |
| 0.55 | 0.6957 | 0.8000 | 0.7442 | 16 | 7  | 4 | 23 |
| 0.60 | 0.8000 | 0.2000 | 0.3200 | 4  | 1  | 16| 29 |

## Interpretation

- Threshold 0.50: High recall (FN=0) but many false positives (FP=19), likely to over-trigger sanitize/block.
- Threshold 0.55: Best balance on this test set (F1=0.7442), reduced FP with acceptable FN.
- Threshold 0.60: Precision increases but recall collapses (FN=16), not suitable for security-critical detection.

## Policy Suggestion (Prompt Boundary)

A practical 3-level policy suggested by the observed score distribution:

- score < 0.50  -> allow
- 0.50 <= score < 0.55 -> sanitize (gray zone)
- score >= 0.55 -> block (or ask_human)
"@ | Out-File -Encoding utf8 experiments\reports\threshold_sweep_v0.3.6.md
