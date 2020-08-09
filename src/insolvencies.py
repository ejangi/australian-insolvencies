import wget
from google.cloud import bigquery

client = bigquery.Client()

def get_results(table_id, reverse=False):
    sql = "SELECT Year, Month, Quarter, NSW, ACT, VIC, QLD, SA, NT, WA, TAS, Other, Australia, NSWSinceLastQuarter, NSWSinceLastYear, ACTSinceLastQuarter, ACTSinceLastYear, VICSinceLastQuarter, VICSinceLastYear, QLDSinceLastQuarter, QLDSinceLastYear, SASinceLastQuarter, SASinceLastYear, NTSinceLastQuarter, NTSinceLastYear, WASinceLastQuarter, WASinceLastYear, TASSinceLastQuarter, TASSinceLastYear, OtherSinceLastQuarter, OtherSinceLastYear, AustraliaSinceLastQuarter, AustraliaSinceLastYear FROM data_gov_au.australian_insolvencies ORDER BY Quarter"
    if reverse:
        sql += " DESC"
    return client.query(sql)

def load_to_bq(data_file, source_file, table_id):
    try:
        wget.download(data_file, source_file)
    except:
        return {"status":"failed","message":"wget failed to download file."}

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
    )

    with open(source_file, "rb") as f:
        job = client.load_table_from_file(f, table_id, job_config=job_config)

    try:
        job.result()  # Waits for the job to complete.

        table = client.get_table(table_id)  # Make an API request.
        print(
            "Loaded {} rows and {} columns to {}".format(
                table.num_rows, len(table.schema), table_id
            )
        )
        return True
    except:
        return False
    