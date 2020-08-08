# Australian Insolvencies

> This utility creates a graph of Australian insolvencies.

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

## Setup

1) Create a *raw* table where the data will be uploaded to, using the following schema:

```json
[{"name":"Quarter","type":"STRING","mode":"NULLABLE"},{"name":"Total_debtors_entering_a_business_related_personal_insolvency__NSW","type":"INTEGER","mode":"NULLABLE"},{"name":"Total_debtors_entering_a_business_related_personal_insolvency__ACT","type":"INTEGER","mode":"NULLABLE"},{"name":"Total_debtors_entering_a_business_related_personal_insolvency__Vic","type":"INTEGER","mode":"NULLABLE"},{"name":"Total_debtors_entering_a_business_related_personal_insolvency__Qld","type":"INTEGER","mode":"NULLABLE"},{"name":"Total_debtors_entering_a_business_related_personal_insolvency__SA","type":"INTEGER","mode":"NULLABLE"},{"name":"Total_debtors_entering_a_business_related_personal_insolvency__NT","type":"INTEGER","mode":"NULLABLE"},{"name":"Total_debtors_entering_a_business_related_personal_insolvency__WA","type":"INTEGER","mode":"NULLABLE"},{"name":"Total_debtors_entering_a_business_related_personal_insolvency__Tas","type":"INTEGER","mode":"NULLABLE"},{"name":"Total_debtors_entering_a_business_related_personal_insolvency__Other","type":"INTEGER","mode":"NULLABLE"},{"name":"Total_debtors_entering_a_business_related_personal_insolvency__Australia","type":"INTEGER","mode":"NULLABLE"}]
```

2) Create a scheduled query that deduplicates the raw data into a fresh table, using this query

