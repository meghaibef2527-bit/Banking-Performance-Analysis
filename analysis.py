"""Loads bank_quarterly.csv into SQLite, runs the SQL in sql/queries.sql and builds charts. Run: python analysis.py"""
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("data/bank_quarterly.csv")
con = sqlite3.connect(":memory:")
con.executescript(open("sql/schema.sql").read())
df.to_sql("bank_quarterly", con, if_exists="append", index=False)

queries = [q.strip() for q in open("sql/queries.sql").read().split(";") if "SELECT" in q]
names = ["sector_trends", "gnpa_change", "deposit_growth", "casa_ranking"]
results = {}
for name, q in zip(names, queries):
    results[name] = pd.read_sql_query(q, con)
    results[name].round(2).to_csv(f"outputs/{name}.csv", index=False)
    print(f"\n== {name} ==\n{results[name].round(2).head(10).to_string(index=False)}")

trend = results["sector_trends"].pivot(index="quarter", columns="sector", values="avg_gnpa_pct")
ax = trend.plot(figsize=(8, 4), title="Average GNPA ratio by sector (%)")
ax.set_ylabel("%"); plt.tight_layout(); plt.savefig("outputs/gnpa_trend.png", dpi=130)
