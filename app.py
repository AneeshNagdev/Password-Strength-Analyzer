from flask import Flask, render_template, request, jsonify
# Make sure your file is named password_analyzer.py (underscore)
from password_analyzer import analyze_password

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    pw = data.get("password", "")
    result = analyze_password(pw)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
