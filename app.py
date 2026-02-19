from flask import Flask, render_template, Response
import csv
import io
import json

app = Flask(__name__)

# ---- API Response (your shared dictionary) ----

DATA_FILE = "Chatgpt/flask/response.json"


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    

api_response = load_data()

@app.route("/")
def report():
    return render_template("report.html", data=api_response)


@app.route("/download")
def download_csv():
    output = io.StringIO()
    writer = csv.writer(output)

    # CSV Header
    writer.writerow([
        "District",
        "Classification",
        "Category",
        "Incentive Name",
        "Max Amount",
        "Status Evidence",
        "Page Numbers",
        "Breakdown"
    ])

    # Flatten nested structure
    for item in api_response:
        for incentive in item["values"]:
            writer.writerow([
                item["district"],
                item["classification"],
                item["Category"],
                incentive["Incentive Name"],
                incentive["Max amount"],
                incentive["Status Evidence"],
                incentive["page Numbers"],
                incentive["Breakdown"]
            ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=incentives_report.csv"}
    )


if __name__ == "__main__":
    app.run(debug=True)
