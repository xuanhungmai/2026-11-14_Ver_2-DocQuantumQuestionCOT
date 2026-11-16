import json
import os

from flask import Flask, abort, jsonify, render_template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "quantum_computing_100_cot.json")

app = Flask(__name__)


def load_data():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# Dữ liệu chỉ đọc -> nạp 1 lần khi khởi động server
DATA = load_data()


def format_item(stt, item):
    keys = sorted(
        (k for k in item if k.startswith("thought_")),
        key=lambda k: int(k.split("_")[1]),
    )
    return {
        "stt": stt,
        "total": len(DATA),
        "question": item.get("question", ""),
        "thoughts": [item[k] for k in keys],
        "answer": item.get("answer", ""),
    }


@app.route("/")
def index():
    return render_template("index.html", total=len(DATA))


@app.route("/api/questions/<int:stt>")
def get_question(stt):
    if stt < 1 or stt > len(DATA):
        abort(404, description=f"Số thứ tự phải nằm trong khoảng từ 1 đến {len(DATA)}.")
    return jsonify(format_item(stt, DATA[stt - 1]))


@app.errorhandler(404)
def not_found(e):
    return jsonify(error=e.description), 404


@app.route("/healthz")
def healthz():
    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
