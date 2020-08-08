import os
import wget
from google.cloud import bigquery
from flask import Flask, render_template

app = Flask(__name__)
client = bigquery.Client()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load')
def load():
    data_file = os.environ.get('DATAFILE')
    source_file = "/tmp/aus.csv"
    try:
        wget.download(data_file, source_file)
    except:
        return {"status":"failed","message":"wget failed to download file."}

    table_id = os.environ.get('TABLE_ID')
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
    )

    with open(source_file, "rb") as f:
        job = client.load_table_from_file(f, table_id, job_config=job_config)

    job.result()  # Waits for the job to complete.

    table = client.get_table(table_id)  # Make an API request.
    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )
    return {"status":"ok"}

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
