# Australian Insolvencies

> This utility creates a graph of Australian insolvencies.

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

## Setup

1) Create a *raw* table where the data will be uploaded to, using the following schema:

```json
```

2) Create a scheduled query that deduplicates the raw data into a fresh table, using this query

```sql
SELECT 
  CONCAT(SPLIT(dedupe.Quarter, '-')[OFFSET(1)], '-', SPLIT(dedupe.Quarter, '-')[OFFSET(0)]) AS Quarter,
  dedupe.Total_debtors_entering_a_business_related_personal_insolvency__NSW AS NSW,
  dedupe.Total_debtors_entering_a_business_related_personal_insolvency__ACT AS ACT,
  dedupe.Total_debtors_entering_a_business_related_personal_insolvency__Vic AS VIC,
  dedupe.Total_debtors_entering_a_business_related_personal_insolvency__Qld AS QLD,
  dedupe.Total_debtors_entering_a_business_related_personal_insolvency__SA AS SA,
  dedupe.Total_debtors_entering_a_business_related_personal_insolvency__NT AS NT,
  dedupe.Total_debtors_entering_a_business_related_personal_insolvency__WA AS WA,
  dedupe.Total_debtors_entering_a_business_related_personal_insolvency__Tas AS TAS,
  dedupe.Total_debtors_entering_a_business_related_personal_insolvency__Other AS Other,
  dedupe.Total_debtors_entering_a_business_related_personal_insolvency__Australia AS Australia,
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY Quarter ORDER BY Quarter ASC) row_number
  FROM <my-dataset_id>.<my-raw-table_id> AS raw
) AS dedupe
WHERE row_number = 1
ORDER BY dedupe.Quarter ASC
```

3) Set the environment variables for `TABLE_ID` and `TABLE_ID_RAW`.