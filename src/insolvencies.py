import wget
from google.cloud import bigquery

client = bigquery.Client()

def get_results(table_id):
    sql = "SELECT Quarter, Australia, ACT, NSW, NT, QLD, SA, TAS, VIC, WA, Other FROM data_gov_au.australian_insolvencies ORDER BY Quarter ASC"
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
    