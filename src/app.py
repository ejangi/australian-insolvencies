import os
import datetime
from insolvencies import load_to_bq, get_results
from flask import Flask, render_template, request, jsonify, Response, send_from_directory

app = Flask(__name__)

@app.template_filter('formatPubDate')
def format_pubDate(value):
    sp = value.split('-')
    dt = datetime.datetime(int(sp[0]), int(sp[1]), 1)
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000");

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory('images', path)

@app.route('/data.json')
def json():
    table_id = os.environ.get('TABLE_ID')
    results = get_results(table_id)
    ret = []
    for row in results:
        r = {
            "Year":row["Year"],
            "Month":row["Month"],
            "Quarter":row["Quarter"],
            "NSW":row["NSW"],
            "ACT":row["ACT"],
            "VIC":row["VIC"],
            "QLD":row["QLD"],
            "SA":row["SA"],
            "NT":row["NT"],
            "WA":row["WA"],
            "TAS":row["TAS"],
            "Other":row["Other"],
            "Australia":row["Australia"],
            "NSWSinceLastQuarter":row["NSWSinceLastQuarter"],
            "NSWSinceLastYear":row["NSWSinceLastYear"],
            "ACTSinceLastQuarter":row["ACTSinceLastQuarter"],
            "ACTSinceLastYear":row["ACTSinceLastYear"],
            "VICSinceLastQuarter":row["VICSinceLastQuarter"],
            "VICSinceLastYear":row["VICSinceLastYear"],
            "QLDSinceLastQuarter":row["QLDSinceLastQuarter"],
            "QLDSinceLastYear":row["QLDSinceLastYear"],
            "SASinceLastQuarter":row["SASinceLastQuarter"],
            "SASinceLastYear":row["SASinceLastYear"],
            "NTSinceLastQuarter":row["NTSinceLastQuarter"],
            "NTSinceLastYear":row["NTSinceLastYear"],
            "WASinceLastQuarter":row["WASinceLastQuarter"],
            "WASinceLastYear":row["WASinceLastYear"],
            "TASSinceLastQuarter":row["TASSinceLastQuarter"],
            "TASSinceLastYear":row["TASSinceLastYear"],
            "OtherSinceLastQuarter":row["OtherSinceLastQuarter"],
            "OtherSinceLastYear":row["OtherSinceLastYear"],
            "AustraliaSinceLastQuarter":row["AustraliaSinceLastQuarter"],
            "AustraliaSinceLastYear":row["AustraliaSinceLastYear"]
        }
        ret.append(r)
    return jsonify(ret), 200

@app.route('/feed')
def feed_all():
    url = os.environ.get('URL')
    table_id = os.environ.get('TABLE_ID')
    results = get_results(table_id, True)
    return Response(render_template('rss-all.xml', url=url, results=results), mimetype='text/xml')

@app.route('/feed/<type>')
def feed(type='Australia'):
    if type not in ["Australia", "QLD", "NSW", "ACT", "VIC", "TAS", "NT", "SA", "WA", "Other"]:
        return jsonify({"status":"forbidden","message":"Invalid location."}), 403
    url = os.environ.get('URL')
    table_id = os.environ.get('TABLE_ID')
    results = get_results(table_id, True)
    return Response(render_template('rss.xml', url=url, type=type, results=results), mimetype='text/xml')

@app.route('/load')
def load():
    load_key = os.environ.get('LOAD_KEY')
    key = request.args.get("key")

    if key != load_key:
        return jsonify({"status":"forbidden","message":"Invalid API Key"}), 403

    table_id_raw = os.environ.get('TABLE_ID_RAW')
    data_file = os.environ.get('DATAFILE')
    source_file = "/tmp/aus.csv"

    if load_to_bq(data_file, source_file, table_id_raw):
        return jsonify({"status":"ok"}), 200
    else:
        return jsonify({"status":"failed","message":"The load failed."}), 500

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