```sql
SELECT 
  Year,
  Month,
  CONCAT(Year, '-', Month) AS Quarter,
  NSW,
  ACT,
  VIC,
  QLD,
  SA,
  NT,
  WA,
  TAS,
  Other,
  Australia,
  COALESCE(((NSW - LAG(NSW) OVER (ORDER BY Year ASC, Month ASC)) * 100) / LAG(NSW) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS NSWSinceLastQuarter,
  COALESCE(((NSW - LAG(NSW) OVER (PARTITION BY Month ORDER BY Year ASC, Month ASC)) * 100) / LAG(NSW) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS NSWSinceLastYear,
  COALESCE(((ACT - LAG(ACT) OVER (ORDER BY Year ASC, Month ASC)) * 100) / LAG(ACT) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS ACTSinceLastQuarter,
  COALESCE(((ACT - LAG(ACT) OVER (PARTITION BY Month ORDER BY Year ASC, Month ASC)) * 100) / LAG(ACT) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS ACTSinceLastYear,
  COALESCE(((VIC - LAG(VIC) OVER (ORDER BY Year ASC, Month ASC)) * 100) / LAG(VIC) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS VICSinceLastQuarter,
  COALESCE(((VIC - LAG(VIC) OVER (PARTITION BY Month ORDER BY Year ASC, Month ASC)) * 100) / LAG(VIC) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS VICSinceLastYear,
  COALESCE(((QLD - LAG(QLD) OVER (ORDER BY Year ASC, Month ASC)) * 100) / LAG(QLD) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS QLDSinceLastQuarter,
  COALESCE(((QLD - LAG(QLD) OVER (PARTITION BY Month ORDER BY Year ASC, Month ASC)) * 100) / LAG(QLD) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS QLDSinceLastYear,
  COALESCE(((SA - LAG(SA) OVER (ORDER BY Year ASC, Month ASC)) * 100) / LAG(SA) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS SASinceLastQuarter,
  COALESCE(((SA - LAG(SA) OVER (PARTITION BY Month ORDER BY Year ASC, Month ASC)) * 100) / LAG(SA) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS SASinceLastYear,
  COALESCE(((NT - LAG(NT) OVER (ORDER BY Year ASC, Month ASC)) * 100) / LAG(NT) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS NTSinceLastQuarter,
  COALESCE(((NT - LAG(NT) OVER (PARTITION BY Month ORDER BY Year ASC, Month ASC)) * 100) / LAG(NT) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS NTSinceLastYear,
  COALESCE(((WA - LAG(WA) OVER (ORDER BY Year ASC, Month ASC)) * 100) / LAG(WA) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS WASinceLastQuarter,
  COALESCE(((WA - LAG(WA) OVER (PARTITION BY Month ORDER BY Year ASC, Month ASC)) * 100) / LAG(WA) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS WASinceLastYear,
  COALESCE(((TAS - LAG(TAS) OVER (ORDER BY Year ASC, Month ASC)) * 100) / LAG(TAS) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS TASSinceLastQuarter,
  COALESCE(((TAS - LAG(TAS) OVER (PARTITION BY Month ORDER BY Year ASC, Month ASC)) * 100) / LAG(TAS) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS TASSinceLastYear,
  COALESCE(((Other - LAG(Other) OVER (ORDER BY Year ASC, Month ASC)) * 100) / LAG(Other) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS OtherSinceLastQuarter,
  COALESCE(((Other - LAG(Other) OVER (PARTITION BY Month ORDER BY Year ASC, Month ASC)) * 100) / LAG(Other) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS OtherSinceLastYear,
  COALESCE(((Australia - LAG(Australia) OVER (ORDER BY Year ASC, Month ASC)) * 100) / LAG(Australia) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS AustraliaSinceLastQuarter,
  COALESCE(((Australia - LAG(Australia) OVER (PARTITION BY Month ORDER BY Year ASC, Month ASC)) * 100) / LAG(Australia) OVER (ORDER BY Year ASC, Month ASC), 0.00) AS AustraliaSinceLastYear
FROM (
  SELECT 
    CONCAT('20', SPLIT(raw.Quarter, '-')[OFFSET(1)]) AS `Year`, 
    CASE
      WHEN SPLIT(raw.Quarter, '-')[OFFSET(0)] = 'Jan' THEN '01'
      WHEN SPLIT(raw.Quarter, '-')[OFFSET(0)] = 'Feb' THEN '02'
      WHEN SPLIT(raw.Quarter, '-')[OFFSET(0)] = 'Mar' THEN '03'
      WHEN SPLIT(raw.Quarter, '-')[OFFSET(0)] = 'Apr' THEN '04'
      WHEN SPLIT(raw.Quarter, '-')[OFFSET(0)] = 'May' THEN '05'
      WHEN SPLIT(raw.Quarter, '-')[OFFSET(0)] = 'Jun' THEN '06'
      WHEN SPLIT(raw.Quarter, '-')[OFFSET(0)] = 'Jul' THEN '07'
      WHEN SPLIT(raw.Quarter, '-')[OFFSET(0)] = 'Aug' THEN '08'
      WHEN SPLIT(raw.Quarter, '-')[OFFSET(0)] = 'Sep' THEN '09'
      WHEN SPLIT(raw.Quarter, '-')[OFFSET(0)] = 'Oct' THEN '10'
      WHEN SPLIT(raw.Quarter, '-')[OFFSET(0)] = 'Nov' THEN '11'
      WHEN SPLIT(raw.Quarter, '-')[OFFSET(0)] = 'Dec' THEN '12'
    END AS `Month`,
    raw.Total_debtors_entering_a_business_related_personal_insolvency__NSW AS NSW,
    raw.Total_debtors_entering_a_business_related_personal_insolvency__ACT AS ACT,
    raw.Total_debtors_entering_a_business_related_personal_insolvency__Vic AS VIC,
    raw.Total_debtors_entering_a_business_related_personal_insolvency__Qld AS QLD,
    raw.Total_debtors_entering_a_business_related_personal_insolvency__SA AS SA,
    raw.Total_debtors_entering_a_business_related_personal_insolvency__NT AS NT,
    raw.Total_debtors_entering_a_business_related_personal_insolvency__WA AS WA,
    raw.Total_debtors_entering_a_business_related_personal_insolvency__Tas AS TAS,
    raw.Total_debtors_entering_a_business_related_personal_insolvency__Other AS Other,
    raw.Total_debtors_entering_a_business_related_personal_insolvency__Australia AS Australia,
    ROW_NUMBER() OVER (PARTITION BY raw.Quarter ORDER BY raw.Quarter ASC) row_number
  FROM data_gov_au.australian_insolvencies_raw AS raw
) AS dedupe
WHERE row_number = 1
ORDER BY dedupe.Year ASC, dedupe.Month ASC
```

3) Set the environment variables for `TABLE_ID` and `TABLE_ID_RAW` and `LOAD_KEY`.

4) Schedule the load using `Cloud Scheduler`.