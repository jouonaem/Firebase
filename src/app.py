from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

# ---------- CREATE ----------
@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    doc_ref = db.collection("students").add(data)
    return jsonify({"id": doc_ref[1].id, "message": "Student added!"}), 201


# ---------- READ ALL ----------
@app.route("/students", methods=["GET"])
def get_students():
    students_ref = db.collection("students").stream()
    students = [{**s.to_dict(), "id": s.id} for s in students_ref]
    return jsonify(students)


# ---------- READ ONE ----------
@app.route("/students/<id>", methods=["GET"])
def get_student(id):
    doc = db.collection("students").document(id).get()
    if doc.exists:
        return jsonify(doc.to_dict())
    return jsonify({"error": "Student not found"}), 404


# ---------- UPDATE ----------
@app.route("/students/<id>", methods=["PUT"])
def update_student(id):
    data = request.json
    db.collection("students").document(id).update(data)
    return jsonify({"message": "Student updated!"})


# ---------- DELETE ----------
@app.route("/students/<id>", methods=["DELETE"])
def delete_student(id):
    db.collection("students").document(id).delete()
    return jsonify({"message": "Student deleted!"})


if __name__ == "__main__":
    app.run(debug=True)
