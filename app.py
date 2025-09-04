from flask import Flask, jsonify, render_template, request, redirect
from pymongo import MongoClient
import certifi, json

app = Flask(__name__)

# MongoDB Atlas connection
MONGO_URI = "mongodb+srv://Abhay:Abhaypande@cluster0.60bxsoq.mongodb.net/"
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["mydb"]
collection = db["mycollection"]

# ---------- Task 1: /api returns JSON from file ----------
@app.route("/api")
def api():
    try:
        with open("data.json") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- Task 2: Form ----------
@app.route("/form", methods=["GET", "POST"])
def form():
    error = None
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        try:
            collection.insert_one({"name": name, "email": email})
            return redirect("/success")
        except Exception as e:
            error = str(e)
    return render_template("form.html", error=error)

@app.route("/success")
def success():
    return "<h2>Data submitted successfully</h2>"

# ---------- Home ----------
@app.route("/")
def home():
    return "<h3>Welcome! Visit <a href='/api'>/api</a> or <a href='/form'>/form</a></h3>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
