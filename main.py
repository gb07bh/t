from flask import Flask, render_template, abort
import os
import json

app = Flask(__name__)

DATA_FOLDER = "data"


def get_available_reports():
    """Return list of json filenames (without .json)"""
    files = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".json"):
            files.append(file.replace(".json", ""))
    return sorted(files)


def load_json(report_name):
    filepath = os.path.join(DATA_FOLDER, f"{report_name}.json")
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@app.context_processor
def inject_reports():
    """Makes reports available in ALL templates"""
    return dict(reports=get_available_reports())


@app.route("/")
def home():
    reports = get_available_reports()
    return render_template("base.html", current_report=None)


@app.route("/report/<report_name>")
def show_report(report_name):
    data = load_json(report_name)

    if not data:
        abort(404)

    return render_template(
        "report.html",
        data=data,
        current_report=report_name
    )


if __name__ == "__main__":
    app.run(debug=True)
