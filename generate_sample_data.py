"""Generates SYNTHETIC quarterly bank data (15 banks x 20 quarters = 300 rows) so the pipeline runs end to end.
Replace data/bank_quarterly.csv with real published results (same columns) to reproduce a real analysis."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
banks = [("PSU Bank %02d" % i, "PSU") for i in range(1, 8)] + [("Private Bank %02d" % i, "Private") for i in range(1, 9)]
quarters = pd.period_range("2021Q1", periods=20, freq="Q").astype(str)
rows = []
for name, sector in banks:
    deposits = rng.uniform(150_000, 900_000) if sector == "PSU" else rng.uniform(80_000, 600_000)
    gnpa = rng.uniform(6, 10) if sector == "PSU" else rng.uniform(2, 4)
    casa = rng.uniform(32, 42) if sector == "PSU" else rng.uniform(38, 48)
    for q in quarters:
        g = rng.normal(0.018 if sector == "PSU" else 0.028, 0.006)
        deposits *= 1 + g
        gnpa = max(0.8, gnpa - rng.normal(0.22 if sector == "PSU" else 0.08, 0.1))
        casa = float(np.clip(casa + rng.normal(-0.05, 0.4), 25, 55))
        advances = deposits * rng.uniform(0.68, 0.82)
        nim = rng.normal(2.9 if sector == "PSU" else 3.7, 0.12)
        rows.append({"bank": name, "sector": sector, "quarter": q, "deposits_crore": round(deposits, 1),
                     "advances_crore": round(advances, 1), "nii_crore": round(advances * nim / 100 / 4 * 1.1, 1),
                     "casa_pct": round(casa, 2), "gnpa_pct": round(gnpa, 2)})
pd.DataFrame(rows).to_csv("data/bank_quarterly.csv", index=False)
print(len(rows), "rows written")
