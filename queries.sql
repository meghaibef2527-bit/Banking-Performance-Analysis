-- 1. Sector averages by quarter
SELECT sector, quarter, AVG(casa_pct) AS avg_casa_pct, AVG(gnpa_pct) AS avg_gnpa_pct, SUM(nii_crore) AS total_nii
FROM bank_quarterly GROUP BY sector, quarter ORDER BY quarter, sector;

-- 2. Change in GNPA ratio, first vs last quarter, by sector (percentage points)
WITH ends AS (
  SELECT sector, quarter, AVG(gnpa_pct) AS gnpa FROM bank_quarterly GROUP BY sector, quarter
)
SELECT f.sector, f.gnpa AS first_gnpa, l.gnpa AS last_gnpa, l.gnpa - f.gnpa AS change_pp
FROM ends f JOIN ends l ON f.sector = l.sector
WHERE f.quarter = (SELECT MIN(quarter) FROM bank_quarterly)
  AND l.quarter = (SELECT MAX(quarter) FROM bank_quarterly);

-- 3. Deposit growth over the full period by sector
WITH ends AS (
  SELECT sector, quarter, SUM(deposits_crore) AS dep FROM bank_quarterly GROUP BY sector, quarter
)
SELECT f.sector, (l.dep / f.dep - 1) * 100 AS deposit_growth_pct
FROM ends f JOIN ends l ON f.sector = l.sector
WHERE f.quarter = (SELECT MIN(quarter) FROM bank_quarterly)
  AND l.quarter = (SELECT MAX(quarter) FROM bank_quarterly);

-- 4. Banks ranked by latest CASA ratio
SELECT bank, sector, casa_pct FROM bank_quarterly
WHERE quarter = (SELECT MAX(quarter) FROM bank_quarterly) ORDER BY casa_pct DESC;
