import os
from insolvencies import load_to_bq, get_results
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data.json')
def json():
    table_id = os.environ.get('TABLE_ID')
    results = get_results(table_id)
    ret = []
    for row in results:
        r = {
            "Quarter":row["Quarter"],
            "Australia":row["Australia"],
            "ACT":row["ACT"],
            "NSW":row["NSW"],
            "NT":row["NT"],
            "QLD":row["QLD"],
            "SA":row["SA"],
            "TAS":row["TAS"],
            "VIC":row["VIC"],
            "WA":row["WA"]
        }
        ret.append(r)
    return jsonify(ret)

@app.route('/load')
def load():
    load_key = os.environ.get('LOAD_KEY')
    key = request.args.get("key")

    if key != load_key:
        return {"status":"forbidden","message":"Invalid API Key"}

    table_id_raw = os.environ.get('TABLE_ID_RAW')
    data_file = os.environ.get('DATAFILE')
    source_file = "/tmp/aus.csv"

    if load_to_bq(data_file, source_file, table_id_raw):
        return {"status":"ok"}
    else:
        return {"status":"failed","message":"The load failed."}

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
