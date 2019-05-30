import StringIO
import csv
from flask import make_response

@app.route('/export', methods="GET")
def export(self):
    si = StringIO.StringIO()
    cw = csv.writer(si)
    cw.writerows(csvList)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
