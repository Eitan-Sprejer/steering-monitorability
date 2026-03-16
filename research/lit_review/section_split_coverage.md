# Section Split Coverage Report

Generated: 2026-02-19

## Summary

| Metric | Count |
|---|---|
| Total papers in `txt/` | 98 |
| Papers with `sections/` directory | 84 |
| Papers missing `sections/` directory | 14 |
| Papers with `sections/` but poor split (pdftext fallback) | 6 |
| Papers with genuine section splits | 78 |

---

## Papers missing `sections/` directory (14)

These papers have raw text in `txt/` but no section subdirectory at all:

```
2501.03124
2504.07831
2504.13707
2505.17244
2505.17815
2509.17938
2510.24941
2510.27378
2601.06423
2601.07663
2601.21183
2602.01750
2602.02496
2602.08449
```

---

## Papers with `sections/` but poor split -- pdftext fallback (6)

These have a `sections/` directory but only contain `full.txt`, `abstract.txt`, and `references.txt`. The index.txt is marked "(pdftext fallback -- HTML not available)", meaning no meaningful section parsing occurred.

| Paper ID | Files present |
|---|---|
| 2301.13379 | full.txt, abstract.txt |
| 2307.11768 | full.txt, abstract.txt |
| 2307.13702 | full.txt, abstract.txt, references.txt |
| 2310.18512 | full.txt, abstract.txt |
| 2412.04984 | full.txt, abstract.txt |
| 2502.12025 | full.txt, abstract.txt |

---

## Papers with genuine section splits (78)

All have 3+ meaningful sections. Section count = number of lines in `index.txt`.

| Paper ID | Sections |
|---|---|
| 2305.04388 | 8 |
| 2311.07466 | 11 |
| 2312.01037 | 15 |
| 2312.06942 | 20 |
| 2401.05566 | 20 |
| 2402.00559 | 11 |
| 2402.13950 | 10 |
| 2402.14897 | 6 |
| 2403.05518 | 19 |
| 2405.15092 | 14 |
| 2406.07358 | 23 |
| 2406.10162 | 15 |
| 2407.13692 | 15 |
| 2409.12822 | 10 |
| 2412.14093 | 18 |
| 2412.16339 | 6 |
| 2501.08156 | 8 |
| 2501.15210 | 4 |
| 2502.08177 | 4 |
| 2502.12558 | 8 |
| 2502.14829 | 21 |
| 2502.18848 | 12 |
| 2503.08679 | 7 |
| 2503.10965 | 16 |
| 2503.11926 | 13 |
| 2503.16851 | 7 |
| 2505.05410 | 9 |
| 2505.23575 | 10 |
| 2506.04909 | 6 |
| 2506.06603 | 6 |
| 2506.09404 | 9 |
| 2506.13206 | 10 |
| 2506.15109 | 3 |
| 2506.15826 | 4 |
| 2506.19143 | 24 |
| 2506.22777 | 13 |
| 2507.01786 | 9 |
| 2507.11473 | 5 |
| 2507.12428 | 14 |
| 2507.12691 | 16 |
| 2507.22928 | 6 |
| 2508.00943 | 13 |
| 2508.19827 | 18 |
| 2508.20151 | 5 |
| 2509.00591 | 5 |
| 2509.03518 | 8 |
| 2509.12895 | 6 |
| 2509.13333 | 6 |
| 2510.03999 | 11 |
| 2510.04040 | 8 |
| 2510.07364 | 14 |
| 2510.18154 | 7 |
| 2510.19476 | 5 |
| 2510.19851 | 6 |
| 2511.08525 | 12 |
| 2511.17408 | 24 |
| 2511.22662 | 12 |
| 2512.04864 | 9 |
| 2512.07810 | 9 |
| 2512.09187 | 8 |
| 2512.11949 | 5 |
| 2512.15674 | 10 |
| 2512.20798 | 9 |
| 2601.00514 | 15 |
| 2601.05752 | 8 |
| 2601.09269 | 7 |
| 2601.14691 | 9 |
| 2602.01425 | 11 |
| 2602.03978 | 9 |
| 2602.04856 | 7 |
| 2602.05539 | 6 |
| 2602.11201 | 8 |
| 2602.13904 | 12 |
| 2602.14095 | 5 |
| 2602.14469 | 14 |
| 2602.14529 | 14 |
| 2602.15338 | 8 |
| 2602.15515 | 20 |

---

## Action items

- **20 papers need section splitting** (14 missing + 6 fallback)
- The 6 fallback papers (2301.13379, 2307.11768, 2307.13702, 2310.18512, 2412.04984, 2502.12025) have HTML unavailable; section extraction may not be possible without manual parsing
- The 14 papers with no sections/ directory at all should be section-split using the standard pipeline
