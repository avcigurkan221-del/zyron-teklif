from flask import Flask, render_template, request, redirect
import json, uuid

app = Flask(__name__)
DB_FILE = "teklifler.json"

def load_data():
    try:
        with open(DB_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def admin():
    data = load_data()
    return render_template("admin.html", teklifler=data)

@app.route("/create", methods=["POST"])
def create():
    data = load_data()
    teklif_id = str(uuid.uuid4())[:8]

    data[teklif_id] = {
        "firma": request.form["firma"],
        "tutar": request.form["tutar"],
        "status": "bekliyor"
    }

    save_data(data)
    return redirect(f"/teklif/{teklif_id}")

@app.route("/teklif/<id>")
def teklif(id):
    data = load_data()
    return render_template("teklif.html", teklif=data[id], id=id)

@app.route("/approve/<id>")
def approve(id):
    data = load_data()
    data[id]["status"] = "onaylandı"
    save_data(data)
    return "ok"

app.run(debug=True)
