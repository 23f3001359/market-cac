#!/usr/bin/env python3
"""
analysis.py
Processes quarterly CAC data, creates visualizations (trend + benchmark), and prints key metrics.

Usage:
    python analysis.py
Outputs:
    - figures/cac_trend.png
    - figures/cac_benchmark_comparison.png
    - analysis_summary.txt
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# --- Config ---
DATA_PATH = "quarterly_cac.csv"
FIG_DIR = "figures"
BENCHMARK = 150.0
REQUIRED_MEAN = 229.56  # as required, for README verification
EMAIL = "23f3001359@ds.study.iitm.ac.in"

os.makedirs(FIG_DIR, exist_ok=True)

# --- Read data ---
df = pd.read_csv(DATA_PATH)
if "quarter" not in df.columns or "cac" not in df.columns:
    raise ValueError("CSV must contain 'quarter' and 'cac' columns")

# Ensure quarters are treated as ordered categories (preserve file order)
quarters = df["quarter"].astype(str).tolist()
cacs = df["cac"].astype(float).tolist()

# --- Compute metrics ---
mean_cac = float(pd.Series(cacs).mean())
median_cac = float(pd.Series(cacs).median())

print(f"Read {len(df)} rows from {DATA_PATH}")
print(f"Average CAC: {mean_cac:.2f}")
print(f"Median CAC: {median_cac:.2f}")
print(f"For verification: {EMAIL}")

# Sanity check: matches required mean (allow a tiny floating-point tolerance)
if abs(mean_cac - REQUIRED_MEAN) > 1e-6:
    print("WARNING: computed mean does not equal REQUIRED_MEAN (229.56).")
else:
    print("Verified: computed mean equals required README value 229.56")

# --- Plot 1: CAC trend with benchmark line ---
plt.figure(figsize=(10,5))
plt.plot(quarters, cacs, marker='o', linewidth=2, label='Company CAC')
plt.axhline(BENCHMARK, color='red', linestyle='--', linewidth=1.5, label=f'Industry Benchmark ({BENCHMARK:.0f})')
plt.title('Quarterly Customer Acquisition Cost (CAC) — Trend vs. Benchmark')
plt.xlabel('Quarter')
plt.ylabel('CAC (USD)')
plt.xticks(rotation=45)
plt.grid(alpha=0.25)
plt.legend()
plt.tight_layout()
trend_path = os.path.join(FIG_DIR, "cac_trend.png")
plt.savefig(trend_path, dpi=150)
plt.close()
print(f"Saved CAC trend figure to: {trend_path}")

# --- Plot 2: Simple bar comparing average to benchmark ---
plt.figure(figsize=(6,4))
labels = ['Company Avg CAC', 'Industry Benchmark']
values = [mean_cac, BENCHMARK]
bars = plt.bar(labels, values)
plt.title('Company Average CAC vs Industry Benchmark')
plt.ylabel('CAC (USD)')

# annotate bars
for bar in bars:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, y + 3, f"{y:.2f}", ha='center', va='bottom')

plt.tight_layout()
cmp_path = os.path.join(FIG_DIR, "cac_benchmark_comparison.png")
plt.savefig(cmp_path, dpi=150)
plt.close()
print(f"Saved benchmark comparison figure to: {cmp_path}")

# --- Summary file (optional) ---
summary_text = f"""CAC Analysis Summary
--------------------
Rows analyzed: {len(df)}
Average CAC: {mean_cac:.2f}
Median CAC: {median_cac:.2f}
Industry benchmark: {BENCHMARK:.2f}

Key insight:
- Current average CAC ({mean_cac:.2f}) is higher than the industry benchmark ({BENCHMARK:.2f}).
- Recommended solution: optimize digital marketing channels (reallocate spend to organic/referral, improve conversion funnel, A/B test landing pages, etc).

Contact for verification: {EMAIL}
"""
with open("analysis_summary.txt", "w", encoding="utf-8") as fh:
    fh.write(summary_text)
print("Wrote analysis_summary.txt")

# --- Done ---
print("Analysis complete.")
